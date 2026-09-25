#!/usr/bin/env python3
"""
Phase 05 rebuilt funding model (Run 2, red team rebuild). Stdlib only.
Run: python3 rebuilt_model.py            (prints scenarios, writes CSVs here)

What changed vs run-2/funding-model/model.py (see audit_original.py for why):
  * Unit of growth is the GROUP (an organizer brings a room of people), not a
    lone viral user. MAU is derived from active groups.
  * Revenue is anchored to an external comparator instead of a 5%-of-signups
    freemium guess: Signal Technology Foundation 2024 Form 990 (as reported):
    revenue $29.4M vs expenses $38.0M; ~70% of funding from large donors,
    ~30% from users giving ~$5-$20/month [VERIFIED 2026 via secondary reports].
    With an ESTIMATED ~70M MAU [UNVERIFIED], user giving is ~$0.01/MAU/month,
    i.e. roughly 0.2% of MAU at $5. Our base (1.2%) is therefore ~6x Signal's
    user-giving rate -- an optimistic assumption, flagged; 'signal_anchor'
    runs the anchored rate. Signal's total cost ~$0.045/MAU/month anchors infra.
  * Three revenue lines, none of which is a toll between members:
      1. supporters (pay-what-you-can membership, $2-$12, avg modelled $5 gross)
      2. room archive (full-resolution media vault for a room, $4/mo, any
         member may pay; the room works fully without it)
      3. institutional sponsors (libraries, co-ops, unions, congregations,
         schools' parent associations) that pay a flat fee to cover rooms for
         their people; they see nothing but what members intentionally share
  * Hiring is ACTUALLY gated on revenue in code (the original claimed this in
    a docstring but hired on a fixed calendar).
  * Safety/support staffing scales with MAU from a funded floor; it can never
    be traded away (a deed term, see design section 3).
  * Legal/insurance/audit priced as line items; media storage accrues with
    tenure; the mind costs the platform $0 (user-supplied key or pass-through
    at cost); unfunded deficits are COUNTED, interest is paid in cash.
  * No PRI loan in the base case (the original's $1.45M loan was never
    checked against a lender). A loan is modelled only as a named variant.
"""
from dataclasses import dataclass, replace
import csv, math, os

HERE = os.path.dirname(os.path.abspath(__file__))

@dataclass(frozen=True)
class S:
    name: str = "base"
    months: int = 96
    # growth (groups)
    seed_groups: int = 40            # hand-seeded organizers' existing groups
    spawn0: float = 0.12             # new groups per active group per month, early [ASSUMPTION]
    spawn_decay: float = 0.99
    spawn_floor: float = 0.05
    group_churn: float = 0.04        # rooms that die each month [ASSUMPTION; kill test K2]
    members: float = 9.0
    active_share: float = 0.70
    overlap: float = 0.85            # people belong to several rooms
    # revenue
    supporter_rate: float = 0.012    # share of MAU paying [ASSUMPTION; ~6x Signal's user-giving rate]
    supporter_gross: float = 5.0
    supporter_churn: float = 0.05    # per month, applied to the paying pool
    archive_rate: float = 0.04       # share of active groups with a paid archive
    archive_price: float = 4.0
    sponsor_start: int = 12
    sponsor_adds: float = 1.0        # new institutional sponsors per month [ASSUMPTION]
    sponsor_churn: float = 0.02
    sponsor_fee: float = 200.0       # $/month average flat fee [ASSUMPTION]
    sponsor_groups_per_month: float = 3.0  # groups each sponsor brings in [ASSUMPTION]
    fee_pct: float = 0.029
    fee_fixed: float = 0.30
    vat_share: float = 0.0           # US-only until v3 (EU/UK gated)
    iap_share: float = 0.0           # web-first; native apps later
    # costs
    loaded: float = 1.28
    founder_salary_y1: float = 85_000   # used only in 'fulltime_from_day_one' variant
    founder_salary: float = 110_000     # full-time market-ish pay, switched on by revenue gate
    stipend_monthly: float = 3_000      # Phase A: each founder part-time stipend, NOT loaded
    lean_phase: bool = True             # Phase A until revenue covers the full-time crew
    ts_contract_monthly: float = 1_500  # Phase A: contracted on-call T&S/escalation + CSAM reporting
    ts_floor_fte: float = 0.5
    ts_per_mau: float = 150_000      # 1 T&S FTE per 150k MAU (report-driven, E2E private rooms) [ASSUMPTION]
    ts_salary: float = 72_000
    support_per_mau: float = 200_000
    support_salary: float = 60_000
    eng_salary: float = 150_000
    max_extra_eng: int = 6
    infra_per_mau: float = 0.04      # compute+bandwidth for text/links/compressed media [ASSUMPTION; Signal-order]
    infra_fixed: float = 1_500
    gb_added_per_mau: float = 0.03   # free media accrual (1 GB cap, compressed), tapering to 0 by m36
    gb_added_per_supporter: float = 0.8
    gb_added_per_archive_room: float = 4.0
    storage_per_gb: float = 0.00695 * 2   # B2 + one replica [VERIFIED 2026 price]
    legal_once: float = 45_000
    legal_base: float = 8_000        # counsel + insurance + trustee/protector fees (full-time phase)
    legal_lean: float = 3_500        # Phase A: US-only, adults-only, web-only, 40-300 groups
    audit_from: int = 18
    audit_monthly: float = 5_000     # annual code audit + financial review, amortised (full-time phase)
    audit_lean: float = 1_500        # Phase A: scoped audit of crypto/export paths only
    grant_total: float = 0.0         # restricted/expenditure-responsibility grants [UNVERIFIED availability]
    grant_months: tuple = (12, 36)
    intl_gate_mau: float = 150_000   # UK/EU launch only above this AND cash-positive
    intl_monthly: float = 6_000
    # funding
    founder_capital: float = 150_000
    patron_campaign: float = 55_000
    patron_month: int = 3
    loan_cap: float = 0.0
    loan_rate_m: float = 0.0025
    buffer: float = 20_000

def run(s: S):
    groups = float(s.seed_groups); spawn = s.spawn0
    sponsors = 0.0; supporters = 0.0; stored = 0.0
    cash = 0.0; loan = 0.0; extra_eng = 0; unfunded = 0.0; capital = 0.0
    intl = False; hist_net = []; hist_rev = []; lean = True; grad_month = None; infra_prev = s.infra_fixed
    rows = []
    for m in range(s.months):
        # --- growth ---
        if m >= s.sponsor_start:
            sponsors = sponsors * (1 - s.sponsor_churn) + s.sponsor_adds
        new_groups = (groups * spawn + sponsors * s.sponsor_groups_per_month) if m > 0 else 0
        groups = groups * (1 - s.group_churn) + new_groups
        spawn = max(s.spawn_floor, spawn * s.spawn_decay)
        mau = groups * s.members * s.active_share * s.overlap
        # --- revenue ---
        target_sup = mau * s.supporter_rate
        # supporter pool: churns at supporter_churn; recruitment closes 35%/month of the gap to the
        # Signal-anchored target share of MAU (so a growing MAU is not instantly monetised)
        supporters = supporters * (1 - s.supporter_churn) + max(0.0, target_sup - supporters * (1 - s.supporter_churn)) * 0.35
        archives = groups * s.archive_rate
        gross = supporters * s.supporter_gross + archives * s.archive_price
        txns = supporters + archives
        fees = gross * s.fee_pct + txns * s.fee_fixed + gross * s.iap_share * 0.15
        vat = gross * s.vat_share * 0.20
        sponsor_rev = sponsors * s.sponsor_fee * (1 - 0.01)  # invoiced, ACH
        rev = gross - fees - vat + sponsor_rev
        # --- costs ---
        L = s.loaded / 12
        fsal = s.founder_salary_y1 if m < 12 else s.founder_salary
        ts_fte = s.ts_floor_fte + max(0.0, mau / s.ts_per_mau - s.ts_floor_fte)
        sup_fte = math.floor(mau / s.support_per_mau)
        # revenue-gated engineering hire: trailing-3-month mean net must cover the hire x1.25
        if len(hist_net) >= 3 and extra_eng < s.max_extra_eng:
            if sum(hist_net[-3:]) / 3 >= 1.25 * s.eng_salary * L:
                extra_eng += 1
        full_team = (2 * fsal + ts_fte * s.ts_salary + sup_fte * s.support_salary + extra_eng * s.eng_salary) * L
        if lean and s.lean_phase:
            # graduation gate: trailing-3-month revenue covers the full-time crew + full legal
            full_cost_est = full_team + s.legal_base + s.audit_monthly + infra_prev + (s.intl_monthly if intl else 0)
            if len(hist_rev) >= 3 and sum(hist_rev[-3:]) / 3 >= 1.10 * full_cost_est:
                lean = False
                grad_month = m
        if lean and s.lean_phase:
            # T&S never shrinks below the deed floor: contract minimum, or MAU-scaled FTE cost if larger
            team = 2 * s.stipend_monthly + max(s.ts_contract_monthly, (mau / s.ts_per_mau) * s.ts_salary * L)
            heads = 2.0  # two part-time stewards + contracted safety
            extra_eng = 0
        else:
            team = full_team
            heads = 2 + ts_fte + sup_fte + extra_eng
        stored += mau * s.gb_added_per_mau * max(0.0, 1 - m / 36) + supporters * s.gb_added_per_supporter \
            + archives * s.gb_added_per_archive_room
        infra = mau * s.infra_per_mau + s.infra_fixed + stored * s.storage_per_gb
        legal = (s.legal_lean if (lean and s.lean_phase) else s.legal_base) + (s.legal_once if m == 0 else 0) \
            + ((s.audit_lean if (lean and s.lean_phase) else s.audit_monthly) if m >= s.audit_from else 0)
        if not intl and mau >= s.intl_gate_mau and len(hist_net) >= 3 and min(hist_net[-3:]) > 0:
            intl = True
        if intl:
            legal += s.intl_monthly
        interest = loan * s.loan_rate_m
        cost = team + infra + legal + interest
        net = rev - cost
        hist_net.append(net); hist_rev.append(rev); infra_prev = infra
        # --- funding ---
        g0, g1 = s.grant_months
        inflow = (s.founder_capital if m == 0 else 0) + (s.patron_campaign if m == s.patron_month else 0) \
            + (s.grant_total / (g1 - g0) if g0 <= m < g1 else 0)
        capital += inflow
        cash += inflow + net
        if cash < s.buffer and loan < s.loan_cap:
            d = min(s.buffer - cash, s.loan_cap - loan); loan += d; cash += d; capital += d
        runway_out = cash < 0
        if cash < 0:
            unfunded += -cash; cash = 0.0
        rows.append(dict(month=m, groups=round(groups), mau=round(mau), supporters=round(supporters),
                         archives=round(archives), sponsors=round(sponsors, 1), revenue=round(rev),
                         team=round(team), infra=round(infra), legal=round(legal), cost=round(cost),
                         net=round(net), heads=round(heads, 1), cash=round(cash), loan=round(loan),
                         capital_committed=round(capital), unfunded_cum=round(unfunded),
                         out_of_money=runway_out, lean_phase=(lean and s.lean_phase)))
    return rows

def breakeven(rows):
    st = 0
    for r in rows:
        st = st + 1 if r["revenue"] >= r["cost"] else 0
        if st >= 3:
            return r["month"] - 2
    return None

def first_out(rows):
    for r in rows:
        if r["out_of_money"]:
            return r["month"]
    return None

def report(s: S, write=True):
    rows = run(s)
    be = breakeven(rows); out = first_out(rows)
    endrow = rows[be] if be is not None else rows[-1]
    print(f"\n=== {s.name} ===")
    print(" mo | groups |    MAU | supp | arch | spons |   rev$ |  cost$ |   net$ | heads |  cash$ | unfunded$")
    for m in [0, 6, 12, 14, 18, 24, 30, 36, 42, 48, 54, 60, 72, 84, 95]:
        if m < len(rows):
            r = rows[m]
            print(f"{m:>3} | {r['groups']:>6,} | {r['mau']:>6,} | {r['supporters']:>4,} | {r['archives']:>4,} | "
                  f"{r['sponsors']:>5} | {r['revenue']:>6,} | {r['cost']:>6,} | {r['net']:>6,} | {r['heads']:>5} | "
                  f"{r['cash']:>6,} | {r['unfunded_cum']:>9,}")
    grad = next((r["month"] for r in rows if not r["lean_phase"]), None)
    print(f"lean phase ends (full-time crew affordable) at month: {grad}")
    print(f"break-even month: {be} | first month committed capital runs out: {out} | "
          f"capital committed ${endrow['capital_committed']:,} + unfunded gap ${endrow['unfunded_cum']:,} "
          f"= total needed to {'BE' if be is not None else 'm95'} ${endrow['capital_committed'] + endrow['unfunded_cum']:,}"
          f" | MAU at that point {endrow['mau']:,}")
    if write:
        with open(os.path.join(HERE, f"rebuilt_{s.name}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return rows, be, out

if __name__ == "__main__":
    base = S()
    scen = [
        base,
        replace(base, name="pessimistic_supporters_half", supporter_rate=0.006),
        replace(base, name="signal_anchor", supporter_rate=0.002),
        replace(base, name="pessimistic_rooms_die_faster", group_churn=0.06),
        replace(base, name="pessimistic_no_sponsors", sponsor_adds=0.0),
        replace(base, name="pessimistic_all", supporter_rate=0.006, group_churn=0.06, sponsor_adds=0.4,
                spawn0=0.07, spawn_floor=0.025),
        replace(base, name="bridge_loan_300k", loan_cap=300_000),
        replace(base, name="fulltime_from_day_one", lean_phase=False),
        replace(base, name="grant_bridge_250k", grant_total=250_000),
        replace(base, name="sponsor_led", sponsor_adds=2.0),
        replace(base, name="sponsor_led_half_fee", sponsor_adds=2.0, sponsor_fee=100.0),
        replace(base, name="optimistic", supporter_rate=0.025, spawn0=0.15, sponsor_adds=2.0),
        replace(base, name="optimistic_plus_grant", supporter_rate=0.025, spawn0=0.15, sponsor_adds=2.0,
                grant_total=250_000),
    ]
    for s in scen:
        report(s)
    # unit economics: variable revenue vs variable cost per MAU (no team, no fixed cost)
    b = base
    L = b.loaded / 12
    per_group_mau = b.members * b.active_share * b.overlap
    var_cost = b.infra_per_mau + (b.ts_salary * L) / b.ts_per_mau + 0.01  # +~$0.01 storage
    archive_per_mau = b.archive_rate * b.archive_price * (1 - b.fee_pct) / per_group_mau
    net_per_supporter = b.supporter_gross * (1 - b.fee_pct) - b.fee_fixed
    breakeven_share = (var_cost - archive_per_mau) / net_per_supporter
    print(f"\n=== unit economics (members only) ===\nvariable cost/MAU ~ ${var_cost:.3f}; archive revenue/MAU ${archive_per_mau:.3f}; "
          f"net per supporter ${net_per_supporter:.2f}\n=> supporter share of MAU needed just to cover VARIABLE cost: {breakeven_share:.1%} "
          f"(base assumption {b.supporter_rate:.1%}); every point below that makes growth LOSE money per member.")
    # what would have to be true: minimum supporter share of MAU for break-even by month 72
    print("\n=== what would have to be true (break-even by month 72, lean->full-time gate as coded) ===")
    for spawn0 in (0.12, 0.15):
        for adds in (0.0, 1.0, 2.0):
            need = None
            for k in range(5, 201):
                r = k / 1000
                rows = run(replace(base, supporter_rate=r, spawn0=spawn0, sponsor_adds=adds))
                be = breakeven(rows)
                if be is not None and be <= 72:
                    need = r; break
            print(f"spawn0={spawn0:.2f} sponsors/mo={adds:.0f}: supporter share of MAU needed = "
                  f"{'>20%' if need is None else f'{need:.1%}'}")
