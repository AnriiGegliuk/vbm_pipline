# # import os
# # from nipype import Node, Workflow
# # from nipype.interfaces.io import SelectFiles, DataSink
# # from nipype.interfaces.spm import CreateWarped
# # from typing import List

# # def join_filepath(parts: List[str]) -> str:
# #     """ Utility function to join file paths. """
# #     return os.path.join(*parts)

# # def find_subject_id(subject_folder: str) -> str:
# #     for file in os.listdir(subject_folder):
# #         if file.endswith('.nii'):
# #             return os.path.splitext(file)[0]
# #     return None

# # def normalize_brain_images(root_derivatives_dir_path: str) -> List[str]:
# #     """ Normalize brain MRI images by Nipype-SPM12.
# #     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.preprocess.html#createwarped
# #     for the details of the Nipype CreateWarped parameters.

# #     Parameters
# #         ----------
# #         root_derivatives_dir_path : str
# #             Path of the root derivatives directory.

# #     Returns
# #         ----------
# #         output_file_path_list : list[str]
# #             Paths of the output files generated in the analysis.
# #     """
# #     c1_files = []
# #     # c2_files = []
# #     flow_field_files = []

# #     # List of all subject folders excluding the Dartel directory
# #     subject_folders = [d for d in os.listdir(root_derivatives_dir_path) 
# #                        if os.path.isdir(os.path.join(root_derivatives_dir_path, d)) and d != 'Dartel']

# #     # Collecting c1 and c2 files
# #     for subject_folder in subject_folders:
# #         subject_folder_path = os.path.join(root_derivatives_dir_path, subject_folder)
# #         subject_id = find_subject_id(subject_folder_path)
# #         if not subject_id:
# #             print(f"Skipping {subject_folder} due to missing NIfTI file")
# #             continue

# #         c1_file = join_filepath([root_derivatives_dir_path, 'Dartel', 'c1', f'c1{subject_id}.nii'])
# #         # c2_file = join_filepath([root_derivatives_dir_path, 'Dartel', 'c2', f'c2{subject_id}.nii'])

# #         # if not os.path.exists(c1_file) or not os.path.exists(c2_file):
# #         #     print(f"Required NIfTI files not found for {subject_id}")
# #         #     continue

# #         c1_files.append(c1_file)
# #         # c2_files.append(c2_file)

# #     # Collecting flow field files
# #     flow_field_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'output', 'flowfields')
# #     for file in os.listdir(flow_field_dir):
# #         if file.startswith('u_') and file.endswith('_Template.nii'):
# #             flow_field_files.append(os.path.join(flow_field_dir, file))

# #     # Ensure all required files are found before proceeding
# #     # if not c1_files or not c2_files or not flow_field_files:
# #     #     print("Missing required files for normalization.")
# #     #     return []

# #     print(f"c1_files: {c1_files}")
# #     # print(f"c2_files: {c2_files}")
# #     print(f"flow_field_files: {flow_field_files}")

# #     # Create a normalization node.
# #     normalization_node = Node(CreateWarped(), name='normalization')
# #     normalization_node.inputs.image_files = c1_files
# #     normalization_node.inputs.flowfield_files = flow_field_files
# #     normalization_node.inputs.modulate = True

# #     # Set a DataSink node.
# #     sink_node = Node(DataSink(), name='data_sink')
# #     sink_node.inputs.base_directory = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')

# #     # Create a workflow.
# #     wf = Workflow(name='vbm_normalization')
# #     wf.base_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'work')
# #     wf.connect(normalization_node, 'warped_files', sink_node, 'warped_files')

# #     # Run the workflow.
# #     try:
# #         wf.run()
# #     except Exception as e:
# #         print(f"Workflow execution error: {e}")
# #         return []

# #     # Collect the paths of the output files saved in the analysis.
# #     output_files = []
# #     output_subdir_path = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')
# #     for root, dirs, files in os.walk(output_subdir_path):
# #         for file in files:
# #             output_files.append(os.path.join(root, file))

# #     return output_files


# import os
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm import CreateWarped
# from typing import List

# def join_filepath(parts: List[str]) -> str:
#     """ Utility function to join file paths. """
#     return os.path.join(*parts)

# def find_subject_id(subject_folder: str) -> str:
#     for file in os.listdir(subject_folder):
#         if file.endswith('.nii'):
#             return os.path.splitext(file)[0]
#     return None

# def normalize_brain_images(root_derivatives_dir_path: str) -> List[str]:
#     """ Normalize brain MRI images by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.preprocess.html#createwarped
#     for the details of the Nipype CreateWarped parameters.

#     Parameters
#     ----------
#     root_derivatives_dir_path : str
#         Path of the root derivatives directory.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """
#     c1_files = []
#     flow_field_files = []

#     # List of all subject folders excluding the Dartel directory
#     subject_folders = [d for d in os.listdir(root_derivatives_dir_path) 
#                        if os.path.isdir(os.path.join(root_derivatives_dir_path, d)) and d != 'Dartel']

#     # Collecting c1 files
#     for subject_folder in subject_folders:
#         subject_folder_path = os.path.join(root_derivatives_dir_path, subject_folder)
#         subject_id = find_subject_id(subject_folder_path)
#         if not subject_id:
#             print(f"Skipping {subject_folder} due to missing NIfTI file")
#             continue

#         c1_file = join_filepath([root_derivatives_dir_path, 'Dartel', 'c1', f'c1{subject_id}.nii'])

#         if not os.path.exists(c1_file):
#             print(f"File not found: {c1_file}")
#             continue

#         c1_files.append(c1_file)

#     # Collecting flow field files
#     flow_field_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'output', 'flowfields')
#     for file in os.listdir(flow_field_dir):
#         if file.startswith('u_') and file.endswith('_Template.nii'):
#             flow_field_file = os.path.join(flow_field_dir, file)
#             if not os.path.exists(flow_field_file):
#                 print(f"Flow field file not found: {flow_field_file}")
#                 continue
#             flow_field_files.append(flow_field_file)

#     if not c1_files or not flow_field_files:
#         print("Missing required files for normalization.")
#         return []

#     print(f"c1_files: {c1_files}")
#     print(f"flow_field_files: {flow_field_files}")

#     # Create a normalization node.
#     normalization_node = Node(CreateWarped(), name='normalization')
#     normalization_node.inputs.image_files = c1_files
#     normalization_node.inputs.flowfield_files = flow_field_files
#     normalization_node.inputs.modulate = True

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')

#     # Create a workflow.
#     wf = Workflow(name='vbm_normalization')
#     wf.base_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'work')
#     wf.connect(normalization_node, 'warped_files', sink_node, 'warped_files')

#     # Run the workflow.
#     try:
#         wf.run()
#     except Exception as e:
#         print(f"Workflow execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     output_subdir_path = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')
#     for root, dirs, files in os.walk(output_subdir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files

####### working as expected

import os
from nipype import Node, Workflow
from nipype.interfaces.io import DataSink
from nipype.interfaces.spm import CreateWarped
from typing import List, Tuple

def join_filepath(parts: List[str]) -> str:
    """ Utility function to join file paths. """
    return os.path.join(*parts)

def find_subject_id(subject_folder: str) -> str:
    for file in os.listdir(subject_folder):
        if file.endswith('.nii'):
            return os.path.splitext(file)[0]
    return None

def get_subject_id_from_filename(filename: str) -> str:
    return filename.split('T2_')[-1].split('.')[0] #:TODO this might be not ideal solution 

def normalize_brain_images(root_derivatives_dir_path: str) -> List[str]:
    """ Normalize brain MRI images by Nipype-SPM12.
    See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.preprocess.html#createwarped
    for the details of the Nipype CreateWarped parameters.

    Parameters
    ----------
    root_derivatives_dir_path : str
        Path of the root derivatives directory.

    Returns
    ----------
    output_file_path_list : list[str]
        Paths of the output files generated in the analysis.
    """
    c1_files = []
    flow_field_files = []

    # List of all subject folders excluding the Dartel directory
    subject_folders = [d for d in os.listdir(root_derivatives_dir_path) 
                       if os.path.isdir(os.path.join(root_derivatives_dir_path, d)) and d != 'Dartel']

    # Collecting c1 files
    for subject_folder in subject_folders:
        subject_folder_path = os.path.join(root_derivatives_dir_path, subject_folder)
        subject_id = find_subject_id(subject_folder_path)
        if not subject_id:
            print(f"Skipping {subject_folder} due to missing NIfTI file")
            continue

        c1_file = join_filepath([root_derivatives_dir_path, 'Dartel', 'c1', f'c1{subject_id}.nii'])

        if not os.path.exists(c1_file):
            print(f"File not found: {c1_file}")
            continue

        c1_files.append(c1_file)

    # Collecting flow field files
    flow_field_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'output', 'flowfields')
    for file in os.listdir(flow_field_dir):
        if file.startswith('u_') and file.endswith('_Template.nii'):
            flow_field_file = os.path.join(flow_field_dir, file)
            if not os.path.exists(flow_field_file):
                print(f"Flow field file not found: {flow_field_file}")
                continue
            flow_field_files.append(flow_field_file)

    if not c1_files or not flow_field_files:
        print("Missing required files for normalization.")
        return []

    # Sort files by subject ID
    c1_files.sort(key=get_subject_id_from_filename)
    flow_field_files.sort(key=get_subject_id_from_filename)

    print(f"c1_files: {c1_files}")
    print(f"flow_field_files: {flow_field_files}")

    # Create a normalization node.
    normalization_node = Node(CreateWarped(), name='normalization')
    normalization_node.inputs.image_files = c1_files
    normalization_node.inputs.flowfield_files = flow_field_files
    normalization_node.inputs.modulate = True

    # Set a DataSink node.
    sink_node = Node(DataSink(), name='data_sink')
    sink_node.inputs.base_directory = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')

    # Create a workflow.
    wf = Workflow(name='vbm_normalization')
    wf.base_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'work')
    wf.connect(normalization_node, 'warped_files', sink_node, 'warped_files')

    # Run the workflow.
    try:
        wf.run()
    except Exception as e:
        print(f"Workflow execution error: {e}")
        return []

    # Collect the paths of the output files saved in the analysis.
    output_files = []
    output_subdir_path = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')
    for root, dirs, files in os.walk(output_subdir_path):
        for file in files:
            output_files.append(os.path.join(root, file))

    return output_files
