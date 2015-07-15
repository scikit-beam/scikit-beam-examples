from __future__ import absolute_import, division, print_function

def test_xrf_spectrum_demo():
    # smoketest the demo
    from xrf.demo_xrf_spectrum import run_demo
    import matplotlib.pyplot as plt
    plt.ion()
    run_demo()

def test_reciprocal_space():
    from reciprocal_space import recip_example
