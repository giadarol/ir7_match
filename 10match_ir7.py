import numpy as np

import xtrack as xt
import xpart as xp
import xdeps as xd

lhc = xt.Multiline.from_json("hllhc.json")
lhc.build_trackers()


p1=lhc.lhcb1.build_particles(x=0,delta=1e-3)
p2=lhc.lhcb2.build_particles(x=0,delta=1e-3)
lhc.lhcb1.track(p1, ele_start="tcp.d6l7.b1", ele_stop="tcspm.6r7.b1")
print(p1.x/1e-3)
lhc.lhcb2.track(p2, ele_start="tcp.d6r7.b2", ele_stop="tcspm.6l7.b2",backtrack=True)
print(p2.x/1e-3)

class SinglePassDispersion(xd.Action):
    def __init__(self,line,ele_start,ele_stop,backtrack=False,delta=1e-3):
        self.line=line
        self.ele_start=ele_start
        self.ele_stop=ele_stop
        self.delta=delta
        self.backtrack=backtrack
        self._pp=line.build_particles(delta=delta)

    def run(self):
        for nn in ['x','px','y','py','zeta','delta','at_element']:
            setattr(self._pp,nn,0)
        self._pp.delta=self.delta
        self.line.track(self._pp,
                        ele_start=self.ele_start,
                        ele_stop=self.ele_stop,
                        backtrack=self.backtrack)
        return {'d'+nn:getattr(self._pp,nn)[0]/self.delta for nn in ['x','px','y','py']}



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




