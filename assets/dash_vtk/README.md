# Dash VTK #

## Introduction ##
- This is the customised Dash VTK used in this GUI for correctly plotting 3D data.
- Please follow the instructions at the main page to set this up before using the GUI.

## Problem ##
- Built-in color maps in Dash VTK cannot properly plot 3D segmentation labels with multiple pixel values.
- More specifically, it is very hard to differentiate colors corresponding to similar pixel values in these labels.

## Solution ##
- A customised color map has been manually added into [async-ReactVTK.js](./async-ReactVTK.js).
    ```
    {
        ColorSpace: "RGB",  # Color space of the color map
        Name: "ITK Snap",  # Name of the color map
        NanColor: [0,0,0],  # Color corresponding to NaN pixels in RGB color space
        RGBPoints: [  # Normalised lookup table describing the color map in RGB color space
            0,0,0,0,     # Label 0 -> Black
            .167,1,0,0,  # Label 1 -> Red
            .333,0,1,0,  # Label 2 -> Green
            .5,0,0,1,    # Label 3 -> Blue
            .667,1,1,0,  # Label 4 -> Yellow
            .833,0,1,1,  # Label 5 -> Cyan
            1,1,0,1      # Label 6 -> Magenta
        ]
    }
    ```