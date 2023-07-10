import xtrack as xt
import xpart as xp

from cpymad.madx import Madx

mad1=Madx()
mad1.call('../acc-models-lhc/lhc.seq')
mad1.call('../acc-models-lhc/hllhc_sequence.madx')
mad1.input('beam, sequence=lhcb1, particle=proton, energy=7000;')
mad1.use('lhcb1')
mad1.call("madxonly/opt_ramp_500_1500.madx")
mad1.globals['l.mbh'] = 1e-20
mad1.twiss()

mad4=Madx()
mad4.input('mylhcbeam=4')
mad4.call('../acc-models-lhc/lhcb4.seq')
mad4.call('../acc-models-lhc/hllhc_sequence.madx')
mad4.input('beam, sequence=lhcb2, particle=proton, energy=7000;')
mad4.use('lhcb2')
mad4.call("madxonly/opt_ramp_500_1500.madx")
mad4.globals['l.mbh'] = 1e-20
mad4.twiss()

# Patch

line1=xt.Line.from_madx_sequence(mad1.sequence.lhcb1,
                                 allow_thick=True,
                                 deferred_expressions=True,
                                 replace_in_expr={'bv_aux':'bvaux_b1'})
line1.particle_ref = xp.Particles(mass0=xp.PROTON_MASS_EV, p0c=7000e9)

line4=xt.Line.from_madx_sequence(mad4.sequence.lhcb2,
                                 allow_thick=True,
                                 deferred_expressions=True,
                                 replace_in_expr={'bv_aux':'bvaux_b2'})
line4.particle_ref = xp.Particles(mass0=xp.PROTON_MASS_EV, p0c=7000e9)

collider = xt.Multiline(lines={'lhcb1':line1,'lhcb2':line4})
collider.lhcb1.particle_ref=xp.Particles(mass0=xp.PROTON_MASS_EV,p0c=7000e9)
collider.lhcb2.particle_ref=xp.Particles(mass0=xp.PROTON_MASS_EV,p0c=7000e9)

collider.lhcb1.twiss_default['method']='4d'
collider.lhcb2.twiss_default['method']='4d'
collider.lhcb2.twiss_default['reverse']=True

collider.build_trackers()

tw = collider.twiss()

collider.to_json('hllhc.json')