# Import modules
import napari
from skimage.io import imread

# Instantiate the napari viewer
viewer = napari.Viewer()

# Open a 3D image
image = imread('https://github.com/NEUBIAS/training-resources/raw/master/image_data/xyz_16bit__spots.tif')
viewer.add_image(image)

# Remember the axis order 0=z, 1=x, 2=y

# Maximum projection along z-axis
max_z_image = np.max(image, axis=0)
viewer.add_image(max_z_image)

# Sum projection along z-axis
sum_z_image = np.sum(image, axis=0)
viewer.add_image(sum_z_image)

# Appreciate that changing the data type during sum projections is useful
print(image.dtype)
print(image.shape)
print(2**16-1) # maximum value that the image's datatype can represent
print(image.shape[0]*(2**16-1)) # maximum value that could occur during sum projection
print(sum_z_image.dtype) # luckily numpy changed the data type during projection
print(2**64-1) # maximum value that the new data type can represent

# Maximum projection along x-axis and y-axis
max_x_image = np.max(image, axis=2)
max_y_image = np.max(image, axis=1)
viewer.add_image(max_x_image)
viewer.add_image(max_y_image)

# Due to the aniotropic pixel size the x and y projections appear squashed
# We can rescale the image to make it appear physcially correct
dx = 0.0941 # micrometer
dy = 0.0941 # micrometer
dz = 0.4 # micrometer

from skimage.transform import rescale
# The axes of the max_x_image are 0=z,1=y
# The z axes is squashed thus we enlarge it to make the image isotropic
rescaled_max_x_image = rescale(max_x_image, [dz/dx,1])  
viewer.add_image(rescaled_max_x_image)

# The max_y_image could be rescaled in the exact same way

# Import modules
import napari
from skimage.io import imread

# Instantiate the napari viewer
import napari
viewer = napari.Viewer()

# Read a binary 2D image
binary_2D_image = imread('https://github.com/NEUBIAS/training-resources/raw/master/image_data/xy_8bit_binary__nuclei.tif')
viewer.add_image(binary_2D_image)

# Connected components with connectivity 1 (aka 2D 4 connectivity) 
from skimage import measure
labels_2D_conn1_image = measure.label(binary_2D_image, connectivity=1)

viewer.add_labels(labels_2D_conn1_image)

# Connected components with connectivity 2 (aka 2D 8 connectivity) 
labels_2D_conn2_image = measure.label(binary_2D_image, connectivity=2)
viewer.add_labels(labels_2D_conn2_image)

# Read a binary 3D image
binary_3D_image = imread('https://github.com/NEUBIAS/training-resources/raw/master/image_data/xyz_8bit_binary__spots.tif')

# Connected components with connectivity 1 (aka 3D 6 connectivity) 
labels_3D_conn1_image = measure.label(binary_3D_image, connectivity=1)
viewer.add_labels(labels_3D_conn1_image)

# Interrogate the values in the 3D label image
print(np.unique(labels_3D_conn1_image)) # the object indices
print(len(np.unique(labels_3D_conn1_image))-1) # the number of objects (minus background)
print(np.max(labels_3D_conn1_image)) # the number of objects (minus background) (if the labels are consecutive!)
np.sum(labels_3D_conn1_image==2) # the number of pixels (~volume) in object number 2
