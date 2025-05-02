"""
Material Deformation Finding (MDF) Algorithm Implementation
===========================================================

This script implements a simplified statistical alignment method
inspired by the MDF approach described in:

Chao Wang, Shaofan Li, Danielle Zeng, Xinhai Zhu,
"Quantification and compensation of thermal distortion in additive manufacturing:
 A computational statistics approach", CMAME 2021, DOI: 10.1016/j.cma.2020.113611.

License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree


def generate_flat_point_cloud(Lx, Ly, spacing):
    """
    Generate a 2D grid of points in the XY plane with zero Z elevation.

    Parameters:
        Lx (float): Width of the grid in X direction.
        Ly (float): Height of the grid in Y direction.
        spacing (float): Distance between points.

    Returns:
        np.ndarray: (N, 3) array of points on a flat surface.
    """
    x, y = np.meshgrid(np.arange(-Lx/2, Lx/2+spacing, spacing),
                       np.arange(-Ly/2, Ly/2+spacing, spacing))
    z = np.zeros_like(x)
    return np.column_stack((x.flatten(), y.flatten(), z.flatten()))


def simple_warping_function(x, y, B=2.0, Lx=200, Ly=100):
    """
    Define a simple quadratic warping function simulating distortion.

    Parameters:
        x, y (np.ndarray): X and Y coordinates.
        B (float): Warping magnitude.
        Lx, Ly (float): Normalization lengths.

    Returns:
        np.ndarray: Warped Z values.
    """
    return B * ((x / Lx)**2 + (y / Ly)**2)


def realistic_manufacture_shape(points, compensation_z,
                                nonlinearity=0.0, noise_std=0.0):
    """
    Simulate a manufactured shape with distortion, nonlinearity, and noise.

    Parameters:
        points (np.ndarray): (N, 3) array of input points.
        compensation_z (np.ndarray): Compensation Z-displacement at each point.
        nonlinearity (float): Degree of nonlinear distortion.
        noise_std (float): Standard deviation of Gaussian noise.

    Returns:
        np.ndarray: Z coordinates of manufactured (distorted) shape.
    """
    warp_z = simple_warping_function(points[:, 0], points[:, 1])
    nonlinear_effect = nonlinearity * compensation_z**2 * np.sign(compensation_z)
    noise = np.random.normal(0, noise_std, size=points.shape[0])
    return warp_z + compensation_z - nonlinear_effect + noise


def compute_mse(source_points, target_points):
    """
    Compute mean squared error (MSE) between two point clouds using nearest neighbors.

    Parameters:
        source_points (np.ndarray): (N, 3) source cloud.
        target_points (np.ndarray): (M, 3) target cloud.

    Returns:
        float: Mean squared distance.

    Raises:
        ValueError: If input contains NaN or Inf.
    """
    if not np.isfinite(source_points).all() or not np.isfinite(target_points).all():
        raise ValueError("NaN or Inf detected in input data.")
    tree = cKDTree(target_points)
    dists, _ = tree.query(source_points, k=1)
    return np.mean(dists**2)


def mdf_align(design_pts, scanned_pts,
              max_iter=30, w=0.05, alpha=2.0, beta=20.0, tol=1e-5):
    """
    Aligns design points to scanned points using MDF-inspired EM approach.

    Parameters:
        design_pts (np.ndarray): (N, 3) design/reference point cloud.
        scanned_pts (np.ndarray): (M, 3) scanned/distorted point cloud.
        max_iter (int): Maximum EM iterations.
        w (float): Weight of uniform noise distribution (outlier handling).
        alpha (float): Regularization strength (unused here, placeholder).
        beta (float): Gaussian kernel width for smoothing.
        tol (float): Convergence tolerance for sigma².

    Returns:
        Tuple[np.ndarray, np.ndarray]: (aligned_points, displacement vectors)
    """
    N, M = design_pts.shape[0], scanned_pts.shape[0]
    displacement = np.zeros_like(design_pts)

    # Estimate initial sigma² from random subset
    count = min(N, M)
    rand_ids = np.random.choice(count, size=count, replace=False)
    dist_init = np.sum((design_pts[rand_ids] - scanned_pts[rand_ids])**2, axis=1)
    sigma2 = max(np.mean(dist_init), 1e-8)

    # Kernel matrix for scanned points
    diff_scanned = scanned_pts[:, None, :] - scanned_pts[None, :, :]
    dist2 = np.sum(diff_scanned**2, axis=2)
    G = np.exp(-dist2 / (2.0 * beta**2))
    eyeM = np.eye(M)

    for it in range(max_iter):
        offset = np.mean(scanned_pts, axis=0) - np.mean(design_pts + displacement, axis=0)
        aligned_simple = scanned_pts + offset

        diff = (design_pts[:, None, :] + displacement[:, None, :]) - aligned_simple[None, :, :]
        dist2 = np.sum(diff**2, axis=2)

        c = (2.0 * np.pi * sigma2)**1.5 * (w / (1.0 - w)) * float(M)/float(N)
        P = np.exp(-dist2 / (2.0 * sigma2))
        denom = np.sum(P, axis=1, keepdims=True) + c
        denom[denom <= 1e-12] = 1e-12
        P = P / denom

        Pt1 = np.sum(P, axis=0)
        P1 = np.sum(P, axis=1)
        Np = np.sum(Pt1)

        x_disp = design_pts + displacement
        muX = (1.0 / Np) * np.sum(x_disp * P1[:, None], axis=0)
        muY = (1.0 / Np) * np.sum(scanned_pts * Pt1[:, None], axis=0)
        new_offset = muY - muX
        displacement += new_offset

        # Update sigma²
        x_hat = design_pts + displacement
        dist2_new = np.sum(P * np.sum((x_hat[:, None, :] - scanned_pts[None, :, :])**2, axis=2))
        sigma2_new = max(dist2_new / (3.0 * Np), 1e-12)

        if abs(sigma2 - sigma2_new) < tol:
            break
        sigma2 = sigma2_new

    aligned_pts = design_pts + displacement
    return aligned_pts, displacement


# ===============================
# Example usage / test script
# ===============================
if __name__ == "__main__":
    # Generate synthetic design point cloud
    Lx, Ly, spacing = 200, 100, 20
    design_cloud = generate_flat_point_cloud(Lx, Ly, spacing)

    # Simulate printed shape with distortion
    compensation_z = np.full(design_cloud.shape[0], 5.0)
    manufactured_z = realistic_manufacture_shape(design_cloud, compensation_z,
                                                 nonlinearity=0.02, noise_std=0.5)
    scanned_cloud = design_cloud.copy()
    scanned_cloud[:, 2] = manufactured_z

    # Apply MDF alignment
    aligned_points, disp = mdf_align(design_cloud, scanned_cloud)

    # Compute and print alignment error
    try:
        mse_val = compute_mse(aligned_points, scanned_cloud)
        print(f"Final alignment MSE = {mse_val:.4f}")
    except ValueError as e:
        print("MSE computation failed:", e)

    # Plot results
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_title("Scanned (blue) vs Original (red)")
    ax1.scatter(scanned_cloud[:, 0], scanned_cloud[:, 1], scanned_cloud[:, 2], s=10, c='blue')
    ax1.scatter(design_cloud[:, 0], design_cloud[:, 1], design_cloud[:, 2], s=20, c='red')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_title("Scanned (blue) vs Aligned (green)")
    ax2.scatter(scanned_cloud[:, 0], scanned_cloud[:, 1], scanned_cloud[:, 2], s=10, c='blue')
    ax2.scatter(aligned_points[:, 0], aligned_points[:, 1], aligned_points[:, 2], s=20, c='green')

    for ax in [ax1, ax2]:
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
    plt.tight_layout()
    plt.show()
