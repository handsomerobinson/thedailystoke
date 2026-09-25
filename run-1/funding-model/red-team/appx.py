ANCH=[(0,0),(6,300),(12,10_000),(18,40_000),(24,120_000),(30,300_000),(36,600_000),(48,1_800_000),
      (60,3_800_000),(72,6_500_000),(84,10_000_000),(96,14_000_000),(120,22_000_000)]
def cum_A(m,g):                      # 04b anchors, time stretched by growth multiplier g
    t=m*g
    for (m0,a0),(m1,a1) in zip(ANCH,ANCH[1:]):
        if t<=m1:
            return a1*(t-m0)/(m1-m0) if a0==0 else a0*(a1/a0)**((t-m0)/(m1-m0))
    return ANCH[-1][1]
def run(conv=0.015, growth=0.7, active=0.6, org_ratio=1.0, org_net=30, inst_final=1000, inst_net=200,
        var=0.025, staff_cost=175_000, bridge=1_500_000, grant_scale=1.0, major_scale=1.0, horizon=144):
    cash=debt=0; rows=[]
    for m in range(horizon+1):
        A=cum_A(m,growth)*active                                   # ACTIVE host keys
        c=0 if m<9 else conv*min(1,(m-9)/24+0.5)
        orgs=0 if m<10 else max(min(40,4*(m-9)), org_ratio*A/1000)
        inst=0 if m<24 else inst_final*min(1,(m-24)/60)**1.3
        earned=A*c*3.40+orgs*org_net+inst*inst_net
        g=(100_000 if 3<=m<12 else 250_000 if 12<=m<=60 else 125_000)*grant_scale if (m>=3 and m%3==0) else 0
        mg=min(2_000_000,250_000*(m//12))*major_scale if (m>=12 and m%12==0) else 0
        staff=(4 if m<7 else 6 if A<50e3 else 9 if A<300e3 else 14 if A<1.5e6 else 20 if A<4e6 else 28 if A<10e6 else 36)
        other=(20e3 if m<7 else 30e3 if A<50e3 else 45e3 if A<300e3 else 70e3 if A<1.5e6 else 100e3 if A<4e6 else 140e3 if A<10e6 else 190e3)
        one={0:60e3,1:60e3,2:40e3,10:120e3}.get(m,0)+(120e3 if m>=22 and m%12==10 else 0)
        opex=A*var+staff*staff_cost/12+other+one
        inflow=(500_000 if m==0 else 0)+(bridge if m==3 else 0); debt+=bridge if m==3 else 0
        cash+=earned+g+mg-opex+inflow-debt*0.01/12
        rows.append((m,A,earned,g,mg,opex,cash))
    return rows
