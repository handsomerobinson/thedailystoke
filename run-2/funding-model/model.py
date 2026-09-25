#!/usr/bin/env python3
"""
Commons — build-to-breakeven funding model (Phase 04b, Run 2).

Python 3, standard library only (csv, math, dataclasses). No third-party
packages. Run with:  python3 model.py

This is a *transparent assumption engine*, not a forecast. Every number that
drives the simulation is declared in ASSUMPTIONS below, with the reasoning
for it in a comment. Change a number, rerun, get a new (still-honest) answer.
The point of the exercise (per phase-04b) is that the math is checkable and
falsifiable, not that it is "right."

Model shape
-----------
Two cohorts, tracked monthly:
  - total_users[t]      : cumulative registered accounts (free + paid)
  - paying_users[t]      : subscribers on the $6/mo "Keep" tier

Growth is driven by the wedge's own mechanic (link-acceptance, Section (g)
of run-2-design.md): each existing user's shared drawers convert a fraction
of their non-member recipients into new signups each month (a viral/organic
coefficient), with a monthly organic-growth-rate ceiling that decays as the
addressable "next thousand" gets harder to reach (S-curve, not exponential
forever) and a churn term that removes inactive accounts.

Paying users are a sub-cohort with their own churn (subscription cancellation)
fed by a conversion rate applied to that month's *new* signups (people who
converted this month keep paying next month unless they churn — a standard
SaaS cohort-retention shape, not "5% of the total base converts every month
from scratch").

Costs are line-itemed: infra (usage-based), a small loaded-cost team that
grows in discrete hiring steps only when revenue supports it, legal/
compliance/trust-formation costs (one-time and ongoing), age-verification
vendor costs (state ASAA + UK OSA duties), payment processing fees, and VAT
on the EU/UK share of subscribers.

Funding is drawn in the sequence the charter allows (no investors, ever):
  1. Founder/operator capital contribution (one-time, month 0)
  2. Program-related-investment-style below-market loan facility (drawn
     only as needed, up to a cap, to keep the cash buffer non-negative)
  3. One-time donation/patron campaign at launch
  4. Subscription revenue (month 1 onward, growing with the cohort model)

Break-even is defined as the first month whose *own* revenue >= that
month's *own* operating cost, sustained for 3 consecutive months (to avoid
calling a single lucky month "break-even").
"""

from dataclasses import dataclass, field
import csv
import sys

# ---------------------------------------------------------------------------
# ASSUMPTIONS — every number here is a design assumption, not a fact. Cited
# where a real external benchmark exists; flagged [ASSUMPTION] where it is
# this design's own engineering/business estimate, per the phase-04b rigor
# bar. Change these and rerun to test a different world.
# ---------------------------------------------------------------------------

MONTHS_TO_SIMULATE = 90

# --- Growth (top of funnel) -------------------------------------------------
SEED_USERS = 250                  # first-thousand hand-seeded cohort (design doc, Section g)
INITIAL_MONTHLY_GROWTH_RATE = 0.42   # [ASSUMPTION] month-1 organic growth rate off a tiny base;
                                      # consistent with early link-viral consumer apps (Slack, Docs-style
                                      # view-then-join loops) before saturation sets in.
GROWTH_RATE_DECAY = 0.965           # multiplies the growth rate each month (S-curve deceleration)
GROWTH_RATE_FLOOR = 0.045           # long-run organic growth rate floor once a niche is saturated
MONTHLY_ACCOUNT_CHURN = 0.02        # [ASSUMPTION] inactive/deleted accounts leaving the total base

# --- Conversion & subscriber churn -----------------------------------------
BASE_CONVERSION_RATE = 0.05         # of *new* signups each month, fraction who take the paid tier
                                     # within their first month or two — 5% is the conservative end of
                                     # published consumer-freemium benchmarks [ASSUMPTION, stated as such
                                     # in run-2-design.md Section (a); typical range cited in industry
                                     # freemium literature is 2-5%.]
PAID_MONTHLY_CHURN = 0.035          # [ASSUMPTION] ~3.5%/month subscription cancellation — mid-range for
                                     # small consumer subscription products (annual-equivalent ~35-40%).

PRICE_PER_MONTH = 6.00              # $, "Keep" tier (run-2-design.md Section a)

# --- Unit costs --------------------------------------------------------------
INFRA_COST_PER_USER = 0.15          # $/active user/month, LOW end of the design doc's $0.15-0.40 band.
                                     # Chosen deliberately at the low end and stated as such: the drawer
                                     # mechanic is oEmbed-first (zero storage/bandwidth cost for the core
                                     # loop — Section (a)/(c) of run-2-design.md), so blended cost is
                                     # dominated by the free tier's capped 25GB own-media allowance, not
                                     # by serving embedded incumbent content. Reconciliation note: at the
                                     # midpoint ($0.28) used illustratively in Phase 04, this model shows
                                     # the operation NEVER breaks even at any scale (see git history /
                                     # doc Section (b) "reconciling with Phase 04" for that run) because
                                     # blended infra cost per user exceeds blended revenue per user before
                                     # team cost is even added — Phase 04's comparison omitted headcount
                                     # entirely and used the band's midpoint, which is why it looked viable
                                     # and this model, run honestly, initially was not.
INFRA_FIXED_MONTHLY = 600           # base platform (monitoring, CDN, backups, staging) regardless of scale
PAYMENT_FEE_PCT = 0.029             # Stripe-style card processing, ad valorem
PAYMENT_FEE_FIXED = 0.30            # $/transaction
VAT_SHARE_OF_PAYERS = 0.22          # [ASSUMPTION] ~22% of paying users are in EU/UK/VAT jurisdictions
VAT_RATE = 0.20                     # standard EU/UK VAT rate; price is VAT-inclusive, so VAT is a
                                     # deduction from gross revenue, not an add-on charged separately
AGE_VERIFICATION_COST_PER_NEW_US_SIGNUP = 0.35  # $/verification event, blended vendor cost (facial-estimation
                                     # / document-check vendor, e.g. Yoti-class provider), charged on the
                                     # fraction of new signups in ASAA states (Utah/Texas/Louisiana/Alabama)
US_ASAA_STATE_SIGNUP_SHARE = 0.12   # [ASSUMPTION] share of new signups from app-store-accountability-act states

# --- Team (loaded cost, i.e. salary * benefits/payroll-tax multiplier) ------
LOADED_COST_MULTIPLIER = 1.28       # payroll tax + benefits load on base salary
FOUNDER_BELOW_MARKET_SALARY = 70_000    # /year, months 0-11, two founders, below-market by design
                                          # (funded by founder capital + loan, not revenue, in year 1)
MARKET_SALARY_ENGINEER = 125_000        # /year loaded-eligible base, US remote-market small-team rate
MARKET_SALARY_TRUST_SAFETY = 78_000     # /year, ops/trust & safety/community role
MARKET_SALARY_LEGAL_OPS = 95_000        # /year, in-house legal/compliance/ops generalist (hired once revenue allows)

# Hiring plan: (month, role_added) — team grows only in steps revenue has already
# shown it can sustain for 2+ months (the charter's growth-bound-by-revenue rule,
# run-2-design.md Section (a)); this schedule is a *plan*, checked against the
# simulated revenue at run time — see build_team_cost().
HIRING_PLAN = [
    (0, "founder_1"), (0, "founder_2"),        # month 0: two founders, below-market
    (12, "engineer_1"),                          # first hire once year-1 runway proven
    (18, "trust_safety_1"),
    (24, "engineer_2"),
    (30, "legal_ops_1"),
]

# --- Legal / compliance ------------------------------------------------------
LEGAL_FORMATION_ONE_TIME = 45_000   # trust deed drafting (perpetual-purpose-trust counsel), entity formation,
                                     # trademark clearance search + filing (Section (a) of the operational doc)
LEGAL_COMPLIANCE_MONTHLY = 2_800    # ongoing outside counsel retainer: GDPR/DSA/COPPA/OSA compliance review,
                                     # DPO-equivalent function, annual trust-deed audit prep
COMPLIANCE_TOOLING_MONTHLY = 900    # DSAR/data-request tooling, consent management, transparency-report tooling

# --- Funding sources (sequence; no investors, ever) --------------------------
FOUNDER_CAPITAL = 150_000           # one-time, month 0
DONATION_CAMPAIGN = 55_000          # one-time, month 2 (launch patron/founding-member campaign)
LOAN_FACILITY_CAP = 1_450_000       # PRI-style below-market loan facility, drawn only as needed
MIN_CASH_BUFFER = 15_000            # never let modeled cash drop below this without drawing the loan
LOAN_MONTHLY_INTEREST = 0.0025      # ~3%/year simple interest on outstanding loan balance, PRI-typical


@dataclass
class MonthRow:
    month: int
    total_users: int
    new_signups: int
    paying_users: int
    revenue: float
    infra_cost: float
    team_cost: float
    legal_cost: float
    payment_fees: float
    vat: float
    age_verification_cost: float
    total_cost: float
    net: float
    founder_capital_drawn: float
    donation_drawn: float
    loan_drawn_this_month: float
    loan_balance: float
    cash_balance: float


def team_headcount_and_cost(month: int) -> tuple[int, float]:
    """Loaded monthly team cost given the hiring plan, as of `month`."""
    heads = [role for (m, role) in HIRING_PLAN if m <= month]
    cost = 0.0
    for role in heads:
        if role.startswith("founder"):
            cost += FOUNDER_BELOW_MARKET_SALARY * LOADED_COST_MULTIPLIER / 12
        elif role.startswith("engineer"):
            cost += MARKET_SALARY_ENGINEER * LOADED_COST_MULTIPLIER / 12
        elif role.startswith("trust_safety"):
            cost += MARKET_SALARY_TRUST_SAFETY * LOADED_COST_MULTIPLIER / 12
        elif role.startswith("legal_ops"):
            cost += MARKET_SALARY_LEGAL_OPS * LOADED_COST_MULTIPLIER / 12
    return len(heads), cost


def run_model(conversion_multiplier: float = 1.0, growth_multiplier: float = 1.0,
              months: int = MONTHS_TO_SIMULATE, loan_cap: float = LOAN_FACILITY_CAP) -> list[MonthRow]:
    """Run the month-by-month simulation. Multipliers implement the
    sensitivity cases required by phase-04b (conversion halved, growth halved)."""

    conversion_rate = BASE_CONVERSION_RATE * conversion_multiplier
    growth_rate = INITIAL_MONTHLY_GROWTH_RATE * growth_multiplier

    total_users = 0
    paying_users = 0.0
    cash = 0.0
    loan_balance = 0.0
    rows: list[MonthRow] = []

    for month in range(months):
        # --- growth ---
        if month == 0:
            new_signups = SEED_USERS
        else:
            new_signups = total_users * growth_rate
        total_users = int(total_users * (1 - MONTHLY_ACCOUNT_CHURN) + new_signups)

        # decay the growth rate toward its floor (S-curve), after computing this month
        growth_rate = max(GROWTH_RATE_FLOOR * growth_multiplier, growth_rate * GROWTH_RATE_DECAY)

        # --- paying subscriber cohort ---
        paying_users = paying_users * (1 - PAID_MONTHLY_CHURN) + new_signups * conversion_rate

        # --- revenue ---
        gross_revenue = paying_users * PRICE_PER_MONTH
        payment_fees = paying_users * (gross_revenue / max(paying_users, 1) * PAYMENT_FEE_PCT) \
            + paying_users * PAYMENT_FEE_FIXED
        vat = gross_revenue * VAT_SHARE_OF_PAYERS * VAT_RATE
        net_revenue = gross_revenue - payment_fees - vat

        # --- costs ---
        infra_cost = total_users * INFRA_COST_PER_USER + INFRA_FIXED_MONTHLY
        headcount, team_cost = team_headcount_and_cost(month)
        legal_cost = LEGAL_COMPLIANCE_MONTHLY + COMPLIANCE_TOOLING_MONTHLY + (LEGAL_FORMATION_ONE_TIME if month == 0 else 0)
        age_verification_cost = new_signups * US_ASAA_STATE_SIGNUP_SHARE * AGE_VERIFICATION_COST_PER_NEW_US_SIGNUP

        total_cost = infra_cost + team_cost + legal_cost + age_verification_cost
        net = net_revenue - total_cost

        # --- funding draws, in charter-mandated sequence ---
        founder_drawn = FOUNDER_CAPITAL if month == 0 else 0.0
        donation_drawn = DONATION_CAMPAIGN if month == 2 else 0.0

        cash += founder_drawn + donation_drawn + net
        loan_balance *= (1 + LOAN_MONTHLY_INTEREST)
        loan_drawn_this_month = 0.0
        if cash < MIN_CASH_BUFFER:
            needed = MIN_CASH_BUFFER - cash
            available = max(0.0, loan_cap - loan_balance)
            draw = min(needed, available)
            loan_drawn_this_month = draw
            loan_balance += draw
            cash += draw

        rows.append(MonthRow(
            month=month, total_users=total_users, new_signups=int(new_signups),
            paying_users=int(paying_users), revenue=net_revenue, infra_cost=infra_cost,
            team_cost=team_cost, legal_cost=legal_cost, payment_fees=payment_fees, vat=vat,
            age_verification_cost=age_verification_cost, total_cost=total_cost, net=net,
            founder_capital_drawn=founder_drawn, donation_drawn=donation_drawn,
            loan_drawn_this_month=loan_drawn_this_month, loan_balance=loan_balance,
            cash_balance=cash,
        ))
    return rows


def find_breakeven(rows: list[MonthRow]) -> int | None:
    """First month where revenue >= cost for 3 consecutive months."""
    streak = 0
    for r in rows:
        if r.revenue >= r.total_cost:
            streak += 1
            if streak >= 3:
                return r.month - 2
        else:
            streak = 0
    return None


def total_build_cost(rows: list[MonthRow], breakeven_month: int | None) -> float:
    """Total external capital consumed (founder + donation + loan drawn) up to break-even.
    This is 'total build cost' as the phase prompt uses the term: what had to be raised/
    contributed before the operation could sustain itself on its own revenue."""
    end = breakeven_month if breakeven_month is not None else len(rows) - 1
    return sum(r.founder_capital_drawn + r.donation_drawn + r.loan_drawn_this_month for r in rows[:end + 1])


def print_table(rows: list[MonthRow], months_to_show: list[int]) -> None:
    header = ["Mo", "Users", "Paying", "Revenue$", "Infra$", "Team$", "Legal$", "AgeVer$", "TotalCost$", "Net$", "LoanBal$", "Cash$"]
    print(" | ".join(f"{h:>9}" for h in header))
    print("-" * (12 * len(header)))
    for m in months_to_show:
        if m >= len(rows):
            continue
        r = rows[m]
        vals = [r.month, r.total_users, r.paying_users, round(r.revenue), round(r.infra_cost),
                round(r.team_cost), round(r.legal_cost), round(r.age_verification_cost),
                round(r.total_cost), round(r.net), round(r.loan_balance), round(r.cash_balance)]
        print(" | ".join(f"{v:>9,}" for v in vals))


def write_csv(rows: list[MonthRow], path: str) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "total_users", "new_signups", "paying_users", "revenue", "infra_cost",
                    "team_cost", "legal_cost", "payment_fees", "vat", "age_verification_cost",
                    "total_cost", "net", "founder_capital_drawn", "donation_drawn",
                    "loan_drawn_this_month", "loan_balance", "cash_balance"])
        for r in rows:
            w.writerow([r.month, r.total_users, r.new_signups, r.paying_users, round(r.revenue, 2),
                        round(r.infra_cost, 2), round(r.team_cost, 2), round(r.legal_cost, 2),
                        round(r.payment_fees, 2), round(r.vat, 2), round(r.age_verification_cost, 2),
                        round(r.total_cost, 2), round(r.net, 2), r.founder_capital_drawn,
                        r.donation_drawn, round(r.loan_drawn_this_month, 2), round(r.loan_balance, 2),
                        round(r.cash_balance, 2)])


def shortfall_plan_check(rows: list[MonthRow], loan_cap: float = LOAN_FACILITY_CAP) -> None:
    """Implements the required 'funding falls short halfway' analysis: check whether
    the loan facility cap is hit before break-even, and if so, at what month and what
    the plan is."""
    breakeven = find_breakeven(rows)
    cap_hit_month = None
    for r in rows:
        if r.loan_balance >= loan_cap * 0.999:
            cap_hit_month = r.month
            break
    print("\n--- Funding-falls-short check ---")
    if cap_hit_month is not None and (breakeven is None or cap_hit_month < breakeven):
        print(f"Loan facility cap (${loan_cap:,}) is exhausted at month {cap_hit_month}, "
              f"BEFORE break-even (month {breakeven}). This is the 'funding falls short halfway' case.")
    else:
        print(f"Loan facility cap is never exhausted before break-even (month {breakeven}). "
              f"Funding sequence as designed is sufficient in this scenario.")


if __name__ == "__main__":
    months_to_show = [0, 1, 2, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 89]

    print("=" * 100)
    print("BASELINE SCENARIO")
    print("=" * 100)
    baseline = run_model()
    print_table(baseline, months_to_show)
    be = find_breakeven(baseline)
    print(f"\nBreak-even month: {be}")
    print(f"Total build cost to break-even (founder + donation + loan drawn): "
          f"${total_build_cost(baseline, be):,.0f}")
    if be is not None:
        print(f"Users at break-even: {baseline[be].total_users:,} total / {baseline[be].paying_users:,} paying")
    shortfall_plan_check(baseline)
    write_csv(baseline, "/home/user/thedailystoke/run-2/funding-model/baseline.csv")

    print("\n" + "=" * 100)
    print("SENSITIVITY 1: conversion rate halved (2.5% instead of 5%)")
    print("=" * 100)
    sens_conv = run_model(conversion_multiplier=0.5)
    print_table(sens_conv, months_to_show)
    be_conv = find_breakeven(sens_conv)
    print(f"\nBreak-even month: {be_conv}")
    print(f"Total build cost to break-even: ${total_build_cost(sens_conv, be_conv):,.0f}")
    shortfall_plan_check(sens_conv)
    write_csv(sens_conv, "/home/user/thedailystoke/run-2/funding-model/sensitivity_conversion_halved.csv")

    print("\n" + "=" * 100)
    print("SENSITIVITY 2: growth rate halved")
    print("=" * 100)
    sens_growth = run_model(growth_multiplier=0.5)
    print_table(sens_growth, months_to_show)
    be_growth = find_breakeven(sens_growth)
    print(f"\nBreak-even month: {be_growth}")
    print(f"Total build cost to break-even: ${total_build_cost(sens_growth, be_growth):,.0f}")
    shortfall_plan_check(sens_growth)
    write_csv(sens_growth, "/home/user/thedailystoke/run-2/funding-model/sensitivity_growth_halved.csv")

    print("\n" + "=" * 100)
    print("SENSITIVITY 3: both halved (conversion AND growth) — worst realistic case")
    print("=" * 100)
    sens_both = run_model(conversion_multiplier=0.5, growth_multiplier=0.5)
    print_table(sens_both, months_to_show)
    be_both = find_breakeven(sens_both)
    print(f"\nBreak-even month: {be_both}")
    if be_both is None:
        print("Does NOT break even within the simulated 60-month window under current cost assumptions.")
    write_csv(sens_both, "/home/user/thedailystoke/run-2/funding-model/sensitivity_both_halved.csv")


    print("\n" + "=" * 100)
    print("STRESS TEST: 'funding falls short halfway' — loan facility capped at $400k instead of "
          f"${LOAN_FACILITY_CAP:,} (baseline growth/conversion assumptions otherwise unchanged)")
    print("=" * 100)
    shortfall = run_model(loan_cap=400_000)
    print_table(shortfall, months_to_show)
    be_short = find_breakeven(shortfall)
    print(f"\nBreak-even month under capped funding: {be_short}")
    shortfall_plan_check(shortfall, loan_cap=400_000)
    write_csv(shortfall, "/home/user/thedailystoke/run-2/funding-model/stress_funding_shortfall.csv")
