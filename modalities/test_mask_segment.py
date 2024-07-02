import os
import nibabel as nb
import numpy as np
from typing import List
from scipy.ndimage import binary_closing
from nipype import Node, Workflow
from nipype.interfaces.spm import NewSegment
from nipype.interfaces.io import DataSink

def join_filepath(paths: List[str]) -> str:
    return os.path.join(*paths)

def segment_brain_images(input_file: str, tpm_path: str, iteration: int, subject_id: str, subject_folder: str) -> str:
    """ Segment brain MRI images using Nipype-SPM12. """
    
    # Define file paths for TPM files
    tpm_files = [
        os.path.abspath(join_filepath([tpm_path, '01_GM.nii'])),
        os.path.abspath(join_filepath([tpm_path, '02_WM.nii'])),
        os.path.abspath(join_filepath([tpm_path, '03_CSF.nii'])),
        os.path.abspath(join_filepath([tpm_path, '04.nii'])),
        os.path.abspath(join_filepath([tpm_path, '05.nii'])),
        os.path.abspath(join_filepath([tpm_path, '06.nii']))
    ]

    output_subdir = os.path.join(subject_folder, 'segmentation', f'{iteration}_segment')
    os.makedirs(output_subdir, exist_ok=True)

    # Running segmentation
    segment_node = Node(NewSegment(), name=f'segment_{subject_id}_{iteration}')
    segment_node.inputs.channel_files = os.path.abspath(input_file)
    segment_node.inputs.channel_info = (0.00001, 60, (True, True)) # bias regularization, and a tuple indicating whether to save the bias-corrected images
    segment_node.inputs.tissues = [
        ((tpm_files[0], 1), 1, (True, True), (True, True)),
        ((tpm_files[1], 1), 1, (True, True), (True, True)),
        ((tpm_files[2], 1), 2, (True, True), (True, True)),
        ((tpm_files[3], 1), 3, (True, False), (False, False)),
        ((tpm_files[4], 1), 4, (True, False), (False, False)),
        ((tpm_files[5], 1), 2, (False, False), (False, False))
    ]

    # Set a DataSink node
    sink_node = Node(DataSink(), name=f'data_sink_{subject_id}_{iteration}')
    sink_node.inputs.base_directory = os.path.abspath(output_subdir)
    sink_node.inputs.substitutions = [('_subject_id', subject_id)]

    # Creating of workflow
    wf = Workflow(name=f'vbm_segment_{iteration}_{subject_id}')
    wf.base_dir = os.path.abspath(output_subdir)  # Ensure the workflow runs in the output directory
    wf.connect(segment_node, 'transformation_mat', sink_node, 'transformation_mat')
    wf.connect(segment_node, 'native_class_images', sink_node, 'native_class_images')
    wf.connect(segment_node, 'dartel_input_images', sink_node, 'dartel_input_images')
    wf.connect(segment_node, 'modulated_class_images', sink_node, 'modulated_class_images')
    wf.connect(segment_node, 'normalized_class_images', sink_node, 'normalized_class_images')
    wf.connect(segment_node, 'bias_corrected_images', sink_node, 'bias_corrected_images')

    # Running the workflow
    try:
        wf.run()
    except Exception as e: # checking if any errors exist
        print(f"Error running workflow for {input_file}: {e}")
        return ''

    return os.path.join(output_subdir, 'bias_corrected_images', f'm{subject_id}.nii')

def mask_brain_images(segmentation_dir: str, subject_folder: str, subject_id: str, iteration: int) -> str:
    """ Mask brain MRI images by Nipype. """
    
    segment1_c1_path = os.path.join(segmentation_dir, 'native_class_images', f'c1{subject_id}.nii')
    segment1_c2_path = os.path.join(segmentation_dir, 'native_class_images', f'c2{subject_id}.nii')
    segment1_c3_path = os.path.join(segmentation_dir, 'native_class_images', f'c3{subject_id}.nii')

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
    mask_output_dir = os.path.join(subject_folder, 'segmentation', f'{iteration}_mask')
    os.makedirs(mask_output_dir, exist_ok=True)
    mask_file_path = os.path.join(mask_output_dir, f'mask_{subject_id}.nii')
    mask_nifti = nb.Nifti1Image(mask_image_data, affine=c1_nifti.affine)
    nb.save(mask_nifti, mask_file_path)

    # Apply the mask to the brain MRI images
    alignment_path = os.path.join(segmentation_dir, 'bias_corrected_images', f'm{subject_id}.nii')
    aligned_nifti = nb.load(alignment_path)
    aligned_image_data = aligned_nifti.get_fdata()
    masked_image_data = mask_image_data * aligned_image_data
    masked_nifti = nb.Nifti1Image(masked_image_data, affine=aligned_nifti.affine)
    masked_file_path = os.path.join(mask_output_dir, f'masked_{subject_id}.nii')
    nb.save(masked_nifti, masked_file_path)

    return masked_file_path