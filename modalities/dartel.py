# import os
# import shutil
# from nipype import Node, Workflow
# from nipype.interfaces.io import SelectFiles, DataSink
# from nipype.interfaces.spm import DARTEL

# def create_dartel_structure(base_path: str):
#     dartel_dir = os.path.join(base_path, 'Dartel')
#     os.makedirs(dartel_dir, exist_ok=True)
#     for folder in ['c1', 'c2', 'rc1', 'rc2', 'rc3']:
#         os.makedirs(os.path.join(dartel_dir, folder), exist_ok=True)
#     return dartel_dir

# def find_subject_id(subject_folder: str) -> str:
#     for file in os.listdir(subject_folder):
#         if file.endswith('.nii'):
#             return os.path.splitext(file)[0]
#     return None

# def copy_segment_files(segment_base_dir: str, dartel_dir: str):
#     for subject_folder in os.listdir(segment_base_dir):
#         subject_folder_path = os.path.join(segment_base_dir, subject_folder)
#         if not os.path.isdir(subject_folder_path):
#             continue

#         subject_id = find_subject_id(subject_folder_path)
#         if not subject_id:
#             print(f"No NIfTI file found in {subject_folder_path}")
#             continue

#         subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
#         if not os.path.isdir(subject_segmentation_dir):
#             print(f"No segmentation directory found for {subject_id}")
#             continue

#         for image_type in ['c1', 'c2']:
#             src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

#         for image_type in ['rc1', 'rc2', 'rc3']:
#             src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

# def perform_dartel(base_path: str):
#     dartel_dir = create_dartel_structure(base_path)
#     copy_segment_files(base_path, dartel_dir)

#     # List of all subject folders
#     subject_folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
#     for subject_folder in subject_folders:
#         subject_folder_path = os.path.join(base_path, subject_folder)
#         subject_id = find_subject_id(subject_folder_path)
#         if not subject_id:
#             print(f"Skipping {subject_folder} due to missing NIfTI file")
#             continue

#         # Set a SelectFiles node.
#         templates = {
#             'rc1': f'rc1/rc1{subject_id}.nii',
#             'rc2': f'rc2/rc2{subject_id}.nii',
#             'rc3': f'rc3/rc3{subject_id}.nii'
#         }
#         select_files_node = Node(SelectFiles(templates), name=f'select_files_{subject_id}')
#         select_files_node.inputs.base_directory = dartel_dir

#         try:
#             selected_files = select_files_node.run().outputs
#         except IOError as e:
#             print(f"File selection error for {subject_id}: {e}")
#             continue

#         # Perform DARTEL.
#         dartel_node = Node(DARTEL(), name=f'dartel_{subject_id}')
#         dartel_node.inputs.image_files = [
#             [selected_files.rc1],
#             [selected_files.rc2],
#             [selected_files.rc3]
#         ]

#         # Set a DataSink node.
#         sink_node = Node(DataSink(), name=f'data_sink_{subject_id}')
#         sink_node.inputs.base_directory = os.path.join(dartel_dir, 'rc1')

#         # Create a workflow.
#         wf = Workflow(name=f'vbm_dartel_{subject_id}')
#         wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#         wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#         wf.connect(dartel_node, 'template_files', sink_node, 'templates')

#         # Run the workflow.
#         wf.run()


########################## finaly worked but had error message with path
# import os
# import shutil
# from nipype import Node, Workflow
# from nipype.interfaces.io import SelectFiles, DataSink
# from nipype.interfaces.spm import DARTEL

# def create_dartel_structure(base_path: str):
#     dartel_dir = os.path.join(base_path, 'Dartel')
#     os.makedirs(dartel_dir, exist_ok=True)
#     for folder in ['c1', 'c2', 'rc1', 'rc2', 'rc3']:
#         os.makedirs(os.path.join(dartel_dir, folder), exist_ok=True)
#     return dartel_dir

# def find_subject_id(subject_folder: str) -> str:
#     for file in os.listdir(subject_folder):
#         if file.endswith('.nii'):
#             return os.path.splitext(file)[0]
#     return None

# def copy_segment_files(segment_base_dir: str, dartel_dir: str):
#     for subject_folder in os.listdir(segment_base_dir):
#         subject_folder_path = os.path.join(segment_base_dir, subject_folder)
#         if not os.path.isdir(subject_folder_path):
#             continue

#         subject_id = find_subject_id(subject_folder_path)
#         if not subject_id:
#             print(f"No NIfTI file found in {subject_folder_path}")
#             continue

#         subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
#         if not os.path.isdir(subject_segmentation_dir):
#             print(f"No segmentation directory found for {subject_id}")
#             continue

#         for image_type in ['c1', 'c2']:
#             src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

#         for image_type in ['rc1', 'rc2', 'rc3']:
#             src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

# def perform_dartel(dartel_dir: str):
#     # List of all subject IDs in Dartel directory
#     subject_ids = [f.replace('rc1', '').replace('.nii', '') for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]

#     for subject_id in subject_ids:
#         # Perform DARTEL
#         dartel_node = Node(DARTEL(), name=f'dartel_{subject_id}')
#         dartel_node.inputs.image_files = [
#             [os.path.join(dartel_dir, 'rc1', f'rc1{subject_id}.nii')],
#             [os.path.join(dartel_dir, 'rc2', f'rc2{subject_id}.nii')],
#             [os.path.join(dartel_dir, 'rc3', f'rc3{subject_id}.nii')]
#         ]

#         # Set a DataSink node
#         sink_node = Node(DataSink(), name=f'data_sink_{subject_id}')
#         sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output', subject_id)

#         # Create a workflow
#         wf = Workflow(name=f'vbm_dartel_{subject_id}')
#         wf.base_dir = dartel_dir  # Ensure the workflow runs in the Dartel directory
#         wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#         wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#         wf.connect(dartel_node, 'template_files', sink_node, 'templates')

#         # Run the workflow
#         wf.run()


# working but gives error with path
# import os
# import shutil
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm import DARTEL

# def create_dartel_structure(base_path: str):
#     dartel_dir = os.path.join(base_path, 'Dartel')
#     os.makedirs(dartel_dir, exist_ok=True)
#     for folder in ['c1', 'c2', 'rc1', 'rc2', 'rc3']:
#         os.makedirs(os.path.join(dartel_dir, folder), exist_ok=True)
#     return dartel_dir

# def find_subject_id(subject_folder: str) -> str:
#     for file in os.listdir(subject_folder):
#         if file.endswith('.nii'):
#             return os.path.splitext(file)[0]
#     return None

# def copy_segment_files(segment_base_dir: str, dartel_dir: str):
#     for subject_folder in os.listdir(segment_base_dir):
#         subject_folder_path = os.path.join(segment_base_dir, subject_folder)
#         if not os.path.isdir(subject_folder_path):
#             continue

#         subject_id = find_subject_id(subject_folder_path)
#         if not subject_id:
#             print(f"No NIfTI file found in {subject_folder_path}")
#             continue

#         subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
#         if not os.path.isdir(subject_segmentation_dir):
#             print(f"No segmentation directory found for {subject_id}")
#             continue

#         for image_type in ['c1', 'c2']:
#             src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

#         for image_type in ['rc1', 'rc2', 'rc3']:
#             src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

# def perform_dartel(dartel_dir: str):
#     # List of all subject IDs in Dartel directory
#     subject_ids = [f.replace('rc1', '').replace('.nii', '') for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]

#     for subject_id in subject_ids:
#         # Perform DARTEL
#         dartel_node = Node(DARTEL(), name=f'dartel_{subject_id}')
#         dartel_node.inputs.image_files = [
#             [os.path.join(dartel_dir, 'rc1', f'rc1{subject_id}.nii')],
#             [os.path.join(dartel_dir, 'rc2', f'rc2{subject_id}.nii')],
#             [os.path.join(dartel_dir, 'rc3', f'rc3{subject_id}.nii')]
#         ]

#         # Set a DataSink node
#         sink_node = Node(DataSink(), name=f'data_sink_{subject_id}')
#         sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output', subject_id)

#         # Create a workflow
#         wf = Workflow(name=f'vbm_dartel_{subject_id}')
#         wf.base_dir = os.path.join(dartel_dir, 'work')  # Ensure the workflow runs in the Dartel directory
#         wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#         wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#         wf.connect(dartel_node, 'template_files', sink_node, 'templates')

#         # Run the workflow
#         wf.run()











######## new code test does not work
# import os
# import shutil
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm import DARTEL

# def create_dartel_structure(base_path: str):
#     dartel_dir = os.path.join(base_path, 'Dartel')
#     os.makedirs(dartel_dir, exist_ok=True)
#     for folder in ['c1', 'c2', 'rc1', 'rc2', 'rc3']:
#         os.makedirs(os.path.join(dartel_dir, folder), exist_ok=True)
#     return dartel_dir

# def find_subject_id(subject_folder: str) -> str:
#     for file in os.listdir(subject_folder):
#         if file.endswith('.nii'):
#             return os.path.splitext(file)[0]
#     return None

# def copy_segment_files(segment_base_dir: str, dartel_dir: str):
#     for subject_folder in os.listdir(segment_base_dir):
#         subject_folder_path = os.path.join(segment_base_dir, subject_folder)
#         if not os.path.isdir(subject_folder_path):
#             continue

#         subject_id = find_subject_id(subject_folder_path)
#         if not subject_id:
#             print(f"No NIfTI file found in {subject_folder_path}")
#             continue

#         subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
#         if not os.path.isdir(subject_segmentation_dir):
#             print(f"No segmentation directory found for {subject_id}")
#             continue

#         for image_type in ['c1', 'c2']:
#             src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

#         for image_type in ['rc1', 'rc2', 'rc3']:
#             src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
#             if os.path.exists(src_file):
#                 dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                 shutil.copy(src_file, dst_file)
#                 print(f"Copied {src_file} to {dst_file}")
#             else:
#                 print(f"File {src_file} does not exist")

# def perform_dartel(dartel_dir: str):
#     # List of all subject IDs in Dartel directory
#     subject_ids = [f.replace('rc1', '').replace('.nii', '') for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]

#     for subject_id in subject_ids:
#         image_files = [
#             os.path.join(dartel_dir, 'rc1', f'rc1{subject_id}.nii'),
#             os.path.join(dartel_dir, 'rc2', f'rc2{subject_id}.nii'),
#             os.path.join(dartel_dir, 'rc3', f'rc3{subject_id}.nii')
#         ]

#         # Check if all files exist before proceeding
#         if not all(os.path.exists(file) for file in image_files):
#             print(f"One or more files for subject {subject_id} do not exist, skipping DARTEL")
#             continue

#         # Perform DARTEL
#         dartel_node = Node(DARTEL(), name=f'dartel_{subject_id}')
#         dartel_node.inputs.image_files = [[file] for file in image_files]

#         # Set a DataSink node
#         sink_node = Node(DataSink(), name=f'data_sink_{subject_id}')
#         sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output', subject_id)

#         # Create a workflow
#         wf = Workflow(name=f'vbm_dartel_{subject_id}')
#         wf.base_dir = os.path.join(dartel_dir, 'work')  # Ensure the workflow runs in the Dartel directory
#         wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#         wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#         wf.connect(dartel_node, 'template_files', sink_node, 'templates')

#         # Run the workflow
#         wf.run()




################# new code 

import os
import shutil
from nipype import Node, Workflow
from nipype.interfaces.io import DataSink
from nipype.interfaces.spm import DARTEL

def create_dartel_structure(base_path: str):
    dartel_dir = os.path.join(base_path, 'Dartel')
    os.makedirs(dartel_dir, exist_ok=True)
    for folder in ['c1', 'c2', 'rc1', 'rc2', 'rc3']:
        os.makedirs(os.path.join(dartel_dir, folder), exist_ok=True)
    return dartel_dir

def find_subject_id(subject_folder: str) -> str:
    for file in os.listdir(subject_folder):
        if file.endswith('.nii'):
            return os.path.splitext(file)[0]
    return None

def copy_segment_files(segment_base_dir: str, dartel_dir: str):
    for subject_folder in os.listdir(segment_base_dir):
        subject_folder_path = os.path.join(segment_base_dir, subject_folder)
        if not os.path.isdir(subject_folder_path):
            continue

        subject_id = find_subject_id(subject_folder_path)
        if not subject_id:
            print(f"No NIfTI file found in {subject_folder_path}")
            continue

        subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
        if not os.path.isdir(subject_segmentation_dir):
            print(f"No segmentation directory found for {subject_id}")
            continue

        for image_type in ['c1', 'c2']:
            src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
            if os.path.exists(src_file):
                dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
                shutil.copy(src_file, dst_file)
                print(f"Copied {src_file} to {dst_file}")
            else:
                print(f"File {src_file} does not exist")

        for image_type in ['rc1', 'rc2', 'rc3']:
            src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
            if os.path.exists(src_file):
                dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
                shutil.copy(src_file, dst_file)
                print(f"Copied {src_file} to {dst_file}")
            else:
                print(f"File {src_file} does not exist")

def perform_dartel(dartel_dir: str):
    # Gather all rc1, rc2, rc3 files for all subjects
    rc1_files = [os.path.abspath(os.path.join(dartel_dir, 'rc1', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]
    rc2_files = [os.path.abspath(os.path.join(dartel_dir, 'rc2', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc2')) if f.endswith('.nii')]
    rc3_files = [os.path.abspath(os.path.join(dartel_dir, 'rc3', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc3')) if f.endswith('.nii')]

    # Debug prints to check files
    print("Current working directory:", os.getcwd())
    print("rc1 files:", rc1_files)
    print("rc2 files:", rc2_files)
    print("rc3 files:", rc3_files)

    # Perform DARTEL
    dartel_node = Node(DARTEL(), name='dartel')
    dartel_node.inputs.image_files = [rc1_files, rc2_files, rc3_files]

    # Check if all files exist before proceeding
    for file_list in dartel_node.inputs.image_files:
        for file_path in file_list:
            abs_file_path = os.path.abspath(file_path)
            if not os.path.exists(abs_file_path):
                print(f"File {abs_file_path} does not exist, skipping DARTEL")
                return

    # Set a DataSink node
    sink_node = Node(DataSink(), name='data_sink')
    sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output')

    # Create a workflow
    wf = Workflow(name='vbm_dartel')
    wf.base_dir = os.path.join(dartel_dir, 'work')  # Ensure the workflow runs in the Dartel directory
    wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
    wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
    wf.connect(dartel_node, 'template_files', sink_node, 'templates')

    # Run the workflow
    wf.run()