from model import run
import sys
def funding(m, shortfall=False):
    f={}
    if m==0: f['founder']=500_000
    if m==2: f['anchor loan']=3_000_000
    if 3<=m<=12 and m%3==0: f['seed grants']=100_000
    if 12<=m<=48 and m%3==0: f['research/open-source grants']=250_000 if not (shortfall and m>=36) else 125_000
    if m>=18 and m%12==6: f['c3 donations']=300_000
    if m==24: f['PRI tranche 2']=4_000_000
    if m==42 and not shortfall: f['PRI tranche 3']=5_000_000
    return f
def sim(shortfall=False, planB=False, horizon=96, **kw):
    rows,be,peak = run(horizon=horizon, var=0.045, org_ratio=1.5, conv_final=0.03, **kw)
    cash=0; out=[]; debt=0; tot={}
    for r in rows:
        m=r[0]; net=r[10]
        if planB and m>=36:
            # freeze: staff capped at 18, other at 90k, growth unaffected here (see growth variant)
            A=r[1]; rev=r[5]; var=r[6]
            staff=min(r[7],18); st=staff*175_000/12; oth=min(r[9],90_000) if m%12!=8 else 90_000+150_000
            net=rev-var-st-oth
        f=funding(m,shortfall)
        for k,v in f.items(): tot[k]=tot.get(k,0)+v
        inflow=sum(f.values())
        if 'loan' in ' '.join(f) or 'PRI' in ' '.join(f): debt+=sum(v for k,v in f.items() if 'loan' in k or 'PRI' in k)
        interest = debt*0.01/12
        cash += net + inflow - interest
        out.append((m,r,net,inflow,interest,cash,f))
    return out,tot,be
if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "base"
    out,tot,be=sim(shortfall=(mode!="base"), planB=(mode=="planB"))
    mincash=min(o[5] for o in out); print("mincash",mincash,"at",[o[0] for o in out if o[5]==mincash], "totals",tot, sum(tot.values()))
    for m,r,net,inflow,intr,cash,f in out:
        if m<=24 or m%3==0:
            print(f"| {m} | {r[1]:,.0f} | {r[2]*100:.1f}% | {r[3]:,.0f} | {r[4]:,.0f} | {r[5]/1000:,.0f} | {r[6]/1000:,.0f} | {r[7]} | {(r[8]+r[9])/1000:,.0f} | {net/1000:,.0f} | {inflow/1000:,.0f} {'('+', '.join(f)+')' if f else ''} | {cash/1000:,.0f} |")
