# %% [markdown]
# ### Measure intensities (with background subtraction)

# %%
# Import python packages.
from OpenIJTIFF import open_ij_tiff, save_ij_tiff
from skimage.io import imsave
import numpy as np
from napari.viewer import Viewer
import pandas as pd
from skimage.measure import regionprops_table

# %%
# load image from url
fpath = "https://github.com/NEUBIAS/training-resources/raw/master/image_data/xy_16bit__h2b.tif"
image, axes_image, voxel_image, units_image = open_ij_tiff(fpath)
fpath = "https://github.com/NEUBIAS/training-resources/raw/master/image_data/xy_8bit_labels__h2b.tif"
labels, axes_labels, voxel_labels, units_labels = open_ij_tiff(fpath)

# %%
# Create a napari_viewer and visualize image and labels
napari_viewer = Viewer()
napari_viewer.add_image(image, name='image')
napari_viewer.add_labels(labels, name='labels')

# %% [markdown]
# ## Compute the intensities 
# ### Background label  
# We can have an estimation of background intensity with the "0" label or create a specific background label.\
# **Napari GUI** Using the `layer controls` for the `labels` layer, manually create an additional label ("3" in this case) that measures the background.

# %%
objects_labels = np.unique(labels.flatten())
objects_labels.sort()
print(objects_labels)

# %% [markdown]
# Observe that there are 4 values: 0 being the background label, 
# 1, 2 are the cells and 3 is the manually labeled background.

# %%
# Use the intensity_image option of regionprops 
# to measure the fluorescence intensity of objects
fluo_regionprops = regionprops_table(
        labels,
        intensity_image = image,
        properties = ('label','area','intensity_mean','intensity_max')
)
print(fluo_regionprops)

# %%
# Wrap in a panda dataframe for better visualization nd export
fluo_measures = pd.DataFrame(fluo_regionprops)
print(fluo_measures)

# %%
# print the background intensity value
background_label = 3
background = fluo_measures[fluo_measures.label==background_label].intensity_mean.values[0]
print(background)

# %%
# Append the sum intensity and 
# background-corrected values to the table
fluo_measures['intensity_sum'] = fluo_measures.intensity_mean * fluo_measures.area
fluo_measures['intensity_mean_corr'] = fluo_measures.intensity_mean - background
fluo_measures['intensity_max_corr'] = fluo_measures.intensity_max - background
fluo_measures['intensity_sum_corr'] = fluo_measures.intensity_mean_corr * fluo_measures.area
print(fluo_measures)

# %% [markdown]
# ### Larger labels for intensitiy measures  

# %%
# Load the larger labels
fpath = "https://github.com/NEUBIAS/training-resources/raw/master/image_data/xy_8bit_labels__h2b_dilate_labels.tif"
dilated_labels, axes_labels, voxel_labels, units_labels = open_ij_tiff(fpath)
objects_labels = np.unique(dilated_labels.flatten())
print(objects_labels)

# %%
# Display the labels 
napari_viewer.add_labels(dilated_labels, name='dilated_labels')

# %%
# Measure the object intensites
fluo_measures_dilated = pd.DataFrame(
    regionprops_table(
        dilated_labels,
        intensity_image = image,
        properties = ('label','area','intensity_mean','intensity_max')
    )
)

# %%
# Append the background-corrected values to the table 
# with the dilated labels, using the same background
fluo_measures_dilated['intensity_sum'] = fluo_measures_dilated.intensity_mean * fluo_measures_dilated.area
fluo_measures_dilated['intensity_mean_corr'] = fluo_measures_dilated.intensity_mean - background
fluo_measures_dilated['intensity_max_corr'] = fluo_measures_dilated.intensity_max - background
fluo_measures_dilated['intensity_sum_corr'] = fluo_measures_dilated.intensity_mean_corr * fluo_measures_dilated.area
print(fluo_measures_dilated)

# %%
# Compare the results
# Observe:
# 1. mean intensity is affected by label size
# 2. max intensity is not affected by label size
# 3. bg-corrected sum intensity is hardly affected by label size
print("Small labels:")
print(fluo_measures)
print("\nLarge labels:")
print(fluo_measures_dilated)

# %%
# Export the data
fluo_measures.to_csv("object_measurements.csv")
fluo_measures_dilated.to_csv("object_measurements_dilated.csv")

