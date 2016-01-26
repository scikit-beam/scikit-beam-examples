
1-time correlation
==================

Included files
--------------
1. [Multi_tau_one_time_correlation_example.ipynb] (https://github.com/scikit-beam/scikit-beam-examples/blob/master/demos/time_correlation/Multi_tau_one_time_correlation_example.ipynb)
    is an example notebook that demonstrates using the one-time correlation functions in [scikit-beam](https://github.com/scikit-beam/scikit-beam).
1. ``100_500_NIPA_GEL.npy`` is a pickled numpy dataset from @afluerasu that
   is used in the time correlation demo.
1. [XPCS fitting] (https://github.com/scikit-beam/scikit-beam-examples/blob/master/demos/time_correlation/XPCS_fitting_with_lmfit.ipynb)
   is an example notebook that demonstrates XPCS data which are fitted with intermediate scattering factor model function in [scikit-beam](https://github.com/scikit-beam/scikit-beam)
   using [lmfit Model] (http://lmfit.github.io/lmfit-py/model.html).
1. [Two time correlation] (https://github.com/scikit-beam/scikit-beam-examples/blob/master/demos/time_correlation/two-time-correlation.ipynb
   is an example notebook that demonstrates two time correlation function in [scikit-beam](https://github.com/scikit-beam/scikit-beam).
1. [Partial multi tau] (https://github.com/scikit-beam/scikit-beam-examples/blob/master/demos/time_correlation/partial-multi-tau.ipynb)
    is an example notebook that demonstrates the multi tau correlation function use partial data.
1. [Removing bad images - one time correlation] (https://github.com/sameera2004/scikit-beam-examples/blob/bad_imgs_correlation/demos/time_correlation/Removing_bad_images_one_time_correlation.ipynb)
    is an example notebook that demonstrates removing bad images for one time correlation analysis
1. [Check removing bad images using the same image 10000 times - one time correlation] (https://github.com/sameera2004/scikit-beam-examples/blob/bad_imgs_correlation/demos/time_correlation/Check_remove_bad_imgs_using_same_image.ipynb)
    is an example notebook that compare the results with no bad images and with bad images using the same image repeated for 10000 times

Relevant papers
---------------
1. Describing one-time correlation (especially the normalization used in the
   scikit-beam library function)
   - D. Lumma, L. B. Lurio, S. G. J. Mochrie and M. Sutton, "Area detector
     based photon correlation in the regime of short data batches: Data 
     reduction for dynamic x-ray scattering," Rev. Sci. Instrum., vol 70,  
     p3274-3289, 2000.
1. Multi-tau scheme for 1-time correlation
   - K. Schätzela, M. Drewela and  S. Stimaca, "Photon correlation 
     measurements at large lag times: Improving statistical accuracy," J. Mod.
     Opt., vol 35,p 711–718, 1988.
1. Intermediate scattering factor
   - L. Li, P. Kwasniewski, D. Orsi, L. Wiegart, L. Cristofolini,
     C. Caronna and A. Fluerasu, " Photon statistics and speckle
     visibility spectroscopy with partially coherent X-rays,"
     J. Synchrotron Rad., vol 21, p 1288-1295, 2014.
1. Two time correklation
   - A. Fluerasu, A. Moussaid, A. Mandsen and A. Schofield,
     "Slow dynamics and aging in collodial gels studied by x-ray photon
      correlation spectroscopy," Phys. Rev. E., vol 76, p 010401(1-4), 2007.