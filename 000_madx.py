import numpy as np
from cpymad import madx
import time

mad = madx.Madx()

mad.input('''
option,-echo,-info;
option,-rbarc;
call,file="madxonly/hllhcb12.madx";
call,file="madxonly/macro.madx";
exec,mk_beam(7000);
call,file="madxonly/opt_ramp_500_1500.madx";
exec,check_ip(b1);
exec,check_ip(b2);
'''
)

mad.use('lhcb1')
tw0_b1 = mad.twiss().dframe()
mad.use('lhcb2')
tw0_b2 = mad.twiss().dframe()


mad.input('''
call,file="madxonly/ir7_optics5_2.str";

on_holdselect=1; jac_calls=   15;jac_tol=1e-20; jac_bisec=3;
exec,select(7,67,78,b1);
exec,select(7,67,78,b2);
jac_calls=15;
''')

knob_names = ['kqt4.l7', 'kqt4.r7', 'kqt5.l7', 'kqt5.r7', 'kqt13.l7b1',
    'kqt12.l7b1', 'kqtl11.l7b1', 'kqtl10.l7b1', 'kqtl9.l7b1', 'kqtl8.l7b1',
    'kqtl7.l7b1', 'kq6.l7b1', 'kq6.r7b1', 'kqtl7.r7b1', 'kqtl8.r7b1',
    'kqtl9.r7b1', 'kqtl10.r7b1', 'kqtl11.r7b1', 'kqt12.r7b1', 'kqt13.r7b1',
    'kqt13.l7b2', 'kqt12.l7b2', 'kqtl11.l7b2', 'kqtl10.l7b2', 'kqtl9.l7b2',
    'kqtl8.l7b2', 'kqtl7.l7b2', 'kq6.l7b2', 'kq6.r7b2', 'kqtl7.r7b2',
    'kqtl8.r7b2', 'kqtl9.r7b2', 'kqtl10.r7b2', 'kqtl11.r7b2', 'kqt12.r7b2',
    'kqt13.r7b2']

knobs_before = {}
for kk in knob_names:
    knobs_before[kk] = mad.globals[kk]

t1 = time.time()
mad.input('''

scale = 23348.89927;
scmin := 0.03*7000./nrj;
qtlimitx28 := 1.0*225.0/scale;
qtlimitx15 := 1.0*205.0/scale;
qtlimit2 := 1.0*160.0/scale;
qtlimit3 := 1.0*200.0/scale;
qtlimit4 := 1.0*125.0/scale;
qtlimit5 := 1.0*120.0/scale;
qtlimit6 := 1.0*90.0/scale;


use,sequence=lhcb1,range=s.ds.l7.b1/e.ds.r7.b1;
use,sequence=lhcb2,range=s.ds.l7.b2/e.ds.r7.b2;

match,      sequence=lhcb1,lhcb2, beta0=bir7b1,bir7b2;
weight,mux=10,muy=10;
constraint, sequence=lhcb1, range=ip7,betx=betxip7b1,bety=betyip7b1;
constraint, sequence=lhcb1, range=ip7,alfx=alfxip7b1,alfy=alfyip7b1;
constraint, sequence=lhcb2, range=ip7,betx=betxip7b2,bety=betyip7b2;
constraint, sequence=lhcb2, range=ip7,alfx=alfxip7b2,alfy=alfyip7b2;
constraint, sequence=lhcb1, range=ip7,dx=dxip7b1,dpx =dpxip7b1;
constraint, sequence=lhcb2, range=ip7,dx=dxip7b2,dpx =dpxip7b2;
constraint, sequence=lhcb1, range=e.ds.r7.b1  alfx=eir7b1->alfx,alfy=eir7b1->alfy;
constraint, sequence=lhcb1, range=e.ds.r7.b1, betx=eir7b1->betx,bety=eir7b1->bety;
constraint, sequence=lhcb1, range=e.ds.r7.b1, dx=eir7b1->dx,dpx=eir7b1->dpx;
constraint, sequence=lhcb1, range=e.ds.r7.b1, mux=muxip7b1+eir7b1->mux;
constraint, sequence=lhcb1, range=e.ds.r7.b1, muy=muyip7b1+eir7b1->muy;
constraint, sequence=lhcb2, range=e.ds.r7.b2, alfx=eir7b2->alfx,alfy=eir7b2->alfy;
constraint, sequence=lhcb2, range=e.ds.r7.b2, betx=eir7b2->betx,bety=eir7b2->bety;
constraint, sequence=lhcb2, range=e.ds.r7.b2, dx=eir7b2->dx,dpx=eir7b2->dpx;
constraint, sequence=lhcb2, range=e.ds.r7.b2, mux=muxip7b2+eir7b2->mux;
constraint, sequence=lhcb2, range=e.ds.r7.b2, muy=muyip7b2+eir7b2->muy;

vary, name=kqt4.l7, step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt4.r7, step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt5.l7, step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt5.r7, step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt13.l7b1,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt12.l7b1,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqtl11.l7b1, step=1.0E-9, lower=-qtlimit4*300./550., upper=qtlimit4*300./550.;
vary, name=kqtl10.l7b1, step=1.0E-9, lower=-qtlimit4*500./550., upper=qtlimit4*500./550.;
vary, name=kqtl9.l7b1,  step=1.0E-9, lower=-qtlimit4*400./550., upper=qtlimit4*400./550.;
vary, name=kqtl8.l7b1,  step=1.0E-9, lower=-qtlimit4*300./550., upper=qtlimit4*300./550.;
vary, name=kqtl7.l7b1,  step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kq6.l7b1,    step=1.0E-9, lower=-qtlimit6, upper=qtlimit6;
vary, name=kq6.r7b1,    step=1.0E-9, lower=-qtlimit6, upper=qtlimit6;
vary, name=kqtl7.r7b1,  step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kqtl8.r7b1,  step=1.0E-9, lower=-qtlimit4*550./550., upper=qtlimit4*550./550.;
vary, name=kqtl9.r7b1,  step=1.0E-9, lower=-qtlimit4*500./550., upper=qtlimit4*500./550.;
vary, name=kqtl10.r7b1, step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kqtl11.r7b1, step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kqt12.r7b1,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt13.r7b1,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt13.l7b2,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt12.l7b2,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqtl11.l7b2, step=1.0E-9, lower=-qtlimit4*300./550., upper=qtlimit4*300./550.;
vary, name=kqtl10.l7b2, step=1.0E-9, lower=-qtlimit4*500./550., upper=qtlimit4*500./550.;
vary, name=kqtl9.l7b2,  step=1.0E-9, lower=-qtlimit4*400./550., upper=qtlimit4*400./550.;
vary, name=kqtl8.l7b2,  step=1.0E-9, lower=-qtlimit4*300./550., upper=qtlimit4*300./550.;
vary, name=kqtl7.l7b2,  step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kq6.l7b2,    step=1.0E-9, lower=-qtlimit6, upper=qtlimit6;
vary, name=kq6.r7b2,    step=1.0E-9, lower=-qtlimit6, upper=qtlimit6;
vary, name=kqtl7.r7b2,  step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kqtl8.r7b2,  step=1.0E-9, lower=-qtlimit4*550./550., upper=qtlimit4*550./550.;
vary, name=kqtl9.r7b2,  step=1.0E-9, lower=-qtlimit4*500./550., upper=qtlimit4*500./550.;
vary, name=kqtl10.r7b2, step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kqtl11.r7b2, step=1.0E-9, lower=-qtlimit4, upper=qtlimit4;
vary, name=kqt12.r7b2,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
vary, name=kqt13.r7b2,  step=1.0E-9, lower=-qtlimit5, upper=qtlimit5;
jacobian,calls=jac_calls, tolerance=jac_tol, bisec=jac_bisec;
endmatch;

''')
t2 = time.time()
print(f'Time for MAD-X matching: {t2-t1}')

knobs_after = {}
for kk in knob_names:
    knobs_after[kk] = mad.globals[kk]

diffs = np.array([knobs_after[kk] - knobs_before[kk] for kk in knobs_after.keys()])

norm_diff_mad = np.sqrt(np.sum(diffs**2, axis=0))

mad.use('lhcb1')
tw1_b1 = mad.twiss().dframe()
mad.use('lhcb2')
tw1_b2 = mad.twiss().dframe()
