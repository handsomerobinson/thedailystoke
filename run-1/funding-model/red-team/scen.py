from model import run
sc = {
 "Phase04-as-written-ish (var .066, org1, conv3, $140k)": dict(var=0.066,org_ratio=1.0,conv_final=0.03,staff_cost=140_000),
 "Uncorrected w/ realistic staff (var .075, org1, conv3)": dict(var=0.075,org_ratio=1.0,conv_final=0.03),
 "BASE (var .045, org1.5, conv3)": dict(var=0.045,org_ratio=1.5,conv_final=0.03),
 "conv 2%": dict(var=0.045,org_ratio=1.5,conv_final=0.02),
 "conv 1.5%": dict(var=0.045,org_ratio=1.5,conv_final=0.015),
 "conv 4%": dict(var=0.045,org_ratio=1.5,conv_final=0.04),
 "growth half speed": dict(var=0.045,org_ratio=1.5,conv_final=0.03,growth_mult=0.5),
 "growth 0.7 speed": dict(var=0.045,org_ratio=1.5,conv_final=0.03,growth_mult=0.7),
 "var 2x (.09)": dict(var=0.09,org_ratio=1.5,conv_final=0.03),
 "staff +20%": dict(var=0.045,org_ratio=1.5,conv_final=0.03,staff_cost=210_000),
 "org 3/1000": dict(var=0.045,org_ratio=3,conv_final=0.03),
}
for k,v in sc.items():
    rows,be,peak=run(horizon=180,**v)
    A = rows[be][1] if be else None
    # sustained BE: first month after which net>=0 for 12 consecutive months
    sbe=None
    for i in range(13,len(rows)-12):
        if all(rows[j][10]>=0 for j in range(i,i+12)): sbe=i;break
    print(f"{k:55s} firstBE={be} sustainedBE={sbe} A@sBE={rows[sbe][1]/1e6 if sbe else 0:.1f}M peakDeficit={peak/1e6:.1f}M")
