[![codecov](https://codecov.io/gh/West-Coast-Differentiators/cs107-FinalProject/branch/master/graph/badge.svg?token=CVUJ0SI09S)](https://codecov.io/gh/West-Coast-Differentiators/cs107-FinalProject)
[![Build Status](https://travis-ci.com/West-Coast-Differentiators/cs107-FinalProject.svg?token=LcEGi8DXzVyEeNU9JqUx&branch=master)](https://travis-ci.com/West-Coast-Differentiators/cs107-FinalProject)

# cs107-FinalProject

## Group 14
* Anita Mahinpei
* Yingchen Liu
* Erik Adames
* Lekshmi Santhosh


# Project description

Our package contains several optimization algorithms that are ubiquitous in machine learning. In the context of the WestCoastAD package, an optimization problem refers to the minimization of a function. Below are the optimization that are currently included in this package:
  * Gradient Descent
  * Momentum Gradient Descent
  * AdaGrad
  * RMSprop
  * Adam
  * BFGS

All the optimization methods mentioned above require derivative computations. For this library, we have used Automatic Differentiation as it is an efficient way of computing these derivatives which can be used with various complex functions.