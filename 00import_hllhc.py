import numpy as np

import xtrack as xt
import xpart as xp

from cpymad.madx import Madx

mad1=Madx()
mad4=Madx()

mad1.call('hllhcb1.madx')
mad4.call('hllhcb4.madx')
mad1.use("lhcb1")
mad4.use("lhcb2")

mad1.twiss()
mad4.twiss()

line1=xt.Line.from_madx_sequence(mad1.sequence.lhcb1,deferred_expressions=True,replace_in_expr={'bv_aux':'bvaux_b1'})
line4=xt.Line.from_madx_sequence(mad4.sequence.lhcb2,deferred_expressions=True,replace_in_expr={'bv_aux':'bvaux_b2'})

lhc=xt.Multiline(lines={'lhcb1':line1,'lhcb2':line4})
lhc.lhcb1.particle_ref=xp.Particles(mass0=xp.PROTON_MASS_EV,p0c=7000e9)
lhc.lhcb2.particle_ref=xp.Particles(mass0=xp.PROTON_MASS_EV,p0c=7000e9)

lhc.lhcb1.twiss_default['method']='4d'
lhc.lhcb2.twiss_default['method']='4d'
lhc.lhcb2.twiss_default['reverse']=True

lhc.build_trackers()

lhc.lhcb1.twiss()
lhc.lhcb2.twiss()

ini1=xt.TwissInit(betx=0.5,bety=0.5,line=lhc.lhcb2,element_name='lhcb1$start')
ini2=xt.TwissInit(betx=0.5,bety=0.5,line=lhc.lhcb2,element_name='lhcb2$start')

tw1=lhc.lhcb2.twiss(twiss_init=ini2,reverse=False,ele_start='lhcb2$start',ele_stop='lhcb2$end')
tw2=lhc.lhcb2.twiss(twiss_init=ini2,reverse=False,ele_start='lhcb2$start',ele_stop='lhcb2$end')

tw1.rows['ip.*'].cols['betx bety']
tw2.rows['ip.*'].cols['betx bety']

assert np.allclose(tw1['betx','ip5'],0.5)
assert np.allclose(tw2['betx','ip5'],0.5)

lhc.to_json('hllhc.json')










