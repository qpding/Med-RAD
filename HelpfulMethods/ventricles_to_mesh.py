#!/usr/bin/env python3
"""Convert ventricles binary NIfTI images into a mesh file."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import open3d as o3d
import SimpleITK as sitk
from skimage import measure


def load_volume(path: Path) -> tuple[np.ndarray, sitk.Image]:
    image = sitk.ReadImage(str(path))
    volume = sitk.GetArrayFromImage(image)
    return volume, image


def build_mesh(volume: np.ndarray, image: sitk.Image, level: float) -> o3d.geometry.TriangleMesh:
    verts, faces, _, _ = measure.marching_cubes(volume, level=level)
    ijk = np.column_stack((verts[:, 2], verts[:, 1], verts[:, 0]))
    verts_phys = np.array([image.TransformContinuousIndexToPhysicalPoint(v.tolist()) for v in ijk])

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(verts_phys)
    mesh.triangles = o3d.utility.Vector3iVector(faces.astype(np.int32))
    mesh.compute_vertex_normals()
    return mesh


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a binary ventricles NIfTI image into a surface mesh.",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the ventricles NIfTI image (e.g., Data/Brain/Patient1/ventricles.nii.gz).",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Path to write the mesh file (e.g., ventricles.ply or ventricles.stl).",
    )
    parser.add_argument(
        "--level",
        type=float,
        default=0.5,
        help="Marching cubes isosurface level for binary data (default: 0.5).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    volume, image = load_volume(args.input)

    if volume.max() <= 0:
        raise ValueError("Input volume appears to be empty (no positive voxels).")

    mesh = build_mesh(volume, image, args.level)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    if not o3d.io.write_triangle_mesh(str(args.output), mesh):
        raise RuntimeError(f"Failed to write mesh to {args.output}")

    print(f"Saved mesh with {len(mesh.vertices)} vertices and {len(mesh.triangles)} faces to {args.output}")


if __name__ == "__main__":
    main()
