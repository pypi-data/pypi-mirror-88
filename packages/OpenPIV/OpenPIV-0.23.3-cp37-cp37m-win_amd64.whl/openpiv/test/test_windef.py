# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 14:33:21 2019

@author: Theo
"""


import numpy as np
import openpiv.windef as windef
from test_process import create_pair, shift_u, shift_v, threshold
import pathlib

frame_a, frame_b = create_pair(image_size=256)

# this test are created only to test the displacement evaluation of the
# function the validation methods are not tested here ant therefore
# are disabled.


# circular cross correlation
def test_first_pass_circ():
    """ test of the first pass """
    x, y, u, v, s2n = windef.first_pass(
        frame_a,
        frame_b,
        window_size=64,
        overlap=32,
        iterations=1,
        correlation_method="circular",
        subpixel_method="gaussian",
        do_sig2noise=True,
        sig2noise_method="peak2peak",
        sig2noise_mask=2,
    )
    print("\n", x, y, u, v, s2n)
    assert np.mean(np.abs(u - shift_u)) < threshold
    assert np.mean(np.abs(v - shift_v)) < threshold


def test_multi_pass_circ():
    """ test fot the multipass """
    window_size = (128, 64, 32)
    overlap = (64, 32, 16)
    iterations = 3

    x, y, u, v, s2n = windef.first_pass(
        frame_a,
        frame_b,
        window_size[0],
        overlap[0],
        iterations,
        correlation_method="circular",
        subpixel_method="gaussian",
        do_sig2noise=True,
        sig2noise_method="peak2peak",
        sig2noise_mask=2,
    )
    u_old = u.copy()
    v_old = v.copy()
    print("\n", x, y, u_old, v_old, s2n)
    assert np.mean(np.abs(u_old - shift_u)) < threshold
    assert np.mean(np.abs(v_old - shift_v)) < threshold
    for i in range(1, iterations):
        x, y, u, v, s2n = windef.multipass_img_deform(
            frame_a,
            frame_b,
            window_size[i],
            overlap[i],
            iterations,
            i,
            x,
            y,
            u,
            v,
            correlation_method="circular",
            subpixel_method="gaussian",
            deformation_method="symmetric",
            do_sig2noise=False,
            sig2noise_method="peak2peak",
            sig2noise_mask=2,
            interpolation_order=3,
        )

    print("\n", x, y, u, v, s2n)
    assert np.mean(np.abs(u - shift_u)) < threshold
    assert np.mean(np.abs(v - shift_v)) < threshold
    # the second condition is to check if the multipass is done.
    # It need's a little numerical inaccuracy.


# linear cross correlation
def test_first_pass_lin():
    """ test of the first pass """
    x, y, u, v, s2n = windef.first_pass(
        frame_a,
        frame_b,
        window_size=64,
        overlap=32,
        iterations=1,
        correlation_method="linear",
        subpixel_method="gaussian",
        do_sig2noise=True,
        sig2noise_method="peak2peak",
        sig2noise_mask=2,
    )
    print("\n", x, y, u, v, s2n)
    assert np.mean(np.abs(u - shift_u)) < threshold
    assert np.mean(np.abs(v - shift_v)) < threshold


def test_invert():
    """ Test windef.piv with invert option """

    file_a = pathlib.Path(__file__).parent / '../examples/test1/exp1_001_a.bmp'
    file_b = pathlib.Path(__file__).parent / '../examples/test1/exp1_001_b.bmp'

    settings = windef.Settings()
    'Data related settings'
    # Folder with the images to process
    settings.filepath_images = pathlib.Path(__file__).parent / '../examples/test1'
    settings.save_path = '.'
    # Root name of the output Folder for Result Files
    settings.save_folder_suffix = 'test'
    # Format and Image Sequence
    settings.frame_pattern_a = 'exp1_001_a.bmp'
    settings.frame_pattern_b = 'exp1_001_a.bmp'

    'Region of interest'
    # (50,300,50,300) #Region of interest: (xmin,xmax,ymin,ymax) or 'full' for full image
    settings.ROI = 'full'
    # settings.ROI = (0,1024,200,500)

    'Image preprocessing'

    settings.invert = True
    # 'None' for no masking, 'edges' for edges masking, 'intensity' for intensity masking
    # WARNING: This part is under development so better not to use MASKS
    settings.dynamic_masking_method = 'None'
    settings.dynamic_masking_threshold = 0.005
    settings.dynamic_masking_filter_size = 7

    'Processing Parameters'
    settings.correlation_method = 'circular'  # 'circular' or 'linear'
    settings.normalized_correlation = 'True'

    settings.deformation_method = 'symmetric'
    settings.iterations = 3  # select the number of PIV passes
    # add the interroagtion window size for each pass. 
    # For the moment, it should be a power of 2 
    settings.windowsizes = (64, 32, 16)  # if longer than n iteration the rest is ignored
    # The overlap of the interroagtion window for each pass.
    settings.overlap = (32, 16, 8)  # This is 50% overlap
    # Has to be a value with base two. In general window size/2 is a good choice.
    # methode used for subpixel interpolation: 'gaussian','centroid','parabolic'
    settings.subpixel_method = 'gaussian'
    # order of the image interpolation for the window deformation
    settings.interpolation_order = 3
    settings.scaling_factor = 1  # scaling factor pixel/meter
    settings.dt = 1  # time between to frames (in seconds)
    'Signal to noise ratio options (only for the last pass)'
    # It is possible to decide if the S/N should be computed (for the last pass) or not
    settings.extract_sig2noise = True  # 'True' or 'False' (only for the last pass)
    # method used to calculate the signal to noise ratio 'peak2peak' or 'peak2mean'
    settings.sig2noise_method = 'peak2peak'
    # select the width of the masked to masked out pixels next to the main peak
    settings.sig2noise_mask = 2
    # If extract_sig2noise==False the values in the signal to noise ratio
    # output column are set to NaN
    'vector validation options'
    # choose if you want to do validation of the first pass: True or False
    settings.validation_first_pass = True
    # only effecting the first pass of the interrogation the following passes
    # in the multipass will be validated
    'Validation Parameters'
    # The validation is done at each iteration based on three filters.
    # The first filter is based on the min/max ranges. Observe that these values are defined in
    # terms of minimum and maximum displacement in pixel/frames.
    settings.MinMax_U_disp = (-30, 30)
    settings.MinMax_V_disp = (-30, 30)
    # The second filter is based on the global STD threshold
    settings.std_threshold = 4  # threshold of the std validation
    # The third filter is the median test (not normalized at the moment)
    settings.median_threshold = 3  # threshold of the median validation
    # On the last iteration, an additional validation can be done based on the S/N.
    settings.median_size = 1 #defines the size of the local median
    'Validation based on the signal to noise ratio'
    # Note: only available when extract_sig2noise==True and only for the last
    # pass of the interrogation
    # Enable the signal to noise ratio validation. Options: True or False
    settings.do_sig2noise_validation = False # This is time consuming
    # minmum signal to noise ratio that is need for a valid vector
    settings.sig2noise_threshold = 1.2
    'Outlier replacement or Smoothing options'
    # Replacment options for vectors which are masked as invalid by the validation
    settings.replace_vectors = True  # Enable the replacment. Chosse: True or False
    settings.smoothn = True  # Enables smoothing of the displacemenet field
    settings.smoothn_p = 0.5  # This is a smoothing parameter
    # select a method to replace the outliers: 'localmean', 'disk', 'distance'
    settings.filter_method = 'localmean'
    # maximum iterations performed to replace the outliers
    settings.max_filter_iteration = 10
    settings.filter_kernel_size = 2  # kernel size for the localmean method
    'Output options'
    # Select if you want to save the plotted vectorfield: True or False
    settings.save_plot = False
    # Choose wether you want to see the vectorfield or not :True or False
    settings.show_plot = False
    settings.scale_plot = 10  # select a value to scale the quiver plot of the vectorfield
    # run the script with the given settings
    windef.piv(settings)



def test_multi_pass_lin():
    """ test fot the multipass """
    window_size = (128, 64, 32)
    overlap = (64, 32, 16)
    iterations = 3

    x, y, u, v, s2n = windef.first_pass(
        frame_a,
        frame_b,
        window_size[0],
        overlap[0],
        iterations,
        correlation_method="linear",
        subpixel_method="gaussian",
        do_sig2noise=True,
        sig2noise_method="peak2peak",
        sig2noise_mask=2,
    )
    u_old = u.copy()
    v_old = v.copy()

    print("\n", x, y, u_old, v_old, s2n)
    assert np.mean(np.abs(u_old - shift_u)) < threshold
    assert np.mean(np.abs(v_old - shift_v)) < threshold

    for i in range(1, iterations):
        x, y, u, v, _ = windef.multipass_img_deform(
            frame_a,
            frame_b,
            window_size[i],
            overlap[i],
            iterations,
            i,
            x,
            y,
            u,
            v,
            correlation_method="linear",
            subpixel_method="gaussian",
            deformation_method="symmetric",
            do_sig2noise=False,
            sig2noise_method="peak2peak",
            sig2noise_mask=2,
            interpolation_order=3,
        )

    print("\n", x, y, u, v, s2n)
    assert np.mean(np.abs(u - shift_u)) < threshold
    assert np.mean(np.abs(v - shift_v)) < threshold

    # the second condition is to check if the multipass is done.
    # It need's a little numerical inaccuracy.
