This repository contains a implementation of the **Material Deformation Finding (MDF)** algorithm proposed in:

> C. Wang, S. Li, D. Zeng, X. Zhu,  
> *Quantification and compensation of thermal distortion in additive manufacturing: A computational statistics approach*,  
> Computer Methods in Applied Mechanics and Engineering, Vol. 375, 2021.  
> [DOI: 10.1016/j.cma.2020.113611](https://doi.org/10.1016/j.cma.2020.113611)

The MDF algorithm is a data-driven, statistical method for quantifying thermal distortion in 3D printed parts. Input is:

The original design geometry (e.g., STL file),

A 3D scan of the distorted printed part.

It then uses a Gaussian Mixture Model-based registration approach, extended from the Coherent Point Drift method, to compute a smooth, continuous deformation field. This allows generating a compensated design that counteracts thermal distortion — enabling more accurate 3D printing without trial-and-error.

