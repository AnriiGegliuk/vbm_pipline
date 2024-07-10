# from modalities.segmentation_1 import segment_brain_images

# output_files = segment_brain_images('data/segmentation_pipline/', 'data/TPM/')
# print(output_files)


import os
from modalities.test_mask_segment import  segment_brain_images, mask_brain_images


def run_segmentation_and_masking(input_folder: str, tpm_path: str):
    # searching for .nii files within the subdirectories of input_folder
    subject_ids = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.nii'):
                subject_ids.append(os.path.join(root, file))
    
    print(subject_ids)  # check .nii files

    for input_file in subject_ids:
        subject_id = os.path.basename(input_file).split('.')[0]
        subject_folder = os.path.dirname(input_file)
        segmentation_folder = os.path.join(subject_folder, 'segmentation')
        os.makedirs(segmentation_folder, exist_ok=True)
        
        for iteration in range(1, 4):
            segmentation_output = segment_brain_images(input_file, tpm_path, iteration, subject_id, subject_folder)
            if not segmentation_output:
                print(f"Segmentation failed for {input_file} in iteration {iteration}")
                break
            mask_output = mask_brain_images(os.path.join(segmentation_folder, f'{iteration}_segment'), subject_folder, subject_id, iteration)
            input_file = os.path.join(segmentation_folder, f'{iteration}_mask', f'masked_{subject_id}.nii')
            
            # renaming the masked output to the original file name for the next iter
            next_input_file = os.path.join(segmentation_folder, f'{iteration}_mask', f'{subject_id}.nii') 
            os.rename(input_file, next_input_file)
            input_file = next_input_file


run_segmentation_and_masking('data/analysis_/', 'data/TPM')