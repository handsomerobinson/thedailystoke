#!/usr/bin/env python3
"""
Porchlight (working name) -- funding model, month 0 to break-even.
Run 3, Phase 04b ("make it real").  Python 3.9+, standard library only.

    python3 model.py            # base case month by month + summary
    python3 model.py --all      # base + sensitivities + halfway shortfall + P04 reconciliation
    python3 model.py --scenario both [--every 3] [--csv out.csv]
    python3 model.py --unit     # cost per claimed member per month at 10K / 1M / 100M

Labels on assumptions:
  [SRC]    from a cited public source (listed in run-3-operational.md, section 8)
  [P04]    carried over from Phase 04 (run-3-design.md sections 3.2 and 7.2)
  [REV]    Phase 04 number revised here; the write-up says why
  [ASSUME] planning number to be verified in operation

Charter constraints are structural in this code:
  * there is no equity / investment inflow type at all;
  * there is no advertising, data-licensing or creator-payout line at all;
  * the only debt is two unsecured, subordinated, non-convertible,
    zero-interest recoverable-grant PRIs, repayable only from surplus above a
    6-month reserve, with no security interest in user data or IP
    (IP and domain are held by the trust, not the operating company);
  * from month 60 the deed caps bind: grants <= 25% of trailing-12-month
    inflows and no single grant > 10% of trailing-12-month inflows.  A grant
    that would break a cap is declined and counted.

Cash basis, nominal US dollars, month 0 = January 2027.  US sales tax is
charged on top of US prices (pass-through, not revenue); EU/UK VAT is
included in displayed prices and remitted (modelled as a deduction).
"""
from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass, replace

# --------------------------------------------------------------------------
# 1. Assumptions
# --------------------------------------------------------------------------

SEASON = {0: 0.8, 1: 0.9, 2: 1.0, 3: 1.0, 4: 1.1, 5: 1.2,     # Jan..Jun
          6: 1.0, 7: 0.9, 8: 1.1, 9: 1.3, 10: 1.6, 11: 1.7}   # Jul..Dec [ASSUME]

LOAD = 0.24        # employer payroll taxes, health, retirement [ASSUME: typical US 20-30%]
PER_HEAD = 7_000   # equipment, software seats, stipend, training per year [ASSUME]
RAISE = 0.03       # annual pay increase [ASSUME]
HIRE_COST = 15_000 # recruiting + onboarding per hire [ASSUME]
SALARY = {         # US remote, mid-cost market, 2027 dollars [ASSUME]
    "eng_senior": 170_000,
    "eng_security": 180_000,     # applied cryptography + infrastructure
    "eng_mid": 140_000,
    "design_community": 135_000,
    "ts_lead": 115_000,          # trust & safety: in-house, never outsourced (deed)
    "ts_specialist": 85_000,
    "support": 72_000,
    "ops_finance": 120_000,
}


@dataclass
class A:
    name: str = "base"
    months: int = 120

    # ---- timeline (month 0 = Jan 2027)
    launch_v1: int = 6    # US web: plan link, memory pages, claim, export, Keepers
    launch_v2: int = 15   # Tables, Halls, opt-in mind, EU + UK
    launch_v3: int = 30   # open seats (per locale), the Window, federation

    # ---- casual organisers (the unit that spreads) [P04 7.2]
    ext_org_at_launch: float = 400.0     # new organisers/month from non-viral channels at launch [ASSUME]
    ext_org_growth: float = 0.07         # monthly growth of those channels to month 48 [ASSUME]
    ext_org_growth_late: float = 0.02    # after month 48 [ASSUME]
    ext_org_cap: float = 12_000.0        # [ASSUME]
    organic_per_org: float = 0.24        # 8 guest touches x 3% guest->host [P04]
    org_retention: float = 0.70          # month-to-month [P04]  -> lifetime k = 0.24/0.30 = 0.8
    touches_per_org: float = 8.0         # [P04: 1.5 plans x 9 invitees x 60% open]
    claim_new_org: float = 0.50          # new organisers who claim a passkey [ASSUME]
    claim_per_touch: float = 0.010       # guest touches ending in a claim [ASSUME]

    # ---- Halls: recurring-event organisations (v2).  A separate segment because
    # a run club or choir organises every week: it does not churn like a party host.
    hall_from_org: float = 0.0015        # share of active casual organisers who open a Hall per month [ASSUME]
    ext_halls_at_v2: float = 20.0        # direct outreach: libraries, run clubs, choirs, PTAs [ASSUME]
    ext_halls_growth: float = 0.05
    ext_halls_cap: float = 250.0
    hall_churn: float = 0.030            # [ASSUME]
    hall_new_people: float = 8.0         # new attendees per Hall per month [ASSUME]
    hall_claim_rate: float = 0.30        # new attendees who claim (to follow the schedule) [ASSUME]
    hall_host_rate: float = 0.03         # new attendees who later organise their own plan [ASSUME]
    hall_price: float = 20.0             # Meetup Standard is $29.99/mo [SRC]; P04 said $12 [REV]
    hall_waiver: float = 0.20            # free for mutual aid / hardship [P04]
    members_per_institution: float = 20_000.0   # libraries, rec departments, universities [ASSUME]
    institution_price: float = 100.0     # per month, invoiced annually [ASSUME]

    member_churn: float = 0.025          # claimed members going dormant per month [ASSUME]
    growth_mult: float = 1.0             # scenario lever

    # ---- Keepers: pay-what-you-can membership.  Suggested $5/mo or $50/yr (the deed
    # ceiling is $5 in 2026 dollars); P04 suggested $4 [REV].  Minimum $1.
    keeper_new: float = 0.032            # new claimed members who become Keepers [ASSUME; freemium ~2.1% SRC anchor]
    keeper_base: float = 0.0003          # monthly conversion of the existing non-paying base [ASSUME]
    keeper_churn: float = 0.040          # incl. failed cards [ASSUME]
    annual_share: float = 0.55           # [ASSUME]
    price_monthly: float = 4.25          # mean chosen monthly amount [ASSUME]
    price_annual: float = 45.0           # mean chosen annual amount [ASSUME]
    founding_keepers: int = 1_200        # "founding year" pledge at launch, $60 once [ASSUME]
    conv_mult: float = 1.0               # scenario lever (Keepers and Hall formation)

    # ---- payments and tax
    card_pct: float = 0.029 + 0.007 + 0.005   # Stripe card + Billing + Tax [SRC]
    card_fixed: float = 0.30                  # [SRC]
    intl_extra_pct: float = 0.015 + 0.010     # international card + FX [SRC]
    intl_payer_share_v2: float = 0.30         # [ASSUME]
    vat_payer_share_v2: float = 0.25          # consumer payers in EU/UK [ASSUME]
    vat_rate: float = 0.21                    # EU 17-27%, UK 20% [SRC range]
    refund_rate: float = 0.01                 # refunds + chargebacks [ASSUME]
    ach_pct: float = 0.008                    # ACH, capped $5 [SRC-ish]

    # ---- variable cost per claimed member per month (see --unit for line items)
    infra_per_member: float = 0.012           # [P04, re-checked in write-up (c)]
    mind_share_v2: float = 0.30               # members who switch the mind on [ASSUME]
    mind_cost_per_user: float = 0.05          # average; hard cap $0.10 [P04]
    email_per_member: float = 0.002           # [ASSUME]
    cost_per_touch: float = 0.0005            # guest page loads, KB of ciphertext [ASSUME]

    # ---- staffing workload drivers [ASSUME; private small groups, reports-only moderation]
    reports_per_member: float = 0.0006        # 0.6 reports per 1,000 claimed members per month
    hours_per_report: float = 0.5             # triage, review, statement of reasons, appeals
    ts_fixed_hours: float = 40.0              # lawful process, NCMEC, NCII 48h desk, DSA/OSA records
    tickets_per_member: float = 0.0012
    hours_per_ticket: float = 0.20
    fte_hours: float = 140.0                  # productive hours per FTE-month (T&S exposure-capped)

    # ---- fixed non-staff costs [ASSUME]
    formation_legal: float = 90_000           # m0-m2: deed, PBC charter, Guardian, trustee, ToS, TM clearance
    counsel_v1: float = 5_000                 # retainer per month
    counsel_v2: float = 9_000                 # + EU/UK regimes, VAT, DSA/OSA
    counsel_per_million: float = 3_000
    eu_uk_reps: float = 1_200                 # GDPR Art.27 rep + DSA Art.13 legal rep + UK rep
    trust_admin: float = 2_000                # Delaware administrative trustee, Guardian, enforcer
    insurance: float = 2_000                  # D&O, cyber, tech E&O, general liability
    insurance_per_million: float = 1_000
    accounting: float = 3_700
    crypto_audit_prelaunch: float = 80_000    # external audit of E2EE design + web client
    security_audit_annual: float = 50_000
    covenant_audit_semiannual: float = 20_000 # H5 external audit
    election_admin_annual: float = 10_000     # independent administrator, member-elected trustees
    infra_base_v1: float = 1_500
    infra_base_v2: float = 3_000              # second region (EU)
    ts_tooling: float = 500
    saas_per_fte: float = 150

    # ---- funding sequence.  No equity type exists.
    founder_gift: float = 800_000             # m0; $150k of it is the trust's continuity reserve [ASSUME -- biggest single assumption]
    continuity_reserve: float = 150_000       # held by the trust, outside the PBC's creditors
    seed_grants: tuple = ((3, 100_000), (7, 100_000))
    program_grants: tuple = ((9, 150_000), (11, 150_000), (15, 200_000), (21, 200_000),
                             (27, 200_000), (33, 200_000), (39, 200_000), (45, 200_000),
                             (51, 150_000), (57, 150_000), (63, 150_000), (69, 150_000))
    caps_from: int = 60                       # deed source caps bind from month 60 [REV: P04 said year 3]
    patrons: tuple = ((6, 4_000), (18, 7_000), (36, 8_000))   # (from month, $/mo); <= $10k/yr per patron
    # Two recoverable-grant PRIs: unsecured, subordinated, non-convertible, 0% interest,
    # repaid ONLY out of cash above a 6-month reserve (50% of the excess each month),
    # forgiven on a solvent wind-down, no acceleration, no board seat, no data rights.
    # gates are proxies for the Phase 04 hypotheses: #1 needs H1-H3 read (>= 2k claimed,
    # >= 2% paying); #2 needs H4/H7 (>= 30k claimed, >= 2% paying).
    pri: tuple = ((12, 1_250_000, 2_000, 0.02), (36, 1_250_000, 30_000, 0.02))
    pri_repay_share: float = 0.5
    pri_reserve_months: float = 6.0

    # ---- runway policy
    freeze_runway: float = 9.0                # months -> hiring freeze
    ember_runway: float = 6.0                 # -> ember mode (skeleton crew; service stays up)
    ember_exit_runway: float = 12.0
    shortfall_from: int | None = None         # from this month grants + PRI fail, patrons halve


# --------------------------------------------------------------------------
# 2. Helpers
# --------------------------------------------------------------------------

def loaded_monthly(role: str, month: int) -> float:
    return (SALARY[role] * (1 + LOAD) * (1 + RAISE) ** (month // 12) + PER_HEAD) / 12.0


def staffing(a: A, month: int, m: float, mode: str, afford: bool = True) -> dict:
    """FTE by role.  T&S and support are sized by workload, never by revenue:
    if money cannot pay for the safety staff a feature needs, the feature is
    paused (Halls' public events, open seats), not the safety staff."""
    ts_hours = m * a.reports_per_member * a.hours_per_report + a.ts_fixed_hours
    sup_hours = m * a.tickets_per_member * a.hours_per_ticket
    if mode == "ember":
        # skeleton crew keeps the service, exports and safety running; growth features paused.
        # Safety staffing is still sized by workload -- ember never cuts trust & safety.
        return {"eng_senior": 1, "eng_security": 0.5 if m >= 250_000 else 0.0,
                "design_community": 0.5, "ts_lead": 1,
                "ts_specialist": max(0, math.ceil(ts_hours / a.fte_hours) - 1),
                "support": math.ceil(sup_hours / a.fte_hours / 2) if m >= 150_000 else 0}
    # core: 4 FTE.  Growth hires (extra eng, support beyond half-workload, ops) are
    # revenue-gated: only once trailing operating revenue covers opex (after break-even).
    s = {"eng_senior": 1, "eng_security": 1,
         "design_community": 1 + (1 if m >= 2e6 and afford else 0),
         "ts_lead": 1 if month >= 3 else 0}
    floor = (1 if month >= a.launch_v2 else 0) + (1 if month >= a.launch_v3 else 0)
    s["ts_specialist"] = max(floor, math.ceil(ts_hours / a.fte_hours) - 1)
    s["support"] = (math.ceil(sup_hours / a.fte_hours) if afford
                    else math.ceil(sup_hours / a.fte_hours / 2)) if m >= 150_000 else 0
    if afford:
        s["eng_senior"] += (1 if m >= 250_000 else 0) + int(m // 5_000_000)
        s["eng_security"] += int(m // 10_000_000)
        s["design_community"] += int(m // 10_000_000)
        s["eng_mid"] = (1 if m >= 600_000 else 0) + (1 if m >= 1_500_000 else 0) \
            + int(max(0.0, m - 1_500_000) // 2_000_000)
        s["ops_finance"] = (1 if m >= 750_000 else 0) + int(m // 5_000_000)
    return s


def card_fees(amount: float, charges: float, pct: float) -> float:
    return amount * pct + charges * 0.30


# --------------------------------------------------------------------------
# 3. Simulation
# --------------------------------------------------------------------------

def simulate(a: A) -> dict:
    rows = []
    O = M = K = H = 0.0
    cash = a.founder_gift - a.continuity_reserve
    debt = 0.0
    drawn: list = []
    staff_prev: dict = {}
    mode, frozen = "normal", False
    streak, be_month = 0, None
    cum_def = peak_def = 0.0
    wind_down = None
    t12_in: list = []
    t12_gr: list = []
    declined = 0.0
    burns: list = []

    for t in range(a.months):
        v2 = t >= a.launch_v2
        g = a.growth_mult * (0.5 if mode == "ember" else 1.0)   # no GTM work in ember mode

        # ---------- casual organisers
        if t < a.launch_v1:
            ext = 10.0 if t >= 3 else 0.0                      # closed alpha: ~30 hosts
        else:
            early = min(t, 48) - a.launch_v1
            late = max(0, t - 48)
            ext = min(a.ext_org_cap, a.ext_org_at_launch * (1 + a.ext_org_growth) ** early
                      * (1 + a.ext_org_growth_late) ** late) * SEASON[t % 12]
        ext *= g
        # ---------- Halls
        new_halls = 0.0
        if v2:
            ext_h = min(a.ext_halls_cap, a.ext_halls_at_v2 * (1 + a.ext_halls_growth) ** (t - a.launch_v2))
            new_halls = (a.hall_from_org * O * a.conv_mult + ext_h) * g
        H = H * (1 - a.hall_churn) + new_halls
        hall_people = H * a.hall_new_people
        organic = a.organic_per_org * a.growth_mult * O + a.hall_host_rate * a.growth_mult * hall_people
        new_org = ext + organic
        O = O * a.org_retention + new_org
        touches = a.touches_per_org * O
        new_claims = a.claim_new_org * new_org + a.claim_per_touch * touches \
            + a.hall_claim_rate * hall_people
        M = M * (1 - a.member_churn) + new_claims

        # ---------- Keepers
        if t >= a.launch_v1:
            K = K * (1 - a.keeper_churn) + a.conv_mult * (
                a.keeper_new * new_claims + a.keeper_base * max(0.0, M - K))
        Km, Ka = K * (1 - a.annual_share), K * a.annual_share
        gross_keep = Km * a.price_monthly + Ka * a.price_annual / 12.0
        intl = a.intl_payer_share_v2 if v2 else 0.0
        vshare = a.vat_payer_share_v2 if v2 else 0.0
        pct = a.card_pct + intl * a.intl_extra_pct
        vat = gross_keep * vshare * a.vat_rate / (1 + a.vat_rate)
        fees = card_fees(gross_keep, Km + Ka / 12.0, pct) + gross_keep * a.refund_rate

        # ---------- Halls + institutions revenue
        paying_halls = H * (1 - a.hall_waiver)
        gross_halls = paying_halls * a.hall_price
        fees += card_fees(gross_halls, paying_halls, pct) + gross_halls * a.refund_rate
        vat += gross_halls * vshare * a.vat_rate / (1 + a.vat_rate) * 0.3   # most Halls B2B reverse charge
        insts = (M / a.members_per_institution) * min(1.0, (t - a.launch_v2 + 1) / 12) if v2 else 0.0
        gross_inst = insts * a.institution_price
        fees += min(gross_inst * a.ach_pct, insts * 5.0 / 12.0)
        gross = gross_keep + gross_halls + gross_inst
        op_rev = gross - fees - vat

        # ---------- costs
        afford = len(rows) >= 3 and sum(r["op_rev"] for r in rows[-3:]) >= 1.15 * sum(r["opex"] for r in rows[-3:])
        s = staffing(a, t, M, mode, afford)
        if mode == "normal" and staff_prev and not frozen:
            s = {r: max(n, staff_prev.get(r, 0)) for r, n in s.items()}   # no churn-and-burn of staff
        if frozen and mode == "normal":
            s = {r: min(n, staff_prev.get(r, 0)) if not r.startswith("ts_") else n
                 for r, n in s.items()}           # a freeze never freezes safety hiring
        staff = sum(n * loaded_monthly(r, t) for r, n in s.items())
        hires = sum(max(0.0, n - staff_prev.get(r, 0)) for r, n in s.items())
        staff += hires * HIRE_COST
        staff_prev = s
        fte = sum(s.values())
        variable = M * (a.infra_per_member + a.email_per_member
                        + (a.mind_share_v2 * a.mind_cost_per_user if v2 and mode != "ember" else 0.0)) \
            + (touches + hall_people * 4) * a.cost_per_touch
        mil = M / 1e6
        legal = (a.formation_legal / 3 if t < 3 else 0.0) + (a.counsel_v2 if v2 else a.counsel_v1) \
            + a.counsel_per_million * mil + (a.eu_uk_reps if v2 else 0.0)
        audits = (a.crypto_audit_prelaunch if t == a.launch_v1 - 1 else 0.0) \
            + (a.security_audit_annual if t > a.launch_v1 and (t - a.launch_v1) % 12 == 11 else 0.0) \
            + (a.covenant_audit_semiannual if t > a.launch_v1 and (t - a.launch_v1) % 6 == 5 else 0.0) \
            + (a.election_admin_annual if t >= 24 and t % 12 == 0 else 0.0)
        overhead = a.trust_admin + a.insurance + a.insurance_per_million * mil + a.accounting \
            + (a.infra_base_v2 if v2 else a.infra_base_v1) + (a.ts_tooling if t >= a.launch_v1 else 0.0) \
            + a.saas_per_fte * fte
        if mode == "ember":
            legal *= 0.6
            audits *= 0.5
        opex = staff + variable + legal + audits + overhead
        net = op_rev - opex

        # ---------- funding inflows, in sequence
        cut = a.shortfall_from is not None and t >= a.shortfall_from
        grants = 0.0
        for (mm, amt) in a.seed_grants + a.program_grants:
            if mm != t or cut:
                continue
            if t >= a.caps_from:
                tot = sum(t12_in[-11:]) + op_rev + amt
                if sum(t12_gr[-11:]) + amt > 0.25 * tot or amt > 0.10 * tot:
                    declined += amt
                    continue
            grants += amt
        patron = 0.0
        for (mm, amt) in a.patrons:
            if t >= mm:
                patron = amt
        if cut:
            patron *= 0.5
        founding = a.founding_keepers * 60.0 if t == a.launch_v1 else 0.0
        founding_net = founding - card_fees(founding, a.founding_keepers, a.card_pct)
        loan = 0.0
        for (mm, amt, gate, level) in a.pri:
            ok = M >= gate and M > 0 and K / M >= level
            if t == mm and not cut and ok:
                loan += amt
                debt += amt
                drawn.append(mm)
        debt_service = 0.0
        excess = cash + net - a.pri_reserve_months * opex
        if debt > 0 and net > 0 and excess > 0:
            debt_service = min(debt, a.pri_repay_share * min(excess, net))
            debt -= debt_service
        cash += net + grants + patron + founding_net + loan - debt_service
        t12_in.append(op_rev + grants + patron + founding)
        t12_gr.append(grants)

        # ---------- break-even bookkeeping
        if be_month is None:
            cum_def -= net
            peak_def = max(peak_def, cum_def)
        streak = streak + 1 if (net >= 0 and t >= a.launch_v1) else 0
        if streak >= 3 and be_month is None:
            be_month = t - 2

        # ---------- runway policy
        burns.append(max(1.0, opex + debt_service - op_rev - patron))
        burn = sum(burns[-3:]) / len(burns[-3:])
        sched = sum(amt for (mm, amt) in a.seed_grants + a.program_grants
                    if t < mm <= t + 6 and not (a.shortfall_from is not None and mm >= a.shortfall_from))
        sched += sum(amt for (mm, amt, gate, level) in a.pri
                     if t < mm <= t + 6 and mm not in drawn
                     and not (a.shortfall_from is not None and mm >= a.shortfall_from)
                     and M >= 0.5 * gate)
        runway = max(0.0, cash + sched) / burn
        if mode == "ember":
            # would the normal-mode team be affordable?  cost it before leaving ember
            sn = staffing(a, t, M, "normal", False)
            normal_staff = sum(n * loaded_monthly(r, t) for r, n in sn.items())
            normal_opex = opex - staff + normal_staff + (legal / 0.6 - legal) + (audits / 0.5 - audits)
            normal_burn = max(1.0, normal_opex + debt_service - op_rev - patron)
            n_runway = 99.0 if op_rev >= normal_opex else max(0.0, cash + sched) / normal_burn
            if n_runway > a.ember_exit_runway:
                mode = "normal"
        else:
            if net >= 0 or t < a.launch_v1 + 3:
                runway = 99.0
            if runway < a.ember_runway:
                mode = "ember"
        if cash < 0 and wind_down is None:
            wind_down = t
        frozen = runway < a.freeze_runway and mode == "normal"

        rows.append(dict(month=t, year=2027 + t // 12, moy=t % 12 + 1, mode=mode,
                         organisers=O, halls=H, claimed=M, keepers=K,
                         paying_share=K / M if M else 0.0, fte=fte,
                         rev_keepers=gross_keep, rev_halls=gross_halls, rev_inst=gross_inst,
                         fees=fees, vat=vat, op_rev=op_rev, staff=staff, variable=variable,
                         legal=legal, audits=audits, overhead=overhead, opex=opex, op_net=net,
                         grants=grants, patrons=patron, founding=founding, loan=loan,
                         debt_service=debt_service, debt=debt, cash=cash, runway=runway,
                         cum_def=cum_def))

    sal = sorted(SALARY.values())
    return dict(a=a, rows=rows, be=be_month, peak_def=peak_def, wind_down=wind_down,
                declined=declined, min_cash=min(r["cash"] for r in rows),
                pay_ratio=sal[-1] / sal[len(sal) // 2])


# --------------------------------------------------------------------------
# 4. Output
# --------------------------------------------------------------------------

def k(x: float) -> str:
    if abs(x) >= 1e6:
        return f"{x / 1e6:,.2f}M"
    if abs(x) >= 1e3:
        return f"{x / 1e3:,.0f}k"
    return f"{x:,.0f}"


def table(res: dict, until: int | None = None, every: int = 1) -> None:
    rows = res["rows"]
    last = len(rows) - 1 if until is None else min(until, len(rows) - 1)
    print("mo yyyy-mm mode   claimed  halls  pay%   fte  op_rev   opex   op_net  grants patron   "
          "loan debtSv    cash cum_def")
    for r in rows[: last + 1]:
        if r["month"] % every and r["month"] != last:
            continue
        print(f"{r['month']:>2} {r['year']}-{r['moy']:02d} {r['mode'][:6]:<6}{k(r['claimed']):>8}"
              f"{k(r['halls']):>7}{100 * r['paying_share']:>6.2f}{r['fte']:>5.1f}"
              f"{k(r['op_rev']):>8}{k(r['opex']):>7}{k(r['op_net']):>9}{k(r['grants']):>8}"
              f"{k(r['patrons']):>7}{k(r['loan']):>7}{k(r['debt_service']):>7}{k(r['cash']):>8}"
              f"{k(r['cum_def']):>8}")


def summary(res: dict) -> str:
    a, rows, be = res["a"], res["rows"], res["be"]
    end = be if be is not None else len(rows) - 1
    at = rows[end]
    tot = lambda key: sum(r[key] for r in rows[: end + 1])
    return "\n".join([
        f"scenario={a.name}",
        "  break-even (first of 3 consecutive months with operating revenue >= operating cost): "
        + (f"month {be} ({2027 + be // 12}-{be % 12 + 1:02d})" if be is not None
           else f"NOT within {a.months} months"),
        f"  build cost to sustainability = peak cumulative operating deficit: ${k(res['peak_def'])}",
        f"  at {'break-even' if be is not None else 'horizon'}: claimed {k(at['claimed'])}, Halls {k(at['halls'])}, "
        f"paying {100 * at['paying_share']:.2f}%, FTE {at['fte']:.1f}, opex ${k(at['opex'])}/mo, "
        f"op revenue ${k(at['op_rev'])}/mo",
        f"  inflows to then: founder ${k(a.founder_gift)} (of which ${k(a.continuity_reserve)} trust reserve), "
        f"grants ${k(tot('grants'))}, patrons ${k(tot('patrons'))}, founding pledges ${k(tot('founding'))}, "
        f"PRI loan ${k(tot('loan'))}",
        f"  min PBC cash ${k(res['min_cash'])}; cash<0 (wind-down trigger) "
        + (f"at month {res['wind_down']}" if res["wind_down"] is not None else "never")
        + f"; ember months {sum(r['mode'] == 'ember' for r in rows[: end + 1])}; "
          f"grants declined by deed caps ${k(res['declined'])}",
        f"  pay ratio highest/median salary {res['pay_ratio']:.2f} (deed cap 4.0)",
    ])


SCENARIOS = {
    "base": A(),
    "conv_half": A(name="conv_half", conv_mult=0.5),
    "growth_half": A(name="growth_half", growth_mult=0.5),
    "both": A(name="both", conv_mult=0.5, growth_mult=0.5),
    # Halls are ~half of revenue at break-even: halve Hall formation and outreach
    "halls_half": A(name="halls_half", hall_from_org=0.00075, ext_halls_cap=125.0, ext_halls_at_v2=10.0),
    # Phase 04's own revenue numbers ($4 suggested, Halls $12, no institutions) under 04b costs
    "p04_prices": A(name="p04_prices", price_monthly=3.75, price_annual=38.0, hall_price=12.0,
                    members_per_institution=1e15),
    # Phase 04's growth claim (1.2M claimed by month 36) needs roughly this much faster spread
    "p04_growth": A(name="p04_growth", org_retention=0.80, ext_org_at_launch=1_500.0),
}


def unit_costs() -> None:
    a = A()
    cols = [(10_000, False, "10K lean"), (1_000_000, False, "1M lean"), (1_000_000, True, "1M full"),
            (100_000_000, True, "100M full")]
    scales = [c[0] for c in cols]
    print("Cost per CLAIMED member per month, steady state, v2 features on (guests: 5 touches/member)")
    print("lean = pre-break-even staffing (no revenue-gated hires); full = all workload + growth hires")
    print(f"{'line item':<50}" + "".join(f"{c[2]:>12}" for c in cols))
    # (fixed $/mo, variable $/member/mo) per scale [ASSUME; see write-up (c) for the basis]
    raw = [
        ("Compute: API, relay, MLS delivery, workers", [(400, 0), (2_500, 0.0015), (60_000, 0.0008)]),
        ("Postgres metadata (HA, PITR backups)", [(350, 0), (1_800, 0.0012), (40_000, 0.0006)]),
        ("Object storage, ciphertext (200 MB @ $0.015/GB)", [(0, 0.003), (0, 0.003), (0, 0.0025)]),
        ("CDN, egress, request operations", [(50, 0.0003), (0, 0.0005), (0, 0.0003)]),
        ("Email + web push", [(20, 0.002), (0, 0.002), (0, 0.0012)]),
        ("Mind LLM (30% opt-in x $0.05; cap $0.10)", [(0, 0.015), (0, 0.015), (0, 0.010)]),
        ("Observability, 7-day logs, transparency log", [(150, 0), (800, 0.0003), (15_000, 0.0001)]),
        ("Guest page loads (5 x $0.0005)", [(0, 0.0025), (0, 0.0025), (0, 0.0020)]),
    ]
    items = [(nm, [sp[0], sp[1], sp[1], sp[2]]) for nm, sp in raw]
    infra = [0.0] * len(cols)
    for name, spec in items:
        vals = [spec[i][0] / n + spec[i][1] for i, n in enumerate(scales)]
        infra = [x + y for x, y in zip(infra, vals)]
        print(f"{name:<50}" + "".join(f"{'$%.4f' % v:>12}" for v in vals))
    print(f"{'= infrastructure subtotal':<50}" + "".join(f"{'$%.4f' % v:>12}" for v in infra))
    ftes = [staffing(a, 36, n, "normal", aff) for n, aff, _ in cols]
    ts, other, fixed = [], [], []
    for n, f in zip(scales, ftes):
        ts.append(sum(v * loaded_monthly(r, 36) for r, v in f.items() if r.startswith("ts_")) / n)
        other.append(sum(v * loaded_monthly(r, 36) for r, v in f.items() if not r.startswith("ts_")) / n)
        scale = 1 + n / 20e6
        legal = a.counsel_v2 + a.counsel_per_million * n / 1e6 + a.eu_uk_reps \
            + (a.security_audit_annual + 2 * a.covenant_audit_semiannual + a.election_admin_annual) / 12 * scale
        fixed.append((legal + a.trust_admin + a.insurance + a.insurance_per_million * n / 1e6
                      + a.accounting * scale + a.infra_base_v2) / n)
    for name, vals in (("Trust & safety staff (workload-sized, in-house)", ts),
                       ("Other staff (eng, design, support, ops)", other),
                       ("Legal, compliance, audits, insurance, trust", fixed)):
        print(f"{name:<50}" + "".join(f"{'$%.4f' % v:>12}" for v in vals))
    total = [infra[i] + ts[i] + other[i] + fixed[i] for i in range(len(cols))]
    print(f"{'= FULLY LOADED':<50}" + "".join(f"{'$%.4f' % v:>12}" for v in total))
    print(f"{'FTE':<50}" + "".join(f"{sum(f.values()):>12.0f}" for f in ftes))
    # steady-state revenue per claimed member under base assumptions
    share = 0.032 * 0.025 / 0.04 + 0.0003 / 0.04 * 0.97      # zero-growth steady state
    keep = share * ((1 - a.annual_share) * a.price_monthly + a.annual_share * a.price_annual / 12)
    rev = keep * 0.93 + (1 / 250) * 0.8 * a.hall_price * 0.93 + a.institution_price / a.members_per_institution
    print(f"{'Net revenue per member (steady state, ~2.8% paying, 1 Hall/250)':<50}"
          + "".join(f"{'$%.4f' % rev:>12}" for _ in scales))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", default="base", choices=list(SCENARIOS) + ["shortfall"])
    p.add_argument("--all", action="store_true")
    p.add_argument("--unit", action="store_true")
    p.add_argument("--every", type=int, default=1)
    p.add_argument("--csv")
    args = p.parse_args()
    if args.unit:
        unit_costs()
        return
    base = simulate(SCENARIOS["base"])
    half = (base["be"] or 60) // 2
    if args.all:
        bar = "=" * 108
        print(bar + "\nBASE CASE: month by month, month 0 to break-even + 3\n" + bar)
        table(base, until=(base["be"] or 116) + 3)
        print("\n" + summary(base) + "\n")
        print(bar + "\nSENSITIVITY (same funding plan and runway policy)\n" + bar)
        for key in ("conv_half", "growth_half", "both", "halls_half"):
            print(summary(simulate(SCENARIOS[key])) + "\n")
        print(bar + "\nUNCONSTRAINED NEED (runway policy off: what each world would cost to reach break-even)\n" + bar)
        for key in ("base", "conv_half", "growth_half", "both", "halls_half"):
            r = simulate(replace(SCENARIOS[key], months=180, freeze_runway=-1, ember_runway=-1))
            be = r["be"]
            print(f"  {key:<12} break-even {'month ' + str(be) if be is not None else 'none in 180 months':<22}"
                  f" peak cumulative operating deficit ${k(r['peak_def']):>7}   min cash ${k(r['min_cash'])}")
        print("\n" + bar + f"\nHALFWAY SHORTFALL: from month {half} every grant and the PRI fail; patrons halve\n" + bar)
        sf = simulate(replace(SCENARIOS["base"], name=f"shortfall_m{half}", shortfall_from=half))
        print(summary(sf) + "\n")
        table(sf, until=(sf["be"] or 116) + 3, every=3)
        print("\n" + bar + "\nRECONCILIATION WITH PHASE 04\n" + bar)
        for key in ("p04_prices", "p04_growth"):
            print(summary(simulate(SCENARIOS[key])) + "\n")
        g = simulate(SCENARIOS["p04_growth"])
        print(f"  p04_growth claimed members at month 36: {k(g['rows'][36]['claimed'])} (P04 assumed 1.2M)")
        print(f"  base claimed members at month 12/24/36: {k(base['rows'][12]['claimed'])} / "
              f"{k(base['rows'][24]['claimed'])} / {k(base['rows'][36]['claimed'])} (P04 assumed 50k / 400k / 1.2M)")
        return
    a = SCENARIOS.get(args.scenario) or replace(SCENARIOS["base"], name="shortfall", shortfall_from=half)
    res = simulate(a)
    table(res, until=(res["be"] or 116) + 3, every=args.every)
    print("\n" + summary(res))
    if args.csv:
        with open(args.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(res["rows"][0]))
            w.writeheader()
            w.writerows(res["rows"])


if __name__ == "__main__":
    main()
