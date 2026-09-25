# Rebuild v2: operator is the purpose-trust-controlled nonprofit (one ledger; grants & deductible gifts are lawful operating income).
import sys
from rebuild import cum_A
def run(conv=0.015, growth=0.7, active=0.6, org_ratio=1.0, org_net=30, inst_final=1000, inst_net=200, var=0.025,
        staff_cost=175_000, bridge=1_500_000, grants=True, major=True, horizon=144, keeper_net=3.40, grant_scale=1.0, major_scale=1.0):
    cash=0; debt=0; rows=[]; first_neg=None
    for m in range(horizon+1):
        A=cum_A(m,growth)*active
        c=0 if m<9 else (conv*min(1,(m-9)/24+0.5))
        K=A*c
        orgs=0 if m<10 else max(min(40,4*(m-9)), org_ratio*A/1000)
        inst=0 if m<24 else inst_final*min(1,((m-24)/60))**1.3
        earned=K*keeper_net+orgs*org_net+inst*inst_net
        # grants: seed 0.1M/qtr M3-M12, then 0.25M/qtr M12-M60, then 0.125M/qtr (declining, never assumed permanent)
        g=0
        if grants:
            if 3<=m<12 and m%3==0: g=100_000
            elif 12<=m<=60 and m%3==0: g=250_000
            elif m>60 and m%3==0: g=125_000
            g*=grant_scale
        # major gifts (Signal-style large donors), annual, capped at 25% of the year's inflow by policy
        mg=0
        if major and m>=12 and m%12==0: mg=min(2_000_000, 250_000*(m//12))*major_scale
        vc=A*var
        staff=4 if m<7 else 6 if A<50_000 else 9 if A<300_000 else 14 if A<1_500_000 else 20 if A<4_000_000 else 28 if A<10_000_000 else 36
        other=20_000 if m<7 else 30_000 if A<50_000 else 45_000 if A<300_000 else 70_000 if A<1_500_000 else 100_000 if A<4_000_000 else 140_000 if A<10_000_000 else 190_000
        one={0:60_000,1:60_000,2:40_000,10:120_000}.get(m,0)
        if m>=22 and m%12==10: one+=120_000
        opex=vc+staff*staff_cost/12+other+one
        inflow=0
        if m==0: inflow+=500_000
        if m==3: inflow+=bridge; debt+=bridge
        cash+=earned+g+mg-opex+inflow-debt*0.01/12
        if first_neg is None and cash<0: first_neg=m
        mg_ann=(min(2_000_000,250_000*(m//12))*major_scale if (major and m>=12) else 0)
        rows.append((m,A,c,K,orgs,inst,earned,g,mg,opex,staff,cash,mg_ann))
    def first_sust(f):
        for i in range(13,len(rows)-12):
            if all(f(rows[j]) for j in range(i,i+12)): return i
    self_suff=first_sust(lambda r: r[6]>=r[9])                       # earned revenue alone covers opex
    donor_sust=first_sust(lambda r: r[6]+r[12]/12>=r[9])  # earned + major gifts (annualised) cover opex
    return rows,first_neg,self_suff,donor_sust
def summary(label,**kw):
    rows,fn,ss,ds=run(**kw)
    mc=min(r[11] for r in rows); mm=[r[0] for r in rows if r[11]==mc][0]
    f=lambda i:(f"M{i} ({rows[i][1]/1e6:.2f}M active)" if i else "none<=M132")
    print(f"{label:44s} earned-only={f(ss):22s} earned+major={f(ds):22s} mincash={mc/1e6:6.2f}M@M{mm} cash<0={fn}")
if __name__=="__main__":
    if len(sys.argv)>1:
        rows,*_=run()
        for r in rows:
            if (r[0]<=24 and r[0]%3==0) or r[0]%12==0:
                m,A,c,K,o,i,e,g,mg,opex,st,cash,_=r
                print(f"| {m} | {A:,.0f} | {c*100:.2f}% | {K:,.0f} | {o:,.0f} | {i:,.0f} | {e/1e3:,.0f} | {(g+mg)/1e3:,.0f} | {st} | {opex/1e3:,.0f} | {cash/1e3:,.0f} |")
        sys.exit()
    summary("BASE")
    summary("conv 0.75%",conv=0.0075)
    summary("conv 3%",conv=0.03)
    summary("institutions 500",inst_final=500)
    summary("institutions 0",inst_final=0)
    summary("growth 0.5x",growth=0.5)
    summary("growth 1.0x",growth=1.0)
    summary("grants halved",grant_scale=0.5)
    summary("major gifts halved",major_scale=0.5)
    summary("no major gifts",major=False)
    summary("no bridge loan",bridge=0)
    summary("staff $210k",staff_cost=210_000)
    summary("var x2",var=0.05)
    summary("downside: conv .75, inst 500, growth .5, grants .5",conv=0.0075,inst_final=500,growth=0.5,grant_scale=0.5)
