# Red-team variants of the Phase 04b funding model (copies; originals untouched).
from model import run
def sim(overrun=0, anchor=3_000_000, grants_to_pbc=True, fdn_offset=True, staff_add=None, conv_final=0.03,
        org_ratio=1.5, var=0.045, growth_mult=1.0, active_share=1.0, pri=True, horizon=120):
    rows,_,_ = run(horizon=horizon, var=var, org_ratio=org_ratio, conv_final=conv_final, growth_mult=growth_mult)
    cash=0; debt=0; out=[]; first_neg=None; fdn=[0]
    for r in rows:
        m,A=r[0],r[1]
        Aa=A*active_share
        # recompute revenue on ACTIVE account-holders (conversion & orgs scale with active base; variable cost too)
        k=Aa*r[2]; o=max(min(60,5*(m-9)) if m>=10 else 0, org_ratio*Aa/1000)
        rev=k*(3.60 if m<19 else 3.40)+o*38
        vc=Aa*var
        fixed=r[8]+r[9]
        if staff_add: fixed+=staff_add(m,A)*175_000/12
        net=rev-vc-fixed-(overrun if m==1 else 0)
        inflow=0
        if m==0: inflow+=500_000
        if m==2: inflow+=anchor; debt+=anchor
        if pri and m==24: inflow+=4_000_000; debt+=4_000_000
        if pri and m==42: inflow+=5_000_000; debt+=5_000_000
        g=0
        if 3<=m<=12 and m%3==0: g+=100_000
        if 12<=m<=48 and m%3==0: g+=250_000
        if m>=18 and m%12==6: g+=300_000
        if grants_to_pbc: inflow+=g
        elif fdn_offset:
            # Foundation absorbs only work it genuinely owns (2 FTE spec from M3, 3 FTE spec+research from M24),
            # and only while its own ledger (grants+donations, less 10% sponsor/overhead) can pay for them.
            fdn[0]+=g*0.9
            fte = 0 if m<3 else (2 if m<24 else 3)
            off=min(fte*175_000/12, max(fdn[0],0)); fdn[0]-=off; net+=off
        cash+=net+inflow-debt*0.01/12
        if first_neg is None and cash<0: first_neg=m
        out.append((m,A,Aa,rev,fixed,net,cash))
    sbe=None
    for i in range(13,len(out)-12):
        if all(out[j][5]>=0 for j in range(i,i+12)): sbe=i;break
    return out,first_neg,sbe
def show(label,**kw):
    out,fn,sbe=sim(**kw)
    mc=min(o[6] for o in out); mm=[o[0] for o in out if o[6]==mc][0]
    print(f"{label:78s} cash<0 at M{fn}  lowest {mc/1e6:6.2f}M @M{mm}  sustainedBE={'M'+str(sbe) if sbe else 'none<=M108'}")
realistic = lambda m,A: (0 if m<13 else (5 if A<120_000 else 7))   # crews/MLS, native shells, 24/7 T&S, Ireland ops
show("04b BASE (as published)")
show("R1 grants/donations kept in Commons Fdn (only 2-3 FTE of genuine offset)", grants_to_pbc=False)
show("R2 anchor loan $2.0M not $3.0M", anchor=2_000_000)
show("R3 R1 + R2", grants_to_pbc=False, anchor=2_000_000)
show("R4 R3 + realistic v2 staffing (+5 FTE at M13, +7 from 120k A)", grants_to_pbc=False, anchor=2_000_000, staff_add=realistic)
show("R5 R1 + realistic staffing (anchor $3M)", grants_to_pbc=False, staff_add=realistic)
show("R6 R5 + only 60% of account-holders active", grants_to_pbc=False, staff_add=realistic, active_share=0.6)
show("R7 R6 + conversion 1.5% (Guardian-grade base rate)", grants_to_pbc=False, staff_add=realistic, active_share=0.6, conv_final=0.015)
show("R8 R7 + PRIs never arrive", grants_to_pbc=False, staff_add=realistic, active_share=0.6, conv_final=0.015, pri=False)
show("R4b R4 + formation legal/trademark overrun of $160k (rename likely)", grants_to_pbc=False, anchor=2_000_000, staff_add=realistic, overrun=160_000)
