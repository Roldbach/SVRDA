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
        |   |   |-- *<<slice_keyword_1>>*.nii.gz
        |   |   |-- *<<slice_keyword_2>>*.nii.gz
        |   |   |-- ...
        |   |-- <<slice_mask_sub_directory_name>>  # Optional
        |   |   |-- *<<slice_mask_keyword_1>>*.nii.gz
        |   |   |-- *<<slice_mask_keyword_2>>*.nii.gz
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
        |   |   |-- *<<slice_keyword_1>>*.nii.gz
        |   |   |-- *<<slice_keyword_2>>*.nii.gz
        |   |   |-- ...
        |   |-- <<slice_mask_sub_directory_name>>  # Optional
        |   |   |-- *<<slice_mask_keyword_1>>*.nii.gz
        |   |   |-- *<<slice_mask_keyword_2>>*.nii.gz
            `-- |-- ...
    ```
- Please modify the provided [configuration template](./assets/configuration_template.json)
to fit your dataset.
    - For example, if the target dataset looks like the following and is located
    at **/home/sample_dataset**:
        ```
        |-- sample_dataset
            |-- case_1
            |   |-- body
            |   |   |-- body-1.nii.gz
            |   |   |-- body-2.nii.gz
            |   |-- organ
            |   |   |-- organ-1.nii.gz
            |   |   |-- organ-2.nii.gz
            |   |-- slice
            |   |   |-- slice-a.nii.gz
            |   |   |-- slice-b.nii.gz
            |   |   |-- slice-c.nii.gz
            |-- case_2
            |   |-- body
            |   |   |-- body-1.nii.gz
            |   |   |-- body-2.nii.gz
            |   |-- organ
            |   |   |-- organ-1.nii.gz
            |   |   |-- organ-2.nii.gz
            |   |-- slice
            |   |   |-- slice-a.nii.gz
            |   |   |-- slice-b.nii.gz
                `-- |-- slice-c.nii.gz
        ```
    - Then, the corresponding configuration file could be:
        ```
        {
            "dataset_directory_path": "/home/dataset/sample_dataset",  # path to the dataset root
                                                                       # directory
            "directory_name": {
                "body": "body"      # name of the directory that contains 3D volumes
                "organ": "organ",   # name of the directory that contains 3D segmentation labels
                "organ_resampled": "organ_resampled",  # name of the directory that 2D resampled
                                                       # segmentation labels are to be saved
                "slice": "slice",   # name of the directory that contains 2D slices
                "slice_mask": "null"    # name of the directory that contains binary masks defining
                                        # the region of interest for corresponding 2D slices
                                        # (optional).
            },
            "file_name": {
                "transformation": "transformation"   # name of the file that contains transformation
                                                     # parameters for all 2D slices in a case
            },
            "pattern": {
                "body": "*-1*",     # regex that matches the required 3D volume (e.g., body-1.nii.gz)
                "organ": "*-2*",    # regex that matches the required 3D segmentation label
                                    # (e.g., organ-2.nii.gz)
                "slice": "slice-*", # regex that matches the required 2D slices
                                    # (e.g., slice-a/b/c.nii.gz)
                "slice_mask": "null"   # regex that matches the required binary masks defining the
                                       # region of interest for corresponding 2D slices (e.g., null)
            },
            "tag": {
                "organ_resampled": "-resampled"   # tag used to synthesize file names for 2D
                                                  # resampled segmentation labels
            },
        }
        ```

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

### Start Up
- Please choose one from the following commands to run SVRDA:
    ```
    python app.py
    python app.py -c /configuration_file_path
    python app.py --configuration /configuration_file_path
    ```
- Once the GUI is running, please go the URL specified in the terminal.
    ```
    Dash is running on http://127.0.0.1:8050/  # On the local server
    Dash is running on http://A.B.C.D:8050/  # On the remote server
    ```
where the specific IP addresses can be customized [here](app.py)


## Important Features
### Transformation
- **Rigid transformations** with six degrees of freedom (three translation and
three rotation parameters) can be applied to adjust the poses of 2D slices.
- Transformations can be computed with respect to:
    - Patient Coordinate System: A static RAS+ coordinate system
    - Slice Coordinate System: A dynamic coordinate system based on the
    real-time pose of the currently selected slice
- Please control transformations using the following keyboard shortcuts:
    - Translations in the Patient Coordinate System:
        - x axis: **a**, **d**
        - y axis: **w**, **s**
        - z axis: **q**, **e**
    - Translations in the Slice Coordinate System:
        - x axis: **j**, **l**
        - y axis: **i**, **k**
        - z axis: **u**, **o**
    - Rotations in the Slice Coordinate System:
        - x axis: **Shift+W**, **Shift+S**
        - y axis: **Shift+A**, **Shift+D**
        - z axis: **Shift+Q**, **Shift+E**

### Mode
- Modes are introduced to adjust the granularity of transformation control:
    - Macro Mode
        - **All 2D slices** are visible.
        - Transformations are applied to **all 2D slices** simultaneously.
    - Micro Mode
        - Only **the selected 2D slice** is visible.
        - Transformations are exclusively applied to **the selected 2D slice**.

### Alignment Quantification
- The alignment between data is quantitatively monitored in real-time by
measuring the difference between the selected slice and its corresponding 2D
cross-section image resampled from the 3D volume.
- The following evaluation metrics have been implemented:
    - Normalised Mutual Information (NMI): A **similarity** metric that measure
    the ratio of the sum of the marginal entropy between the images.
    - Sum of Absolute Difference (SAD): A **difference** metric that measures
    the sum of the absolute difference between pixel values between the images.

### Case and Saving
- To shift to a new case, please:
    - use **Previous/Next** buttons to go through each case one-by-one.
    - select the new case ID in the dropdown showing the current case ID.
- The current case is **auto-saved** before shifting to a new case.
- **Please notice that directly closing the browser won't save the current case.
To save the last case, please manually press the Save button.**
