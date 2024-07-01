import nibabel as nb
import numpy as np
import os
from typing import List
from scipy.ndimage import binary_closing

def mask_brain_images(output_dir: str, subject_id: str) -> List[str]:
    """Mask brain MRI images by Nipype.

    Parameters
    ----------
    output_dir : str
        Path of the output directory containing segmented NIfTI files.
    subject_id : str
        Subject identifier to process.

    Returns
    ----------
    output_file_path_list : list[str]
        Paths of the output files generated in the analysis.
    """

    # Define file paths based on provided output structure
    segment1_c1_path = os.path.join(output_dir, 'native_class_images', f'c1{subject_id}.nii')
    segment1_c2_path = os.path.join(output_dir, 'native_class_images', f'c2{subject_id}.nii')
    segment1_c3_path = os.path.join(output_dir, 'native_class_images', f'c3{subject_id}.nii')

    # Load image data from NIfTI files
    c1_nifti = nb.load(segment1_c1_path)
    c2_nifti = nb.load(segment1_c2_path)
    c3_nifti = nb.load(segment1_c3_path)
    c1_image_data = c1_nifti.get_fdata()
    c2_image_data = c2_nifti.get_fdata()
    c3_image_data = c3_nifti.get_fdata()

    # Create mask images
    x, y, z = c1_image_data.shape
    mask_image_data = np.zeros((x, y, z))
    for n in range(z):
        for k in range(y):
            for m in range(x):
                if c1_image_data[m, k, n] > 0 or c2_image_data[m, k, n] > 0 or c3_image_data[m, k, n] > 0:
                    mask_image_data[m, k, n] = 1

    # Apply binary closing to fill holes in the mask
    mask_image_data = binary_closing(mask_image_data).astype(np.uint8)

    # Save the mask image data
    mask_nifti = nb.Nifti1Image(mask_image_data, affine=c1_nifti.affine)
    mask_file_path = os.path.join(output_dir, 'mask.nii')
    nb.save(mask_nifti, mask_file_path)

    # Apply the mask to the brain MRI images
    alignment_path = os.path.join(output_dir, f'{subject_id}.nii')
    aligned_nifti = nb.load(alignment_path)
    aligned_image_data = aligned_nifti.get_fdata()
    masked_image_data = mask_image_data * aligned_image_data
    masked_nifti = nb.Nifti1Image(masked_image_data, affine=aligned_nifti.affine)
    masked_file_path = os.path.join(output_dir, f'masked_{subject_id}.nii')
    nb.save(masked_nifti, masked_file_path)

    # Return the paths of the output files saved in the analysis
    return [mask_file_path, masked_file_path]




# def mask_brain_images(output_dir: str, subject_id: str) -> List[str]:
#     """Mask brain MRI images by Nipype.

#     Parameters
#     ----------
#     output_dir : str
#         Path of the output directory containing segmented NIfTI files.
#     subject_id : str
#         Subject identifier to process.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """

#     # Define file paths based on provided output structure
#     segment1_c1_path = os.path.join(output_dir, 'native_class_images', f'c1{subject_id}.nii')
#     segment1_c2_path = os.path.join(output_dir, 'native_class_images', f'c2{subject_id}.nii')
#     segment1_c3_path = os.path.join(output_dir, 'native_class_images', f'c3{subject_id}.nii')

#     # Load image data from NIfTI files
#     c1_nifti = nb.load(segment1_c1_path)
#     c2_nifti = nb.load(segment1_c2_path)
#     c3_nifti = nb.load(segment1_c3_path)
#     c1_image_data = c1_nifti.get_fdata()
#     c2_image_data = c2_nifti.get_fdata()
#     c3_image_data = c3_nifti.get_fdata()

#     # Create mask images
#     x, y, z = c1_image_data.shape
#     mask_image_data = np.zeros((x, y, z))
#     for n in range(z):
#         for k in range(y):
#             for m in range(x):
#                 if c1_image_data[m, k, n] > 0 or c2_image_data[m, k, n] > 0 or c3_image_data[m, k, n] > 0:
#                     mask_image_data[m, k, n] = 1

#     # Save the mask image data
#     mask_nifti = nb.Nifti1Image(mask_image_data, affine=c1_nifti.affine)
#     mask_file_path = os.path.join(output_dir, 'mask.nii')
#     nb.save(mask_nifti, mask_file_path)

#     # Apply the mask to the brain MRI images
#     alignment_path = os.path.join(output_dir, f'{subject_id}.nii')
#     aligned_nifti = nb.load(alignment_path)
#     aligned_image_data = aligned_nifti.get_fdata()
#     masked_image_data = mask_image_data * aligned_image_data
#     masked_nifti = nb.Nifti1Image(masked_image_data, affine=aligned_nifti.affine)
#     masked_file_path = os.path.join(output_dir, f'masked_{subject_id}.nii')
#     nb.save(masked_nifti, masked_file_path)

#     # Return the paths of the output files saved in the analysis
#     return [mask_file_path, masked_file_path]