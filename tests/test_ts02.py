import pytest
import os
import subprocess
import numpy.testing as npt

from qcifc.core import QuantumChemistry, DaltonFactory

CASE = 'ts02'

@pytest.fixture(params=[
    'DaltonDummy',
    'Dalton'
    ])
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
            41.15162966,  3.05665099,  1.7610597 ,  1.53740381,  1.40776145,
            83.71247278, 84.45117178,  7.52251542,  8.26121442,  4.93133286,
            5.67003186,  4.48402107,  5.22272007,  4.22473636,  4.96343536,
            2.16508555,  2.53443505, 41.15162966,  3.05665099,  1.7610597 ,
            1.53740381,  1.40776145, 83.71247278, 84.45117178,  7.52251542,
            8.26121442,  4.93133286,  5.67003186,  4.48402107,  5.22272007,
            4.22473636,  4.96343536,  2.16508555,  2.53443505
        ]
    )

def test_get_s2_diagonal(mod, qcp):
    """Get diagonal overlap hessian"""
    sd = qcp.get_overlap_diagonal() 
    lsd = len(sd)
    npt.assert_allclose(
        sd,
        [
            1.,  1.,  1.,  1.,  1.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,
        2.,  2.,  1.,  1., -1., -1., -1., -1., -1., -2., -2., -2., -2.,
       -2., -2., -2., -2., -2., -2., -1., -1.
        ]
    )
    

def test_get_rhs(mod, qcp):
    """Get property gradient right-hand side"""
    rhs,  = qcp.get_rhs('z',) 
    npt.assert_allclose(
       rhs,
       [ 
         8.94435483e-17,  8.87286414e-16, -7.28540423e-17,
         1.58013378e-16,  1.26794454e-02, -1.03948048e-17,
        -3.28434472e-18, -2.72446954e-17, -4.10615567e-18,
         2.26716303e-16,  8.45837058e-17, -3.09199726e-16,
        -1.14952287e-16,  1.00618252e-01,  3.78492357e-02,
         6.95956129e-17,  2.62418517e-17, -8.94435483e-17,
        -8.87286414e-16,  7.28540423e-17, -1.58013378e-16,
        -1.26794454e-02,  1.03948048e-17,  3.28434472e-18,
         2.72446954e-17,  4.10615567e-18, -2.26716303e-16,
        -8.45837058e-17,  3.09199726e-16,  1.14952287e-16,
        -1.00618252e-01, -3.78492357e-02, -6.95956129e-17,
        -2.62418517e-17
       ] 
    )

@pytest.mark.parametrize('args',
    [
        (
            'z', (0.0,),
            {('z', 0.0): [
                 2.17351169e-18,  2.90280578e-16, -4.13694335e-17,
                 1.02779359e-16,  9.00681388e-03, -1.24172712e-19,
                -3.88904577e-20, -3.62175334e-18, -4.97040200e-19,
                 4.59746502e-17,  1.49176773e-17, -6.89559039e-17,
                -2.20100417e-17,  2.38164572e-02,  7.62561269e-03,
                 3.21445095e-17,  1.03541228e-17, -2.17351169e-18,
                -2.90280578e-16,  4.13694335e-17, -1.02779359e-16,
                -9.00681388e-03,  1.24172712e-19,  3.88904577e-20,
                 3.62175334e-18,  4.97040200e-19, -4.59746502e-17,
                -1.49176773e-17,  6.89559039e-17,  2.20100417e-17,
                -2.38164572e-02, -7.62561269e-03, -3.21445095e-17,
                -1.03541228e-17
            ]}
        ),
        (
            'z', (0.5,),
            { ('z', 0.5): 
                [
                 2.20024508e-18,  3.47050269e-16, -5.77720802e-17,
                 1.52316173e-16,  1.39678165e-02, -1.25673969e-19,
                -3.93564842e-20, -4.17702276e-18, -5.65491588e-19,
                 5.76690683e-17,  1.81120190e-17, -8.87479495e-17,
                -2.72223318e-17,  3.12020089e-02,  9.54960337e-03,
                 4.17970193e-17,  1.28988397e-17, -2.14742014e-18,
                -2.49472444e-16,  3.22211936e-17, -7.75562394e-17,
                -6.64624257e-03,  1.22706898e-19,  3.84353386e-20,
                 3.19679039e-18,  4.43371191e-19, -3.82235003e-17,
                -1.26811547e-17,  5.63819361e-17,  1.84729966e-17,
                -1.92580535e-02, -6.34688454e-03, -2.61138382e-17,
                -8.64801891e-18
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
        ('x', 'x', (0,), {('x', 'x', 0): -3.905850683643e+00}),
        ('y', 'y', (0,), {('y', 'y', 0): -1.142145071013e+01}),
        ('z', 'z', (0,), {('z', 'z', 0): -4.258206719769e-02}),
        ('x', 'x', (0.5,), {('x', 'x', 0.5): -5.509763897604e+00}),
        ('y', 'y', (0.5,), {('y', 'y', 0.5): 3.988082514830e+00}),
        ('z', 'z', (0.5,), {('z', 'z', 0.5): -2.554873449850e-01}),
    ],
    ids=['xx0', 'yy0', 'zz0', 'xx0.5', 'yy0.5', 'zz0.5']
)
def test_lr(mod, qcp, args):
    aops, bops, freqs, expected = args
    lr = qcp.lr(aops, bops, freqs)
    for k, v in lr.items():
        npt.assert_allclose(v, expected[k], rtol=1e-4)
