# Phase 05 rebuilt funding model: two ledgers (PBC operations vs Commons Foundation), active users, lean scope.
import sys
ANCH=[(0,0),(6,300),(12,10_000),(18,40_000),(24,120_000),(30,300_000),(36,600_000),(48,1_800_000),(60,3_800_000),(72,6_500_000),(84,10_000_000),(96,14_000_000),(120,22_000_000)]
def cum_A(m,g):
    t=m*g
    for (m0,a0),(m1,a1) in zip(ANCH,ANCH[1:]):
        if t<=m1:
            if a0==0: return a1*(t-m0)/(m1-m0)
            return a0*(a1/a0)**((t-m0)/(m1-m0))
    return ANCH[-1][1]
def run(conv=0.015, growth=0.7, active=0.6, org_ratio=1.0, org_net=30, inst_final=1000, inst_net=200, var=0.025,
        staff_cost=175_000, anchor=1_500_000, pri=True, horizon=144, keeper_net=3.40, verbose=False, inst_start=24):
    cash=0; debt=0; fdn=0; rows=[]; first_neg=None; peak=0; cum=0
    for m in range(horizon+1):
        A=cum_A(m,growth)*active
        c=0 if m<9 else (conv*min(1,(m-9)/24+0.5))           # ramps from half to full conversion over 2 years
        K=A*c
        orgs=0 if m<10 else max(min(40,4*(m-9)), org_ratio*A/1000)
        inst=0 if m<inst_start else inst_final*min(1,((m-inst_start)/60))**1.3
        rev=K*keeper_net+orgs*org_net+inst*inst_net
        vc=A*var
        staff=4 if m<7 else 6 if A<50_000 else 9 if A<300_000 else 14 if A<1_500_000 else 20 if A<4_000_000 else 28 if A<10_000_000 else 36
        other=20_000 if m<7 else 30_000 if A<50_000 else 45_000 if A<300_000 else 70_000 if A<1_500_000 else 100_000 if A<4_000_000 else 140_000 if A<10_000_000 else 190_000
        one={0:60_000,1:60_000,2:40_000,10:120_000}.get(m,0)     # staged formation (Fdn+PBC shell), smaller crypto audit (no MLS in v1)
        if m>=22 and m%12==10: one+=120_000                       # annual audit
        net=rev-vc-staff*staff_cost/12-other-one
        cum+=net; peak=min(peak,cum)
        inflow=0
        if m==0: inflow+=500_000
        if m==3: inflow+=anchor; debt+=anchor
        if pri and m==30: inflow+=3_000_000; debt+=3_000_000
        if pri and m==54: inflow+=4_000_000; debt+=4_000_000
        cash+=net+inflow-debt*0.01/12
        if first_neg is None and cash<0: first_neg=m
        rows.append((m,A,c,K,orgs,inst,rev,vc,staff,net,inflow,cash))
    sbe=None
    for i in range(13,len(rows)-12):
        if all(rows[j][9]>=0 for j in range(i,i+12)): sbe=i;break
    return rows,first_neg,sbe,peak
def summary(label,**kw):
    rows,fn,sbe,peak=run(**kw)
    mc=min(r[11] for r in rows); mm=[r[0] for r in rows if r[11]==mc][0]
    a=rows[sbe][1]/1e6 if sbe else 0
    print(f"{label:52s} sustBE={('M'+str(sbe)) if sbe else 'none<=M132':10s} activeA@BE={a:5.2f}M peakDeficit={-peak/1e6:5.1f}M mincash={mc/1e6:6.2f}M@M{mm} cash<0={fn}")
if __name__=="__main__":
    if len(sys.argv)>1:
        rows,fn,sbe,peak=run()
        for r in rows:
            if r[0]<=24 and r[0]%3==0 or r[0]%6==0:
                m,A,c,K,o,i,rev,vc,st,net,inf,cash=r
                print(f"| {m} | {A:,.0f} | {c*100:.2f}% | {K:,.0f} | {o:,.0f} | {i:,.0f} | {rev/1e3:,.0f} | {vc/1e3:,.1f} | {st} | {net/1e3:,.0f} | {inf/1e3:,.0f} | {cash/1e3:,.0f} |")
        sys.exit()
    summary("REBUILD BASE")
    summary("conv 0.75%",conv=0.0075)
    summary("conv 3%",conv=0.03)
    summary("institutions 500 not 1000",inst_final=500)
    summary("institutions 0",inst_final=0)
    summary("growth 0.5x",growth=0.5)
    summary("growth 1.0x (04b speed)",growth=1.0)
    summary("PRIs never arrive",pri=False)
    summary("anchor $0.75M",anchor=750_000)
    summary("var x2",var=0.05)
    summary("staff $210k",staff_cost=210_000)
    summary("combined: conv .75%, inst 500, growth .5",conv=0.0075,inst_final=500,growth=0.5)
