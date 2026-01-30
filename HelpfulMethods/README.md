# Dependencies

* pip install numpy==1.19.5
* pip install SimpleITK==2.2.0
* pip install open3d==0.15.1

# Using the HelpfulMethods scripts

These scripts are standard Python utilities. Run them from the command line after installing the listed dependencies (they do not need to be loaded into 3D Slicer).

# Ventricles mesh export

The `ventricles_to_mesh.py` script converts the binary ventricles NIfTI images into a surface mesh.

Dependencies:
* pip install scikit-image==0.20.0

Example:
```bash
python HelpfulMethods/ventricles_to_mesh.py \
  Data/Brain/Patient1/ventricles.nii.gz \
  Outputs/ventricles_patient1.ply
```
