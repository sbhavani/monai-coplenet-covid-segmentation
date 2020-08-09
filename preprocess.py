import os
from lungmask import mask
import SimpleITK as sitk
import dicom2nifti
import nibabel as nb
import numpy as np
from skimage.transform import resize

data_path = os.getenv('PATIENT_FOLDER')
nifti_path = os.getenv('IMAGE_FOLDER')

# takes nifti image as input and returns a nifti image
def segment_lung_ct(img):
    return mask.apply(img)  # default model is U-net(R231)

# convert patient scans to nifti
def convert_scans_to_nifti():
    for d in os.listdir(data_path):
        # this will create one Nifti file per series in folder
        output_dir = os.path.join(nifti_path, d)
        os.mkdir(output_dir)
        dicom2nifti.convert_directory(
            os.path.join(data_path, d), 
            output_folder=output_dir,
            compression=True, # .nii.gz vs .nii
            reorient=True, # left anterior superior coordinates
        )


# save segmented lung scans
for scan in os.listdir(nifti_path):
    input_fname = os.path.join(nifti_path, scan)
    if scan.startswith('segmented'):
        continue
    # load nifti object
    nii = nb.load(input_fname)
    # get nd array data
    img = nii.get_data()
    print(img.shape)
    x,y,z = (int(img.shape[0]/2), int(img.shape[1]/2), img.shape[2])
    #img = resize(img, (x,y,z))
    print(img.shape)
    scan_array = np.transpose(img, (2,1,0))
    sitk_img = sitk.GetImageFromArray(scan_array)
    segmentation = mask.apply(sitk_img) #segment_lung_ct(sitk_img)
    result = np.bitwise_and(scan_array, segmentation)
    # convert from integers to floats
    pixels = result.astype('float32')
    # normalize to the range 0-1
    pixels /= 2.0
    # confirm the normalization
    print('Min: %.3f, Max: %.3f' % (pixels.min(), pixels.max()))
    res_image = sitk.GetImageFromArray(pixels)
    sitk.WriteImage(res_image,os.path.join(nifti_path, 'segmented_' + scan))
