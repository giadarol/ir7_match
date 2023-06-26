import numpy as np

import xtrack as xt
import xpart as xp

lhc = xt.Multiline.from_json("hllhc.json")
lhc.build_trackers()


tw1 = lhc.lhcb1.twiss()
tw2 = lhc.lhcb2.twiss()
assert np.allclose(tw1["betx", "ip5"], 0.5)
assert np.allclose(tw2["betx", "ip5"], 0.5)

tw1 = lhc.lhcb1.twiss()
tw2 = lhc.lhcb2.twiss()
bir7b1=tw1.get_twiss_init("s.ds.l7.b1")
eir7b1=tw1.get_twiss_init("e.ds.r7.b1")
bir7b2=tw2.get_twiss_init("s.ds.l7.b2")
eir7b2=tw2.get_twiss_init("e.ds.r7.b2")

varylist = [xt.Vary("kqt13.l7b1", step=1e-6), xt.Vary("kqt13.l7b2", step=1e-6)]

lhc.vars["kqt4.r7"] *= 0.99

lhc.match(
    ele_start=("s.ds.l7.b1", "s.ds.l7.b2"),
    ele_stop=("e.ds.r7.b1", "e.ds.r7.b2"),
    twiss_init=(bir7b1,bir7b2),
    targets=[
        xt.Target("betx", tw1['betx',"e.ds.r7.b1"], line="lhcb1", at="e.ds.r7.b1", tol=1e-6),
        xt.Target("betx", tw2['betx',"e.ds.r7.b2"], line="lhcb2", at="e.ds.r7.b2", tol=1e-6),
    ],
    vary=varylist,
    verbose=True,
)



