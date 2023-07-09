import time

import re
import numpy as np

import xtrack as xt
import xpart as xp
import xdeps as xd

t0 = time.time()

lhc = xt.Multiline.from_json("hllhc.json")
lhc.build_trackers()

t1 = time.time()

p1 = lhc.lhcb1.build_particles(x=0, delta=1e-3)
p2 = lhc.lhcb2.build_particles(x=0, delta=1e-3)
lhc.lhcb1.track(p1, ele_start="tcp.d6l7.b1", ele_stop="tcspm.6r7.b1")
print(p1.x / 1e-3)
lhc.lhcb2.track(p2, ele_start="tcp.d6r7.b2", ele_stop="tcspm.6l7.b2", backtrack=True)
print(p2.x / 1e-3)

t2 = time.time()

class SinglePassDispersion(xd.Action):
    def __init__(self, line, ele_start, ele_stop, backtrack=False, delta=1e-3):
        self.line = line
        self.ele_start = ele_start
        self.ele_stop = ele_stop
        self.delta = delta
        self.backtrack = backtrack
        self._pp = line.build_particles(delta=delta)

    def run(self):
        for nn in ["x", "px", "y", "py", "zeta", "delta", "at_element"]:
            setattr(self._pp, nn, 0)
        self._pp.delta = self.delta
        self.line.track(
            self._pp,
            ele_start=self.ele_start,
            ele_stop=self.ele_stop,
            backtrack=self.backtrack,
        )
        return {
            "d" + nn: getattr(self._pp, nn)[0] / self.delta
            for nn in ["x", "px", "y", "py"]
        }

t3 = time.time()


tw1 = lhc.lhcb1.twiss()
tw2 = lhc.lhcb2.twiss()
assert np.allclose(tw1["betx", "ip5"], 0.5)
assert np.allclose(tw2["betx", "ip5"], 0.5)

bir7b1 = tw1.get_twiss_init("s.ds.l7.b1")
eir7b1 = tw1.get_twiss_init("e.ds.r7.b1")
bir7b2 = tw2.get_twiss_init("s.ds.l7.b2")
eir7b2 = tw2.get_twiss_init("e.ds.r7.b2")

t4 = time.time()

from pyoptics import madlang
newopt=madlang.load(open("ir7_optics5_2.str")).vars_to_dict()
for k,v in newopt.items():
    lhc.vars[k]=v

t5 = time.time()

namelist=sorted([nn for nn in lhc.vars.keys() if re.match(r"kq[t0-9].*\.[lr]7", nn)])
varylist = [ xt.Vary(nn, step=1e-6) for nn in namelist ]

act_sp1 = SinglePassDispersion(
    lhc.lhcb1, ele_start="tcp.d6l7.b1", ele_stop="tcspm.6r7.b1"
)
act_sp2 = SinglePassDispersion(
    lhc.lhcb2, ele_start="tcp.d6r7.b2", ele_stop="tcspm.6l7.b2", backtrack=False
)

# build targets
zz1 = ["e.ds.r7.b1", tw1, "lhcb1"], ["e.ds.r7.b2", tw2, "lhcb2"]
zz = ["betx", "bety", "alfx", "alfy", "dx", "dpx", "mux", "muy"]
ww = [1e-4, 1e-4, 1e-4, 1e-4, 1e-6, 1e-6, 1e-6, 1e-6]

tarlist_end = [
    xt.Target(oo, tw[oo, ee], line=ll, at=ee, tol=1e-7)
    for ee, tw, ll in zz1
    for oo,tl in zip(zz,ww)
]

zz1 = ["ip7", tw1, "lhcb1"], ["ip7", tw2, "lhcb2"]
zz = ["betx", "bety", "alfx", "alfy", "dx", "dpx"]
ww = [1e-4, 1e-4, 1e-4, 1e-4, 1e-6, 1e-6]

tarlist_ip = [
    xt.Target(oo, lhc.vars[f"{oo}ip7b{ll[-1]}"]._value, line=ll, at=ee, tol=1e-7)
    for ee, tw, ll in zz1
    for oo,tl in zip(zz,ww)
]

tarlist_sp = [
        xt.Target(action=act_sp1, tar="dx", value=-0.03126, tol=1e-7),
        xt.Target(action=act_sp2, tar="dx", value=-0.03126, tol=1e-7),
    ]

t6 = time.time()


out=lhc.match(
    ele_start=("s.ds.l7.b1", "s.ds.l7.b2"),
    ele_stop=("e.ds.r7.b1", "e.ds.r7.b2"),
    twiss_init=(bir7b1, bir7b2),
    targets=tarlist_end+tarlist_ip,
    vary=varylist,
    verbose=False,
    solver_options={"n_steps_max": 10},
    assert_within_tol=False
)

t7 = time.time()

for tt in out['optimizer']._err.targets:
    if tt.line:
       nn=" ".join((tt.line,)+tt.tar)
       rr=tt.action.run()[tt.line][tt.tar]
    else:
       nn=tt.tar
       rr=tt.action.run()[tt.tar]
    vv=tt.value
    dd=(rr-vv)
    print(f'{nn:25}: {rr:15.7e} {vv:15.7e} d={dd:15.7e} {dd<tt.tol}')


for nn,vv in zip(varylist,out['res']):
    print(f"{nn.name:15} {vv}")


t = [t1-t0, t2-t1, t3-t2, t4-t3, t5-t4, t6-t5, t7-t6]