from cpymad import madx

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
call,file="madxonly/rematch_ir7b12.madx";
''')

mad.use('lhcb1')
tw1_b1 = mad.twiss().dframe()
mad.use('lhcb2')
tw1_b2 = mad.twiss().dframe()
