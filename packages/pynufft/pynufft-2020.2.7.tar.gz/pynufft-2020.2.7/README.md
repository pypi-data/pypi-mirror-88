# PyNUFFT: Python non-uniform fast Fourier transform
![](g5738.jpeg)

A minimal "getting start" tutorial is available at http://jyhmiinlin.github.io/pynufft/ . This package reimplements the min-max interpolator (Fessler, Jeffrey A., and Bradley P. Sutton. "Nonuniform fast Fourier transforms using min-max interpolation." IEEE transactions on signal processing 51.2 (2003): 560-574.) for Python.

Please cite Lin, Jyh-Miin. "Python non-uniform fast Fourier transform (PyNUFFT): An accelerated non-Cartesian MRI package on a heterogeneous platform (CPU/GPU)." Journal of Imaging 4.3 (2018): 51.

and or

Jyh-Miin Lin and Hsiao-Wen. Chung, Pynufft: python non-uniform fast Fourier transform for MRI Building Bridges in Medical Sciences 2017, St John’s College, CB2 1TP Cambridge, UK. 

You can also find other very useful Python nufft/nfft functions at: 

1. SigPy (Ong, F., and M. Lustig. "SigPy: a python package for high performance iterative reconstruction." Proceedings of the ISMRM 27th Annual Meeting, Montreal, Quebec, Canada. Vol. 4819. 2019. Note the order starts from the last axis), https://sigpy.readthedocs.io/en/latest/generated/sigpy.nufft.html?highlight=nufft
2. gpuNUFFT: (Knoll, Florian, et al. "gpuNUFFT-an open source GPU library for 3D regridding with direct Matlab interface." Proceedings of the 22nd annual meeting of ISMRM, Milan, Italy. 2014.): https://github.com/andyschwarzl/gpuNUFFT/tree/master/python
3. mrrt.nufft (mrrt.mri demos for the ISMRM 2020 Data Sampling Workshop in Sedona, AZ with raw cuda kernels): https://github.com/mritools/mrrt.nufft
4. pyNFFT (Keiner, J., Kunis, S., and Potts, D. ''Using NFFT 3 - a software library for various nonequispaced fast Fourier transforms'' ACM Trans. Math. Software,36, Article 19, 1-30, 2009. The python wrapper of NFFT): https://pythonhosted.org/pyNFFT/tutorial.html
5. finufft (Barnett, Alexander H., Jeremy Magland, and Ludvig af Klinteberg. "A Parallel Nonuniform Fast Fourier Transform Library Based on an “Exponential of Semicircle" Kernel." SIAM Journal on Scientific Computing 41.5 (2019): C479-C504., exponential semicircle kernel): https://finufft.readthedocs.io/en/latest/python.html
6. torchkbnufft (M. J. Muckley, R. Stern, T. Murrell, F. Knoll, TorchKbNufft: A High-Level, Hardware-Agnostic Non-Uniform Fast Fourier Transform, 2020 ISMRM Workshop on Data Sampling and Image Reconstruction): https://github.com/mmuckley/torchkbnufft
7. tfkbnufft (adapt torchkbnufft for TensorFlow): https://github.com/zaccharieramzi/tfkbnufft
8. TFNUFFT (adapt the min-max interpolator in PyNUFFT for tensorflow): https://github.com/yf0726/TFNUFFT

## Installation

$ pip install pynufft --user


### Using Numpy/Scipy

```
$ python
Python 3.6.11 (default, Aug 23 2020, 18:05:39) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pynufft import NUFFT
>>> import numpy
>>> A = NUFFT()
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> Kd = (128,128)
>>> Jd = (6,6)
>>> A.plan(om, Nd, Kd, Jd)
0
>>> x=numpy.random.randn(*Nd)
>>> y = A.forward(x)
```

### Using PyCUDA

```
>>> from pynufft import NUFFT, helper
>>> import numpy
>>> A2= NUFFT(helper.device_list()[0])
>>> A2.device
<reikna.cluda.cuda.Device object at 0x7f9ad99923b0>
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> Kd = (128,128)
>>> Jd = (6,6)
>>> A2.plan(om, Nd, Kd, Jd)
0
>>> x=numpy.random.randn(*Nd)
>>> y = A2.forward(x)
```

### Using NUDFT (double precision)

Some users ask for double precision. 
NUDFT is offered.

```
>>> from pynufft import  NUDFT
>>> import numpy
>>> x=numpy.random.randn(*Nd)
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> A = NUDFT()
>>> A.plan(om, Nd)
>>> y_cpu = A.forward(x)

```


## Testing GPU acceleration

```
Python 3.6.11 (default, Aug 23 2020, 18:05:39) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pynufft import tests
>>> tests.test_init(0)
device name =  <reikna.cluda.cuda.Device object at 0x7f41d4098688>
0.06576069355010987
0.006289639472961426
error gx2= 2.0638987e-07
error gy= 1.0912560261408778e-07
acceleration= 10.455399523742015
17.97926664352417 2.710083246231079
acceleration in solver= 6.634211944790991
```
### Comparisons

![](Figure_1.png)



### On the RRSG challenge of reproducible research in ISMRM 2019

The RRSG Challenge aims to reproduce the CG-SENSE paper (Pruessmann KP, Weiger M, Börnert P, Boesiger P. Advances in Sensitivity Encoding With Arbitrary k-Space Trajectories.
Magnetic Resonance in Medicine 2001;(46):638–651.).

Actually, PyNUFFT does not fail in this challenge. Our result is as follows. (The code is available on request)

The basic idea is to extract the coil sensitivity profiles from the center of k-space (as the ACS in ESPIRiT).

The problem is ill-conditioned. The square root of the sampling-density compensation function D<sup>1/2</sup> is needed. 

A nice feature about Scipy/Numpy is that we can build a scipy.sparse.LinearOperator.

This LinearOperator allows the problem to be solved by scipy.sparse.linalg.lsmr or scipy.sparse.linalg.lsqr. (Normal equation is not used in this case)

![](with_espirit.png)

### Cartesian k-space?

If you insist to use NUFFT, please see https://jyhmiinlin.github.io/pynufft/manu/realistic_om.html#cartesian-k-space

The numerical accuracy is 6.0265739765301084e-06 for single-precision. 

Other methods may cause suboptimal results.

### Contact information
J.-M. Lin
email: pynufft@gamil.com

