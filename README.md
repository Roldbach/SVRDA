# SVRDA: A Web-based Dataset Annotation Tool for Slice-to-Volume Registration


> **SVRDA: A Web-based Dataset Annotation Tool for Slice-to-Volume Registration**<br>
> Weixun Luo, Alexandre Triay Bagur, Paul Aljabar, George Ralli, Sir Michael Brady<br>
> Preprint
> 
> **Abstract** <br>
> **Background and Objective:** The lack of benchmark datasets has impeded the
> advancement of slice-to-volume registration algorithms. Such datasets are
> difficult to acquire primarily due to the dimensional discrepancy within data
> and the absence of task-specific software. We seek to develop a user-friendly
> tool to streamline the dataset annotation for slice-to-volume registration.<br>
>
> **Methods:** The proposed tool namely SVRDA is an installation-free web
> application for platform-independent collaborative dataset annotation. It
> enables efficient transformation manipulation via keyboard shortcuts and
> smooth case transitions with auto-saving. SVRDA also supports configuration-
> based data loading and adheres to the separation of concerns, offering great
> flexibility and extensibility for future research. Various supplementary
> features have been implemented to facilitate slice-to-volume registration.<br>
>
> **Results:** We validated the effectiveness of SVRDA by indirectly evaluating
> the post-registration segmentation quality on the UK Biobank data, observing
> in a dramatic overall improvement (24.02% in the Dice Similarity Coefficient
> and 48.93% in the 95th percentile Hausdorff distance respectively) supported
> by highly statistically significant evidence ($p < 0.001$). Also, we showcased
> the clinical usage of SVRDA by integrating it into test-retest T1
> quantification on in-house magnetic resonance acquisitions, leading to more
> consistent results after registration.<br>
>
> **Conclusions:** SVRDA can facilitate collaborative annotation of benchmark
> datasets while being potentially applicable to other pipelines incorporating
> slice-to-volume registration.<br>


## Description
- This repository contains the official implementation of *SVRDA: A Web-based
Dataset Annotation Tool for Slice-to-Volume Registration.* We have provided our
full source code and documentation here.


## Get Started
### Environment
- Please use Anaconda/Miniconda to set up the required environment using the
provided environment setup files.
    ```
    # 1. Go to the repository root directory.
    cd /repository_root_directory

    # 2. Choose a compatible setup file for your CPU.
    conda env create -f assets/environment/environment_linux_x86_64.yml
    conda env create -f assets/environment/environment_macOS_arm64.yml
    conda env create -f assets/environment/environment_macOS_intel_x86_64.yml

    # 3. Activate the environment.
    conda activate SVRDA
    ```
- Once the environment is activated, please manually replace the dash_vtk
package with [this version](./assets/dash_vtk) to enable proper coloring for
categorical 3D segmentation labels.
    ```
    # For users with Anaconda installed at $HOME:
    cp -r assets/dash_vtk $HOME/anaconda3/envs/SVRDA/lib/python3.10/site-packages

    # For users with Miniconda installed at $HOME:
    cp -r assets/dash_vtk $HOME/miniconda3/envs/SVRDA/lib/python3.10/site-packages
    ```
    - If Anaconda/Miniconda is not installed at **$HOME**, please replace it
    with the corresponding directory.
- For more information about this package, please refer to [here](./assets/dash_vtk/README.md).

### Dataset and Configuration
- Please prepare a dataset with the following structure:
    ```
    |-- dataset
        |-- case_1
        |   |-- <<body_sub_directory_name>>
        |   |   |-- *<<body_keyword_1>>*.nii.gz
        |   |   |-- *<<body_keyword_2>>*.nii.gz
        |   |   |-- ...
        |   |-- <<organ_sub_directory_name>>
        |   |   |-- *<<organ_keyword_1>>*.nii.gz
        |   |   |-- *<<organ_keyword_2>>*.nii.gz
        |   |   |-- ...
        |   |-- <<slice_sub_directory_name>>
        |   |   |-- *-a*.nii.gz
        |   |   |-- *-b*.nii.gz
        |   |   |-- *-c*.nii.gz
        |   |-- <<slice_mask_sub_directory_name>>  # Optional
        |   |   |-- *-a*.nii.gz
        |   |   |-- *-b*.nii.gz
        |   |   |-- *-c*.nii.gz
        |   |   |-- ...
        `-- case_2
        |   |-- <<body_sub_directory_name>>
        |   |   |-- *<<body_keyword_1>>*.nii.gz
        |   |   |-- *<<body_keyword_2>>*.nii.gz
        |   |   |-- ...
        |   |-- <<organ_sub_directory_name>>
        |   |   |-- *<<organ_keyword_1>>*.nii.gz
        |   |   |-- *<<organ_keyword_2>>*.nii.gz
        |   |   |-- ...
        |   |-- <<slice_sub_directory_name>>
        |   |   |-- *-a*.nii.gz
        |   |   |-- *-b*.nii.gz
        |   |   |-- *-c*.nii.gz
        |   |-- <<slice_mask_sub_directory_name>>  # Optional
        |   |   |-- *-a*.nii.gz
        |   |   |-- *-b*.nii.gz
        |   |   |-- *-c*.nii.gz
            `-- |-- ...
    ```
- Please modify the provided [configuration template](./assets/configuration_template.json)
to fit your dataset.
    - For example, if the target dataset looks like the following and is located
    at **/home/sample_dataset**:
        ```
        |-- sample_dataset
            |-- case_1
            |   |-- volume
            |   |   |-- volume-1.nii.gz
            |   |   |-- volume-2.nii.gz
            |   |   |-- ...
            |   |-- organ
            |   |   |-- organ-1.nii.gz
            |   |   |-- organ-2.nii.gz
            |   |   |-- ...
            |   |-- slice
            |   |   |-- slice-a.nii.gz
            |   |   |-- slice-b.nii.gz
            |   |   |-- slice-c.nii.gz
            |-- case_2
            |   |-- volume
            |   |   |-- volume-1.nii.gz
            |   |   |-- volume-2.nii.gz
            |   |   |-- ...
            |   |-- organ
            |   |   |-- organ-1.nii.gz
            |   |   |-- organ-2.nii.gz
            |   |   |-- ...
            |   |-- slice
            |   |   |-- slice-a.nii.gz
            |   |   |-- slice-b.nii.gz
            |   |   |-- slice-c.nii.gz
                `-- |-- ...
            ```
    - Then, the corresponding configuration file could be:
        ```
        {
            "dataset_directory_path": "/home/dataset/sample_dataset",  # path to the dataset root
                                                                       # directory
            "directory_name": {
                "body": "volume"    # name of the directory that contains 3D volumes
                "organ": "organ",   # name of the directory that contains 3D segmentation labels
                "organ_resampled": "organ_resampled",  # name of the directory that 2D resampled
                                                       # segmentation labels are saved
                "slice": "slice",   # name of the directory that contains 2D slices
                "slice_mask": "null"    # name of the directory that contains 2D masks defining the
                                        # region of interest for corresponding 2D slices (optional).
            },
            "file_name": {
                "transformation": "transformation"   # name of the file that contains transformation
                                                     # parameters for all 2D slices in a case
            },
            "pattern": {
                "body": "*-1*",     # regex that only matches the required 3D volume
                "organ": "*-2*",    # regex that only matches the required 3D segmentation label
                "slice": "slice-*", # regex that only matches the required 2D slices
                "slice_mask": "null"   # regex that only matches the required 2D masks defining the
                                       # region of interest for corresponding 2D slices (optional)
            },
            "tag": {
                "organ_resampled": "-resampled"   # tag used to build file names for 2D resampled
                                                  # segmentation labels
            },
        }
        ```

### Start Up
- The GUI can be started in the following ways:
    - Passing the configuration file path as an argument:
    ```
    python app.py -c /configuration_file_path
    python app.py --configuration /configuration_file_path
    ```
    - Without passing the configuration file path as an argument (and uploading
    through Home Page later):
    ```
    python app.py
    ```
- Once the GUI is successfully started (or is running on a remote machine),
please go the URL specified in the terminal.
    ```
    Dash is running on http://127.0.0.1:8050/  # On local laptops
    Dash is running on http://A.B.C.D:8050/  # On the remote machine
    ```
where `A.B.C.D` is the remote IP address.

### Transformation ###
- Currently, **rigid transformations** can be applied to 2D quantitative
parametric maps to adjust their positions. These include translation and
rotation in the x, y, z axis for a total of **6** degrees of freedom.
- Scanner Coordinate System (static) used in the GUI coincides with the
**NiFTI** coordinate system , which has the directional code **LAS**.
- Slice Coordinate System (dynamic) used in the GUI depends on the
**real-time** orientation of **the selected 2D quantitative parametric map**.

### Transformation Control ###
- Transformations can be controlled using the following keyboard shortcuts:
    - Translations in Scanner Coordinate System:
        - x axis: **a**, **d**
        - y axis: **w**, **s**
        - z axis: **q**, **e**
    - Translations in Slice Coordinate System:
        - x axis: **j**, **l**
        - y axis: **i**, **k**
        - z axis: **u**, **o**
    - Rotations in Slice Coordinate System:
        - x axis: **Shift + W**, **Shift + S**
        - y axis: **Shift + A**, **Shift + D**
        - z axis: **Shift + Q**, **Shift + E**

### Mode ###
- We introduce different modes to allow flexible control of transformations.
    - Macro Mode
        - **All 2D quantitative parametric maps** are visible within the 3D plot.
        - Transformations can be applied to **all 2D quantitative parametric
        maps** as group effects.
        - Rotations are done in **Scanner Coordinate System** only and **the
        mean centroid of all 2D quantitative parametric maps** is chosen as the
        rotation centre.
    - Micro Mode
        - Only **the selected 2D quantitative parametric map** is visible within
        the 3D plot.
        - Transformations can only be applied to **the selected 2D quantitative
        parametric map**.
        - Rotations are done in **Slice Coordinate System** depending on the
        selected 2D quantitative parametric map and its **centroid** is chosen as
        the rotation centre.

### Evaluation ###
- Evaluation are served as a support to help users determine whether 2D
quantitative parametric maps are well aligned with the 3D volume at the current
position or not.
- Evaluation is done by measuring the similarity/difference between **the
selected 2D quantitative map** and **the corresponding 2D resampled image from
the 3D volume**.
- For manual registration, we encourage users to mainly rely on exptertise and
knowledge during decision making and only use this as a supplementary reference.
- The following evaluation metrics are available in the GUI:
    - Normalised Mutual Information (NMI): A **similarity** measurement that
    measures the mutual dependence between 2 images. This is recommended for
    **multi-modal data**.
    - Sum of Absolute Difference (SAD): A **difference** measurement that
    measures the pixel-wise difference between 2 images.

### Case Control ###
- To shift to a new case, you could:
    - use **Previous** and **Next** buttons to go through each case one-by-one.
    - click the dropdown showing the current case id and select the new case id.
- The current case is **auto-saved** before shifting to a new case.
- **Please notice that directly closing the browser won't save the current case.
To save the last case, please manually press the Save button.**

### Note ###
- Dash reports exceptions at the bottom right corner. **It is fine to have "ID not found in layout" error.**

