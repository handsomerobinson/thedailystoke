import sys, math
# scenario params
def run(conv_final=0.03, growth_mult=1.0, var=0.075, staff_cost=175_000, org_ratio=1.0, print_rows=False, horizon=120, gate=False, label=""):
    # account-holder anchors (month -> A) base
    anchors = [(0,0),(6,300),(12,10_000),(18,40_000),(24,120_000),(30,300_000),(36,600_000),(48,1_800_000),(60,3_800_000),(72,6_500_000),(84,10_000_000),(96,14_000_000),(120,22_000_000)]
    def A_at(m):
        # growth_mult stretches time: slower growth => anchors reached later
        t = m*growth_mult
        for (m0,a0),(m1,a1) in zip(anchors,anchors[1:]):
            if t<=m1:
                if a0==0: return a1*(t-m0)/(m1-m0)
                r=(a1/a0)**((t-m0)/(m1-m0)); return a0*r
        return anchors[-1][1]
    def conv(m):
        if m<9: return 0
        if m<=24: return 0.01+ (min(conv_final,0.025)-0.01)*(m-9)/15 if conv_final>=0.025 else 0.01+(conv_final-0.01)*(m-9)/15
        if m<=36: 
            c24 = 0.025 if conv_final>=0.025 else conv_final
            return c24+(conv_final-c24)*(m-24)/12
        return conv_final
    def keeper_net(m): return 3.60 if m<19 else 3.40
    def orgs(m,A):
        if m<10: return 0
        early = min(60, 5*(m-9))
        return max(early, org_ratio*A/1000)
    def staff(m,A):
        if m<=3: return 4
        if m<=9: return 7
        if A<60_000: return 9
        if A<400_000: return 13
        if A<1_200_000: return 18
        if A<3_000_000: return 24
        if A<6_000_000: return 30
        if A<12_000_000: return 38
        return 50
    def other(m,A):
        if m<=9: return 30_000
        if A<60_000: return 40_000
        if A<400_000: return 60_000
        if A<1_200_000: return 90_000
        if A<3_000_000: return 120_000
        if A<6_000_000: return 150_000
        if A<12_000_000: return 190_000
        return 260_000
    onetime = {0:70_000,1:90_000,2:80_000,8:300_000,17:40_000,18:40_000}
    rows=[]; cum=0; minc=0; be=None; peak=0
    for m in range(0,horizon+1):
        A=A_at(m)
        if m%12==8 and m>=20: onetime_m=150_000   # annual audit + pentest
        else: onetime_m=onetime.get(m,0)
        k=A*conv(m); o=orgs(m,A)
        rev = k*keeper_net(m) + o*38
        vc = A*var if m>=7 else A*var
        st = staff(m,A)*staff_cost/12
        fx = st+other(m,A)+onetime_m
        net = rev - vc - fx
        cum += net
        if cum<peak: peak=cum
        if be is None and m>12 and net>=0: be=m
        rows.append((m,A,conv(m),k,o,rev,vc,staff(m,A),st,other(m,A)+onetime_m,net,cum))
    return rows,be,peak
if __name__=="__main__":
    rows,be,peak=run()
    for r in rows:
        m=r[0]
        if m<=24 or m%3==0:
            print(f"M{m:3d} A={r[1]:>11,.0f} c={r[2]*100:4.2f}% K={r[3]:>9,.0f} orgs={r[4]:>7,.0f} rev={r[5]:>11,.0f} var={r[6]:>10,.0f} staff={r[7]:2d} staff$={r[8]:>9,.0f} other={r[9]:>8,.0f} net={r[10]:>11,.0f} cum={r[11]:>13,.0f}")
    print("BE",be,"peak",peak)
