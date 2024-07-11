import os
import nibabel as nb
import numpy as np
import pandas as pd
from typing import List

def join_filepath(parts: List[str]) -> str:
    """ Utility function to join file paths. """
    return os.path.join(*parts)

def find_subject_id(subject_folder: str) -> str:
    for file in os.listdir(subject_folder):
        if file.endswith('.nii'):
            return os.path.splitext(file)[0]
    return None

def calc_total_brain_volume(subject_folder: str) -> dict:
    """ Calculate the total brain volume. """
    
    subject_id = find_subject_id(subject_folder)
    if not subject_id:
        print(f"No NIfTI file found in {subject_folder}")
        return {}

    segment2_dir_path = os.path.join(subject_folder, 'segmentation', '3_segment', 'native_class_images')
    if not os.path.exists(segment2_dir_path):
        print(f"No native_class_images directory found for {subject_id}")
        return {}

    c1_file = os.path.join(segment2_dir_path, f'c1{subject_id}.nii')
    c2_file = os.path.join(segment2_dir_path, f'c2{subject_id}.nii')
    if not os.path.exists(c1_file) or not os.path.exists(c2_file):
        print(f"Required NIfTI files not found for {subject_id}")
        return {}

    # Load image data from NIfTI files.
    c1_nifti = nb.load(c1_file)
    c2_nifti = nb.load(c2_file)
    c1_image_data = c1_nifti.get_fdata()
    c2_image_data = c2_nifti.get_fdata()

    # Calculate the brain volumes.
    c1_volume_size = abs(np.linalg.det(c1_nifti.affine))
    c2_volume_size = abs(np.linalg.det(c2_nifti.affine))
    c1_brain_volume = np.sum(c1_image_data) * c1_volume_size / 1000
    c2_brain_volume = np.sum(c2_image_data) * c2_volume_size / 1000
    total_brain_volume = c1_brain_volume + c2_brain_volume

    return {
        "subject_id": subject_id,
        "grey_matter_volume": c1_brain_volume,
        "white_matter_volume": c2_brain_volume,
        "total_brain_volume": total_brain_volume
    }

def create_final_csv(base_path: str, output_file: str):
    brain_volume_data = []
    subject_folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    for subject_folder in subject_folders:
        if 'Dartel' in subject_folder: # ignoring Dartel folder
            continue
        subject_folder_path = os.path.join(base_path, subject_folder)
        brain_volume_info = calc_total_brain_volume(subject_folder_path)
        if brain_volume_info:
            brain_volume_data.append(brain_volume_info)

    
    os.makedirs(os.path.dirname(output_file), exist_ok=True) # create the directory if it does not exist

    # creating a DataFrame and save to CSV
    df = pd.DataFrame(brain_volume_data)
    df.to_csv(output_file, index=False)