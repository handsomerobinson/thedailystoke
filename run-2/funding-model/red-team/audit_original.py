#!/usr/bin/env python3
"""
Phase 05 red team -- audit of run-2/funding-model/model.py.

Re-implements the original model's mechanics exactly (verified: the
'as_published' row reproduces break-even month 71 and $1,594,179), then
applies corrections ONE AT A TIME, cumulatively, so each step's effect on
the headline is visible. Stdlib only. Run: python3 audit_original.py

Every correction constant is labelled with its evidence:
  [VERIFIED 2026] = checked by live web search this session (see
                    run-2-design-final.md, Appendix B sources)
  [INTERNAL]      = taken from the design's own documents (inconsistency)
  [ASSUMPTION]    = red-team estimate, stated so it can be argued with
"""
from dataclasses import dataclass, replace
import math

@dataclass(frozen=True)
class P:
    months: int = 90
    seed_users: int = 250
    g0: float = 0.42
    g_decay: float = 0.965
    g_floor: float = 0.045
    acct_churn: float = 0.02
    conv: float = 0.05
    paid_churn: float = 0.035
    price: float = 6.0
    infra_per_user: float = 0.15
    infra_fixed: float = 600
    fee_pct: float = 0.029
    fee_fixed: float = 0.30
    vat_share: float = 0.22
    vat: float = 0.20
    agever_cost: float = 0.35
    asaa_share: float = 0.12
    legal_monthly: float = 3700
    legal_once: float = 45000
    founder_cap: float = 150_000
    patron: float = 55_000
    loan_cap: float = 1_450_000
    buffer: float = 15_000
    loan_rate_m: float = 0.0025
    # --- red-team correction switches ---
    interest_paid_in_cash: bool = False     # original capitalises interest silently
    count_unfunded_deficit: bool = False    # original lets cash go negative uncounted
    ts_floor_scaling: bool = False          # deed floor: 1 T&S FTE / 50k active rooms
    support_scaling: bool = False           # 1 support FTE per 150k users
    eng_scaling: bool = False               # web+iOS+Android+backend+crypto+SRE
    storage_growth: bool = False            # media accrues with tenure
    legal_realistic: bool = False
    app_store_share: float = 0.0            # share of payers billed via IAP
    app_store_fee: float = 0.15
    mind_cost_per_mind_user: float = 0.0    # LLM $ per mind user / month
    mind_adoption: float = 0.0
    loaded: float = 1.28

def team_cost(p: P, m: int, users: float) -> tuple[float, float]:
    """Returns (monthly loaded cost, headcount)."""
    L = p.loaded / 12
    cost = 2 * 70_000 * L  # founders (original: below-market, forever)
    heads = 2
    plan = [(12, 125_000), (18, 78_000), (24, 125_000), (30, 95_000)]
    for mm, sal in plan:
        if m >= mm:
            cost += sal * L; heads += 1
    if p.ts_floor_scaling:
        # [INTERNAL] run-2-operational.md (d): "1 FTE per 50,000 active rooms",
        # deed-mandated. [ASSUMPTION] active rooms ~= 0.25 x users.
        need = math.ceil(users * 0.25 / 50_000)
        extra = max(0, need - 1)          # 1 T&S already in plan
        cost += extra * 78_000 * L; heads += extra
    if p.support_scaling:
        extra = math.floor(users / 150_000)
        cost += extra * 60_000 * L; heads += extra
    if p.eng_scaling:
        # [ASSUMPTION] an E2E, 3-client (web/iOS/Android) product with a CSAM
        # hash pipeline, key recovery, reproducible builds and an oEmbed proxy
        # needs >=3 more engineers by month 18 and one per ~400k users after
        # (SRE/security); $165k is a modest US market rate for crypto/mobile.
        extra = (3 if m >= 18 else 0) + math.floor(users / 400_000)
        cost += extra * 165_000 * L; heads += extra
    return cost, heads

def run(p: P):
    users = 0.0; paying = 0.0; cash = 0.0; loan = 0.0; g = p.g0
    stored_gb = 0.0
    capital_in = 0.0; unfunded = 0.0
    rows = []
    for m in range(p.months):
        new = p.seed_users if m == 0 else users * g
        users = int(users * (1 - p.acct_churn) + new)
        g = max(p.g_floor, g * p.g_decay)
        paying = paying * (1 - p.paid_churn) + new * p.conv
        gross = paying * p.price
        fees = gross * p.fee_pct + paying * p.fee_fixed
        store = gross * p.app_store_share * p.app_store_fee
        vat = gross * p.vat_share * p.vat
        rev = gross - fees - vat - store
        infra = users * p.infra_per_user + p.infra_fixed
        if p.storage_growth:
            # [ASSUMPTION] each active free user adds 0.25 GB/month of
            # encrypted media, each payer 3 GB/month (the $6 tier sells 1 TB);
            # nothing is deleted. [VERIFIED 2026] B2 $6.95/TB-month used
            # (cheapest mainstream; S3 Standard is $23/TB) + 1 replica.
            stored_gb = stored_gb * (1 - p.acct_churn) + users * 0.25 + paying * 3.0
            infra += stored_gb * 0.00695 * 2
        tc, heads = team_cost(p, m, users)
        legal = p.legal_monthly + (p.legal_once if m == 0 else 0)
        if p.legal_realistic:
            # [ASSUMPTION, itemised in the final doc section 9]: outside counsel
            # across GDPR/DSA/OSA/COPPA/state age laws ~$9k/mo; EU+UK Art.27
            # representatives ~$1.5k/mo; trustee + protector fees ~$3k/mo;
            # D&O + cyber + E&O insurance ~$2.5k/mo; annual financial audit
            # (promised public P&L) + annual independent code audit
            # (promised in proof plan) ~$120k/yr = $10k/mo from month 12.
            legal += 9000 + 1500 + 3000 + 2500 + (10_000 if m >= 12 else 0) - p.legal_monthly
        agever = new * p.asaa_share * p.agever_cost
        mind = users * p.mind_adoption * p.mind_cost_per_mind_user
        interest = loan * p.loan_rate_m
        cost = infra + tc + legal + agever + mind + (interest if p.interest_paid_in_cash else 0)
        net = rev - cost
        inflow = (p.founder_cap if m == 0 else 0) + (p.patron if m == 2 else 0)
        capital_in += inflow
        cash += inflow + net
        if not p.interest_paid_in_cash:
            loan *= (1 + p.loan_rate_m)
        if cash < p.buffer:
            draw = min(p.buffer - cash, max(0.0, p.loan_cap - loan))
            loan += draw; cash += draw; capital_in += draw
        if p.count_unfunded_deficit and cash < p.buffer:
            gap = p.buffer - cash      # somebody has to put this money in
            unfunded += gap; cash += gap
        rows.append(dict(m=m, users=users, paying=paying, rev=rev, cost=cost, net=net,
                         loan=loan, cash=cash, heads=heads, capital=capital_in + unfunded,
                         unfunded=unfunded))
    return rows

def breakeven(rows):
    s = 0
    for r in rows:
        s = s + 1 if r["rev"] >= r["cost"] else 0
        if s >= 3:
            return r["m"] - 2
    return None

def summarize(name, p):
    rows = run(p)
    be = breakeven(rows)
    end = rows[be] if be is not None else rows[-1]
    worst_cash = min(r["cash"] for r in rows)
    last = rows[-1]
    print(f"{name:<58} BE={str(be):>4}  capital-to-BE/end=${end['capital']:>11,.0f}  "
          f"unfunded=${end['unfunded']:>10,.0f}  min_cash=${worst_cash:>11,.0f}  "
          f"m89 rev/cost={last['rev']:>9,.0f}/{last['cost']:>9,.0f} heads={last['heads']}")
    return rows

if __name__ == "__main__":
    base = P()
    steps = [
        ("0 as published (reproduces model.py)", base),
        ("1 +count unfunded cash deficit", replace(base, count_unfunded_deficit=True)),
        ("2 +interest paid in cash, not capitalised", None),
        ("3 +T&S floor per the deed (1 FTE/50k rooms)", None),
        ("4 +support scaling (1 FTE/150k users)", None),
        ("5 +engineering realism (3 clients, E2E, SRE)", None),
        ("6 +legal/insurance/audit realism", None),
        ("7 +media storage accrues (B2 $6.95/TB x2)", None),
        ("8 +30% of payers via app-store IAP at 15%", None),
        ("9 +mind LLM cost ($0.60/mo, 25% adoption)", None),
        ("10 +paid churn 8%/mo (RevenueCat-anchored)", None),
        ("11 +conversion 2.2% (RevenueCat freemium median)", None),
    ]
    cur = base
    mods = [
        dict(count_unfunded_deficit=True),
        dict(interest_paid_in_cash=True),
        dict(ts_floor_scaling=True),
        dict(support_scaling=True),
        dict(eng_scaling=True),
        dict(legal_realistic=True),
        dict(storage_growth=True),
        dict(app_store_share=0.30),
        dict(mind_cost_per_mind_user=0.60, mind_adoption=0.25),
        dict(paid_churn=0.08),
        dict(conv=0.022),
    ]
    summarize(steps[0][0], base)
    for (name, _), mod in zip(steps[1:], mods):
        cur = replace(cur, **mod)
        summarize(name, cur)
    print()
    print("Isolated single corrections applied to the ORIGINAL (one at a time):")
    for name, mod in [("paid churn 8%/mo only", dict(paid_churn=0.08, count_unfunded_deficit=True)),
                      ("conversion 2.2% only", dict(conv=0.022, count_unfunded_deficit=True)),
                      ("T&S deed floor only", dict(ts_floor_scaling=True, count_unfunded_deficit=True)),
                      ("storage accrual only", dict(storage_growth=True, count_unfunded_deficit=True)),
                      ("mind LLM cost only", dict(mind_cost_per_mind_user=0.60, mind_adoption=0.25, count_unfunded_deficit=True)),
                      ("legal realism only", dict(legal_realistic=True, count_unfunded_deficit=True))]:
        summarize(name, replace(base, **mod))
    # debt-service check on the as-published baseline
    rows = run(replace(base, count_unfunded_deficit=True))
    r = rows[71]
    print(f"\nAt published break-even (m71): monthly surplus ${r['net']:,.0f} vs interest on "
          f"${r['loan']:,.0f} loan = ${r['loan']*base.loan_rate_m:,.0f}/mo -> surplus does not cover interest.")
