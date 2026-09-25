#!/usr/bin/env python3
"""Phase 05 red team: the ORIGINAL funding model (../model.py, unmodified) run under attack assumptions.

    python3 attack_runs.py

Every scenario is a dataclasses.replace() of the original base case, so the only thing that changes is the
assumption named.  One scenario (A7) monkeypatches the staffing function to add the engineers the v1/v2 scope
needs; the original function is restored afterwards.
"""
from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model as M  # noqa: E402

BASE = M.A()


def line(name: str, res: dict, note: str) -> None:
    rows = res["rows"]
    be = res["be"]
    wd = res["wind_down"]
    c36 = rows[36]["claimed"]
    print(f"{name:<34} break-even {('m' + str(be)) if be is not None else 'none/120':<9} "
          f"cash<0 at {('m' + str(wd)) if wd is not None else 'never':<6} min cash {M.k(res['min_cash']):>7}  "
          f"peak deficit {M.k(res['peak_def']):>6}  claimed m36 {M.k(c36):>5}  PRI drawn "
          f"{M.k(sum(r['loan'] for r in rows)):>5}\n    {note}")


def run(name: str, a: M.A, note: str) -> dict:
    r = M.simulate(a)
    line(name, r, note)
    return r


print("=" * 118)
print("ORIGINAL MODEL, ATTACK ASSUMPTIONS (one change each unless stated)")
print("=" * 118)
run("A0 base (as published)", BASE, "reproduces run-3-operational.md (b).4")
run("A1 no PRI #1 (no lender at m12)", replace(BASE, name="no_pri1", pri=((36, 1_250_000, 30_000, 0.02),)),
    "the $1.25M zero-interest, forgivable, unsecured PRI has no named lender; operating revenue at m12 is $485/month")
run("A2 no PRIs at all", replace(BASE, name="no_pri", pri=()), "")
run("A3 grants halved", replace(BASE, name="grants_half",
    seed_grants=tuple((m, a / 2) for m, a in BASE.seed_grants),
    program_grants=tuple((m, a / 2) for m, a in BASE.program_grants)), "NGI Zero closed; a PBC is ineligible for most foundation money")
run("A4 zero-budget acquisition grows 3%/mo", replace(BASE, name="ext3", ext_org_growth=0.03),
    "base assumes non-viral acquisition compounds 7%/mo for 42 months with NO marketing line in opex")
run("A5 Halls: only 40% pay", replace(BASE, name="halls40", hall_waiver=0.60),
    "Luma, Meetup groups, WhatsApp Communities, Heylo, Strava clubs are free or bundled; base assumes 80% of Halls pay from day one")
run("A6 Hall attendees 3/mo not 8", replace(BASE, name="hallpeople3", hall_new_people=3.0),
    "base: every Hall brings 8 brand-new people a month, forever; Halls are the main claim engine after m36")
_orig_staffing = M.staffing


def staffing_plus_eng(a, month, m, mode, afford=True):
    s = _orig_staffing(a, month, m, mode, afford)
    if mode != "ember":
        s["eng_mid"] = s.get("eng_mid", 0) + (1 if month >= 0 else 0) + (1 if month >= 9 else 0)
    return s


M.staffing = staffing_plus_eng
run("A7 +2 engineers for the v1/v2 scope", replace(BASE, name="eng_plus2"),
    "v1+v2 = HPKE web E2EE, passkey-PRF, DAP counters, transparency log, MLS Tables, ActivityPub/AT Halls, mind, EU/UK "
    "launch, open spec: base staffs it with 1 senior + 1 security engineer")
M.staffing = _orig_staffing
run("A8 T&S reports 3x (0.0018/member)", replace(BASE, name="ts3x", reports_per_member=0.0018),
    "guests (8 touches/organiser) can report; phishing-style plan covers; NCII desk")
run("A9 Keepers 1.6% of new claims", replace(BASE, name="keep_half_new", keeper_new=0.016),
    "a tool used a few times a year; Apple Invites creation is bundled in iCloud+ from $0.99/mo")
run("A10 month-14 starvation: no PRI#1 + grants half",
    replace(BASE, name="m14", pri=((36, 1_250_000, 30_000, 0.02),),
            seed_grants=tuple((m, a / 2) for m, a in BASE.seed_grants),
            program_grants=tuple((m, a / 2) for m, a in BASE.program_grants)), "")
honest = replace(BASE, name="honest", ext_org_growth=0.045, hall_waiver=0.45, hall_new_people=5.0,
                 keeper_new=0.024, reports_per_member=0.0012, pri=())
M.staffing = staffing_plus_eng
r = run("A11 'honest middle' (all moderate, no PRIs)", honest,
        "ext growth 4.5%/mo, 55% of Halls pay, 5 new Hall attendees/mo, Keepers 2.4% of new claims, T&S 2x, +2 eng, no PRIs")
u = M.simulate(replace(honest, months=180, freeze_runway=-1, ember_runway=-1))
M.staffing = _orig_staffing
print(f"    unconstrained (runway policy off, 180 months): break-even "
      f"{('m' + str(u['be'])) if u['be'] is not None else 'none'}; peak cumulative deficit ${M.k(u['peak_def'])}")
