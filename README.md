# MDF-Inspired Thermal Distortion Compensation

A practical geometric compensation workflow for estimating and counteracting manufacturing distortion from point-cloud data.

Inspired by the **Material Deformation Finding (MDF)** framework, this project combines probabilistic registration, iterative displacement estimation, and pre-compensation in a compact computational pipeline for additive-manufacturing distortion studies.

## Highlights

- **Point-cloud distortion registration** between nominal and manufactured geometry
- **Probabilistic correspondence estimation** for noisy geometric observations
- **Iterative displacement recovery** to estimate systematic shape error
- **Geometric pre-compensation** based on the recovered distortion
- **Self-contained synthetic benchmark** with controlled warping, noise, visualization, and error evaluation

`mdf.py` generates a nominal planar geometry, applies a nonlinear manufacturing-style warping field, estimates the displacement needed to recover alignment, reports nearest-neighbor MSE, and visualizes the nominal, distorted, and corrected geometries.

## Workflow

1. Generate or load the nominal design point cloud.
2. Obtain a distorted manufactured/scan point cloud.
3. Estimate probabilistic correspondence between the two geometries.
4. Iteratively recover the displacement that aligns the nominal and distorted shapes.
5. Use the estimated distortion as a basis for geometric compensation.
6. Evaluate residual geometric error after alignment/compensation.

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python mdf.py
```

## Main functions

- `generate_flat_point_cloud(...)` — creates the nominal reference geometry.
- `simple_warping_function(...)` — defines a controlled nonlinear distortion field.
- `realistic_manufacture_shape(...)` — simulates manufacturing distortion and noise.
- `mdf_align(...)` — performs probabilistic deformation registration.
- `compute_mse(...)` — evaluates nearest-neighbor geometric error.

## Research context

The workflow is motivated by:

> C. Wang, S. Li, D. Zeng, X. Zhu,  
> *Quantification and compensation of thermal distortion in additive manufacturing: A computational statistics approach*,  
> Computer Methods in Applied Mechanics and Engineering, 375, 2021.  
> DOI: https://doi.org/10.1016/j.cma.2020.113611

The repository is useful as a compact platform for testing distortion-registration ideas, compensation strategies, synthetic deformation scenarios, and extensions toward richer non-rigid manufacturing-response models.

## Implementation note

The current `mdf_align()` routine uses the probabilistic/EM registration structure with a global displacement update. The reference MDF formulation extends this idea to a spatially varying non-rigid deformation field with kernel regularization. That richer field model is a natural extension of the workflow implemented here.
