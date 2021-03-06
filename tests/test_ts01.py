import pytest
import os
import subprocess
import numpy.testing as npt

from qcifc.core import QuantumChemistry, DaltonFactory

CASE = 'ts01'

@pytest.fixture(params=['DaltonDummy', 'Dalton'])
def qcp(request):
    tmp = os.path.join(os.path.dirname(__file__), f'test_{CASE}.d')
    factory = QuantumChemistry.set_code(
            request.param,
            tmpdir=tmp,
            )
    return factory

@pytest.fixture(scope='module')
def mod():
    tmpdir = os.path.join(os.path.dirname(__file__), f'test_{CASE}.d')
    os.chdir(tmpdir)
    subprocess.call(['dalton', '-get', 'AOPROPER AOONEINT AOTWOINT', 'hf', CASE])
    subprocess.call(['tar', 'xvfz', f'hf_{CASE}.tar.gz'])
    yield
    subprocess.call('rm *.[0-9] DALTON.* *AO* *SIR* *RSP* molden.inp', shell=True)
    
def test_get_orbhess(mod, qcp):
    """Get diagonal orbital hessian"""
    od = qcp.get_orbital_diagonal() 
    npt.assert_allclose(od,
      [
          207.63510426,  21.00522587,  15.89399134,  15.88200483,
           15.88200483,   2.29411362,   1.41453738,   1.07335853,
            1.07335853, 416.9399669 ,  43.68021011,  33.45774106,
           33.43376805,  33.43376805,   6.25798563,   4.49883315,
            3.81647545,   3.81647545,   2.0435971 , 207.63510426,
           21.00522587,  15.89399134,  15.88200483,  15.88200483,
            2.29411362,   1.41453738,   1.07335853,   1.07335853,
          416.9399669 ,  43.68021011,  33.45774106,  33.43376805,
           33.43376805,   6.25798563,   4.49883315,   3.81647545,
            3.81647545,   2.0435971 
        ]
    )

def test_get_s2_diagonal(mod, qcp):
    """Get diagonal overlap hessian"""
    sd = qcp.get_overlap_diagonal() 
    lsd = len(sd)
    npt.assert_allclose(
        sd,
        [
            1., 1., 1., 1., 1., 1., 1., 1., 1.,
            2., 2., 2., 2., 2., 2., 2., 2., 2., 1., 
            -1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,
           -2.,-2.,-2.,-2.,-2.,-2.,-2.,-2.,-2.,-1.
        ]
    )
    

def test_get_rhs(mod, qcp):
    """Get property gradient right-hand side"""
    rhs,  = qcp.get_rhs('z',) 
    npt.assert_allclose(
       rhs,
       [ 
        -6.57989324e-19,  4.62112979e-18,  3.46230723e-20,
        -3.41544066e-03,  2.51740485e-12, -6.31689618e-17,
        -2.21892286e-17,  3.25372463e-02,  1.11583016e-16,
         1.77519347e-19,  1.39030993e-17, -1.30975112e-18,
         3.08379878e-02, -2.27296296e-11, -1.07341703e-16,
        -1.20667401e-17, -2.84863611e-01, -9.76877341e-16,
         8.22187178e-18,  6.57989324e-19, -4.62112979e-18,
        -3.46230723e-20,  3.41544066e-03, -2.51740485e-12,
         6.31689618e-17,  2.21892286e-17, -3.25372463e-02,
        -1.11583016e-16, -1.77519347e-19, -1.39030993e-17,
         1.30975112e-18, -3.08379878e-02,  2.27296296e-11,
         1.07341703e-16,  1.20667401e-17,  2.84863611e-01,
         9.76877341e-16, -8.22187178e-18
       ] 
    )

@pytest.mark.parametrize('args',
    [
        (
            'z', (0.0,),
            {('z', 0.0): [
                -3.16896955e-21,  2.19999053e-19,  2.17837493e-21,
                -2.15050977e-04,  1.58506743e-13, -2.75352368e-17,
                -1.56865621e-17,  3.03134929e-02,  1.03956891e-16,
                 4.25767164e-22,  3.18292866e-19, -3.91464300e-20,
                 9.22360524e-04, -6.79840502e-13, -1.71527564e-17,
                -2.68219329e-18, -7.46404934e-02, -2.55963219e-16,
                 4.02323520e-18, 
                 3.16896955e-21, -2.19999053e-19, -2.17837493e-21,
                 2.15050977e-04, -1.58506743e-13,  2.75352368e-17,
                 1.56865621e-17, -3.03134929e-02, -1.03956891e-16,
                -4.25767164e-22, -3.18292866e-19,  3.91464300e-20,
                -9.22360524e-04,  6.79840502e-13,  1.71527564e-17, 
                 2.68219329e-18,  7.46404934e-02,  2.55963219e-16,
                -4.02323520e-18
            ]}
        ),
        (
            'z', (0.5,),
            { ('z', 0.5): [
            -3.17661908e-21,  2.25363516e-19,  2.24912900e-21,
            -2.22041320e-04,  1.63659086e-13, -3.52090085e-17,
            -2.42627901e-17,  5.67485166e-02,  1.94612985e-16,
             4.26790791e-22,  3.25750488e-19, -4.03525038e-20,
             9.50798802e-04, -7.00801387e-13, -2.04149860e-17,
            -3.44878981e-18, -1.01141876e-01, -3.46843904e-16,
             5.32643641e-18,
             3.16135678e-21, -2.14884039e-19, -2.11193672e-21,  
             2.08487343e-04, -1.53668912e-13, 2.26078715e-17,  
             1.15898643e-17, -2.06801219e-02, -7.09202724e-17, 
            -4.24748436e-22, -3.11169066e-19, 3.80103593e-20, 
            -8.95574012e-04,  6.60097077e-13, 1.47894620e-17,  
             2.19441830e-18,  5.91435820e-02, 2.02819956e-16, 
            -3.23237976e-18
             ],
            }
        ),
    ],
    ids=['0.0', '0.5']
)
def test_initial_guess(mod, qcp, args):
    """form paired trialvectors from rhs/orbdiag"""
    ops, freqs, expected = args
    initial_guess = qcp.initial_guess(ops, freqs)
    for op, freq in zip(ops, freqs):
        npt.assert_allclose(
            initial_guess[(op, freq)],
            expected[(op, freq)],
            rtol=1e-5,
        )

@pytest.mark.parametrize('args',
    [
        ('x', 'x', (0,), {('x', 'x', 0): -1.545996633923e+01}),
        ('y', 'y', (0,), {('y', 'y', 0): -1.745339237129e-01}),
        ('z', 'z', (0,), {('z', 'z', 0): -1.745339237129e-01}),
        ('x', 'x', (0.5,), {('x', 'x', 0.5): -2.270755038893e+01}),
        ('y', 'y', (0.5,), {('y', 'y', 0.5): -2.072139155315e-01}),
        ('z', 'z', (0.5,), {('z', 'z', 0.5): -2.072139155315e-01}),
    ],
    ids=['xx0', 'yy0', 'zz0', 'xx0.5', 'yy0.5', 'zz0.5']
)
def test_lr(mod, qcp, args):
    aops, bops, freqs, expected = args
    lr = qcp.lr(aops, bops, freqs)
    for k, v in lr.items():
        npt.assert_allclose(v, expected[k], rtol=1e-4)
