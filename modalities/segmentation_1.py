from nipype import Node, Workflow, config
from nipype.interfaces.io import DataSink
from nipype.interfaces.spm import NewSegment
from typing import List
import os

def join_filepath(paths: List[str]) -> str:
    return os.path.join(*paths)

def segment_brain_images(input_folder: str, tpm_path: str) -> List[str]:
    """ Segment brain MRI images into some tissues such as the gray matter by Nipype-SPM12.

    Parameters  TODO: for now it is ok but maybe in the future I will need to modify it to get a templates from fixed foder or project
    ----------  
    input_folder : str
        Path of the directory containing the input NIfTI files. 
    tpm_path : str
        Path of the directory storing the tissue probability map (TPM) files.

    Returns
    ----------
    output_file_path_list : list[str]
        Paths of the output files generated in the analysis.
    """
    # # set Nipype configuration for MATLAB, suppressing stty errors
    # cfg = dict(execution={'matlab_cmd': '/usr/local/MATLAB/R2022a/bin/matlab -nodesktop -nosplash 2>/dev/null'})
    # config.update_config(cfg)

    # find all .nii files in the input folder and their subdir
    nifti_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.nii'):
                nifti_files.append(os.path.join(root, file))

    # checking if the nii file is there
    if not nifti_files:
        raise FileNotFoundError(f"No NIfTI files found in the input folder: {input_folder}")

    # define file paths for TPM files
    tpm_files = [
        os.path.abspath(join_filepath([tpm_path, '01_GM.nii'])),
        os.path.abspath(join_filepath([tpm_path, '02_WM.nii'])),
        os.path.abspath(join_filepath([tpm_path, '03_CSF.nii'])),
        os.path.abspath(join_filepath([tpm_path, '04.nii'])),
        os.path.abspath(join_filepath([tpm_path, '05.nii'])),
        os.path.abspath(join_filepath([tpm_path, '06.nii']))
    ]

    # checking if all TPM files exist
    for f in tpm_files:
        if not os.path.exists(f):
            raise FileNotFoundError(f"TPM file not found: {f}")

    # list to store all output file paths
    all_output_files = []

    # processing each NIfTI file
    for nifti_file in nifti_files:
        subject_id = os.path.basename(nifti_file).split('.')[0]
        output_dir = os.path.dirname(nifti_file)  # saving results in the same directory as the input file

        # checking the nii file exists
        if not os.path.exists(nifti_file):
            raise FileNotFoundError(f"NIfTI file not found: {nifti_file}")
        print(f"Processing file: {nifti_file}")

        # running segmentation
        segment_node = Node(NewSegment(), name=f'segment_{subject_id}')
        segment_node.inputs.channel_files = os.path.abspath(nifti_file)
        segment_node.inputs.channel_info = (0.00001, 60, (True, True)) # bias regularization, and a tuple indicating whether to save the bias-corrected images
        segment_node.inputs.tissues = [
            ((tpm_files[0], 1), 1, (True, True), (True, True)),
            ((tpm_files[1], 1), 1, (True, True), (True, True)),
            ((tpm_files[2], 1), 2, (True, True), (True, True)),
            ((tpm_files[3], 1), 3, (True, False), (False, False)),
            ((tpm_files[4], 1), 4, (True, False), (False, False)),
            ((tpm_files[5], 1), 2, (False, False), (False, False))
        ]

        # # Debugging: Print the paths used for the segment node
        # print(f"segment_node.inputs.channel_files: {segment_node.inputs.channel_files}")

        # Set a DataSink node
        sink_node = Node(DataSink(), name=f'data_sink_{subject_id}')
        sink_node.inputs.base_directory = os.path.abspath(output_dir)
        sink_node.inputs.substitutions = [('_subject_id', subject_id)]

        # # Debugging: Print the output directory
        # print(f"sink_node.inputs.base_directory: {sink_node.inputs.base_directory}")

        # creating of workflow
        wf = Workflow(name=f'vbm_segment1_{subject_id}')
        wf.base_dir = os.path.abspath(output_dir)  # Ensure the workflow runs in the output directory
        wf.connect(segment_node, 'transformation_mat', sink_node, 'transformation_mat')
        wf.connect(segment_node, 'native_class_images', sink_node, 'native_class_images')
        wf.connect(segment_node, 'dartel_input_images', sink_node, 'dartel_input_images')
        wf.connect(segment_node, 'modulated_class_images', sink_node, 'modulated_class_images')
        wf.connect(segment_node, 'normalized_class_images', sink_node, 'normalized_class_images')

        wf.connect(segment_node, 'bias_corrected_images', sink_node, 'bias_corrected_images')

        # runing the workflow
        try:
            wf.run()
        except Exception as e: # checking if any errors exist
            print(f"Error running workflow for {nifti_file}: {e}")
            continue

        # collect output files for this subject directly from the expected paths
        subject_output_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if subject_id in file:
                    subject_output_files.append(os.path.join(root, file))

        all_output_files.extend(subject_output_files)

    return all_output_files