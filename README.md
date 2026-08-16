# MDF-Inspired Thermal Distortion Compensation Prototype

This repository provides a practical **MDF-inspired deformation-registration prototype** for exploring geometric distortion estimation and compensation in additive manufacturing.

The workflow is motivated by the Material Deformation Finding (MDF) framework introduced in:

> C. Wang, S. Li, D. Zeng, X. Zhu,  
> *Quantification and compensation of thermal distortion in additive manufacturing: A computational statistics approach*,  
> Computer Methods in Applied Mechanics and Engineering, Vol. 375, 2021.  
> DOI: https://doi.org/10.1016/j.cma.2020.113611

## What this repository demonstrates

The prototype captures the main computational idea behind deformation-registration-based compensation:

1. represent the nominal design and manufactured geometry as point clouds;
2. establish probabilistic correspondence between the two geometries;
3. iteratively estimate the displacement needed to align the design with the distorted shape;
4. evaluate the recovered deformation using nearest-neighbor geometric error;
5. use the estimated displacement as the basis for geometric compensation.

`mdf.py` includes a self-contained synthetic example that generates a flat design, applies a controlled warping field, performs probabilistic alignment, reports the final mean-squared registration error, and visualizes the result.

## Scope relative to the full MDF method

This repository is a **compact MDF-inspired implementation**, not a line-by-line reproduction of the complete algorithm in Wang et al. The current alignment routine uses the probabilistic/EM registration structure but a simplified global displacement update. The full paper develops a non-rigid material deformation field with spatial kernel regularization and additional model updates that are outside the scope of this prototype.

This makes the repository useful for studying the registration and compensation workflow, testing synthetic distortion scenarios, and prototyping extensions before moving to a full non-rigid formulation.

## Installation

```bash
python -m pip install numpy scipy matplotlib
```

## Run the example

```bash
python mdf.py
```

The script will:

- generate a synthetic design point cloud;
- apply quadratic warping, optional nonlinearity, and noise;
- estimate the alignment displacement;
- print the final nearest-neighbor MSE;
- display the original, scanned, and aligned point clouds.

## Main functions

- `generate_flat_point_cloud(...)` — creates the synthetic reference geometry.
- `simple_warping_function(...)` — defines a controlled distortion field.
- `realistic_manufacture_shape(...)` — simulates distorted manufacturing output.
- `mdf_align(...)` — performs the MDF-inspired probabilistic alignment.
- `compute_mse(...)` — evaluates nearest-neighbor geometric error.

## Research use

The code is intended as a lightweight research prototype for geometric compensation studies. For quantitative comparison with the published MDF method, the full non-rigid kernel-based formulation should be implemented and validated against the reference paper.
