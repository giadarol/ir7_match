import xtrack as xt

collider = xt.Multiline.from_json("hllhc.json")
collider.build_trackers()

tw0 = collider.twiss()

# Load new strength for ir7
from cpymad.madx import Madx
mad = Madx()
mad.options.echo = False
mad.options.info = False
mad.options.warn = True
mad.call("ir7_optics5_2.str")

for kk in mad.globals.keys():
    collider.vars[kk] = mad.globals[kk]

betxip7b1 = collider.vars["betxip7b1"]._value
alfxip7b1 = collider.vars["alfxip7b1"]._value
betyip7b1 = collider.vars["betyip7b1"]._value
alfyip7b1 = collider.vars["alfyip7b1"]._value
dxip7b1 = collider.vars["dxip7b1"]._value
dpxip7b1 = collider.vars["dpxip7b1"]._value

betxip7b2 = collider.vars["betxip7b2"]._value
alfxip7b2 = collider.vars["alfxip7b2"]._value
betyip7b2 = collider.vars["betyip7b2"]._value
alfyip7b2 = collider.vars["alfyip7b2"]._value
dxip7b2 = collider.vars["dxip7b2"]._value
dpxip7b2 = collider.vars["dpxip7b2"]._value

scale = 23348.89927
scmin = 0.03 * 7000
qtlimitx28 = 1.0*225.0/scale
qtlimitx15 = 1.0*205.0/scale
qtlimit2 = 1.0*160.0/scale
qtlimit3 = 1.0*200.0/scale
qtlimit4 = 1.0*125.0/scale
qtlimit5 = 1.0*120.0/scale
qtlimit6 = 1.0*90.0/scale

twinit_b1 = tw0.lhcb1.get_twiss_init("s.ds.l7.b1")
twinit_b2 = tw0.lhcb2.get_twiss_init("s.ds.l7.b2")


opt = collider.match(
    solve=False,
    ele_start=("s.ds.l7.b1", "s.ds.l7.b2"),
    ele_stop=("e.ds.r7.b1", "e.ds.r7.b2"),
    twiss_init=(twinit_b1, twinit_b2),
    targets=[
        # Optics in IP7 for beam 1
        xt.Target(line='lhcb1', at='ip7', tar='betx', value=betxip7b1, tol=1e-6),
        xt.Target(line='lhcb1', at='ip7', tar='alfx', value=alfxip7b1, tol=1e-6),
        xt.Target(line='lhcb1', at='ip7', tar='bety', value=betyip7b1, tol=1e-6),
        xt.Target(line='lhcb1', at='ip7', tar='alfy', value=alfyip7b1, tol=1e-6),
        xt.Target(line='lhcb1', at='ip7', tar='dx',   value=dxip7b1,   tol=1e-6),
        xt.Target(line='lhcb1', at='ip7', tar='dpx',  value=dpxip7b1,  tol=1e-6),

        # Optics in IP7 for beam 2
        xt.Target(line='lhcb2', at='ip7', tar='betx', value=betxip7b2, tol=1e-6),
        xt.Target(line='lhcb2', at='ip7', tar='alfx', value=alfxip7b2, tol=1e-6),
        xt.Target(line='lhcb2', at='ip7', tar='bety', value=betyip7b2, tol=1e-6),
        xt.Target(line='lhcb2', at='ip7', tar='alfy', value=alfyip7b2, tol=1e-6),
        xt.Target(line='lhcb2', at='ip7', tar='dx',   value=dxip7b2,   tol=1e-6),
        xt.Target(line='lhcb2', at='ip7', tar='dpx',  value=dpxip7b2,  tol=1e-6),

        # Optics in 'e.ds.r7.b1' for beam 1
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='betx', value=tw0.lhcb1['betx','e.ds.r7.b1'], tol=1e-6),
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='alfx', value=tw0.lhcb1['alfx','e.ds.r7.b1'], tol=1e-6),
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='bety', value=tw0.lhcb1['bety','e.ds.r7.b1'], tol=1e-6),
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='alfy', value=tw0.lhcb1['alfy','e.ds.r7.b1'], tol=1e-6),
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='dx',   value=tw0.lhcb1['dx','e.ds.r7.b1'],   tol=1e-6),
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='dpx',  value=tw0.lhcb1['dpx','e.ds.r7.b1'],  tol=1e-6),
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='mux',  value=tw0.lhcb1['mux','e.ds.r7.b1'],  tol=1e-6),
        xt.Target(line='lhcb1', at='e.ds.r7.b1', tar='muy',  value=tw0.lhcb1['muy','e.ds.r7.b1'],  tol=1e-6),

        # Optics in 'e.ds.r7.b2' for beam 2
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='betx', value=tw0.lhcb2['betx','e.ds.r7.b2'], tol=1e-6),
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='alfx', value=tw0.lhcb2['alfx','e.ds.r7.b2'], tol=1e-6),
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='bety', value=tw0.lhcb2['bety','e.ds.r7.b2'], tol=1e-6),
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='alfy', value=tw0.lhcb2['alfy','e.ds.r7.b2'], tol=1e-6),
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='dx',   value=tw0.lhcb2['dx','e.ds.r7.b2'],   tol=1e-6),
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='dpx',  value=tw0.lhcb2['dpx','e.ds.r7.b2'],  tol=1e-6),
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='mux',  value=tw0.lhcb2['mux','e.ds.r7.b2'],  tol=1e-6),
        xt.Target(line='lhcb2', at='e.ds.r7.b2', tar='muy',  value=tw0.lhcb2['muy','e.ds.r7.b2'],  tol=1e-6),
    ],
    vary=[
        xt.Vary('kqt4.l7',     step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt4.r7',     step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt5.l7',     step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt5.r7',     step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt13.l7b1',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt12.l7b1',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqtl11.l7b1', step=1.0E-9, limits=(-qtlimit4*300./550., qtlimit4*300./550.)),
        xt.Vary('kqtl10.l7b1', step=1.0E-9, limits=(-qtlimit4*500./550., qtlimit4*500./550.)),
        xt.Vary('kqtl9.l7b1',  step=1.0E-9, limits=(-qtlimit4*400./550., qtlimit4*400./550.)),
        xt.Vary('kqtl8.l7b1',  step=1.0E-9, limits=(-qtlimit4*300./550., qtlimit4*300./550.)),
        xt.Vary('kqtl7.l7b1',  step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kq6.l7b1',    step=1.0E-9, limits=(-qtlimit6, qtlimit6)),
        xt.Vary('kq6.r7b1',    step=1.0E-9, limits=(-qtlimit6, qtlimit6)),
        xt.Vary('kqtl7.r7b1',  step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kqtl8.r7b1',  step=1.0E-9, limits=(-qtlimit4*550./550., qtlimit4*550./550.)),
        xt.Vary('kqtl9.r7b1',  step=1.0E-9, limits=(-qtlimit4*500./550., qtlimit4*500./550.)),
        xt.Vary('kqtl10.r7b1', step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kqtl11.r7b1', step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kqt12.r7b1',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt13.r7b1',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt13.l7b2',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt12.l7b2',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqtl11.l7b2', step=1.0E-9, limits=(-qtlimit4*300./550., qtlimit4*300./550.)),
        xt.Vary('kqtl10.l7b2', step=1.0E-9, limits=(-qtlimit4*500./550., qtlimit4*500./550.)),
        xt.Vary('kqtl9.l7b2',  step=1.0E-9, limits=(-qtlimit4*400./550., qtlimit4*400./550.)),
        xt.Vary('kqtl8.l7b2',  step=1.0E-9, limits=(-qtlimit4*300./550., qtlimit4*300./550.)),
        xt.Vary('kqtl7.l7b2',  step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kq6.l7b2',    step=1.0E-9, limits=(-qtlimit6, qtlimit6)),
        xt.Vary('kq6.r7b2',    step=1.0E-9, limits=(-qtlimit6, qtlimit6)),
        xt.Vary('kqtl7.r7b2',  step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kqtl8.r7b2',  step=1.0E-9, limits=(-qtlimit4*550./550., qtlimit4*550./550.)),
        xt.Vary('kqtl9.r7b2',  step=1.0E-9, limits=(-qtlimit4*500./550., qtlimit4*500./550.)),
        xt.Vary('kqtl10.r7b2', step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kqtl11.r7b2', step=1.0E-9, limits=(-qtlimit4, qtlimit4)),
        xt.Vary('kqt12.r7b2',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
        xt.Vary('kqt13.r7b2',  step=1.0E-9, limits=(-qtlimit5, qtlimit5)),
    ])