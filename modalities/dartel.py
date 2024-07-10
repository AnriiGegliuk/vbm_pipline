################# new code working perfectly for single structure examle inside data/analysis_/conditions

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
#     # Gather all rc1, rc2, rc3 files for all subjects
#     rc1_files = [os.path.abspath(os.path.join(dartel_dir, 'rc1', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]
#     rc2_files = [os.path.abspath(os.path.join(dartel_dir, 'rc2', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc2')) if f.endswith('.nii')]
#     rc3_files = [os.path.abspath(os.path.join(dartel_dir, 'rc3', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc3')) if f.endswith('.nii')]

#     # Debug prints to check files
#     print("Current working directory:", os.getcwd())
#     print("rc1 files:", rc1_files)
#     print("rc2 files:", rc2_files)
#     print("rc3 files:", rc3_files)

#     # Perform DARTEL
#     dartel_node = Node(DARTEL(), name='dartel')
#     dartel_node.inputs.image_files = [rc1_files, rc2_files, rc3_files]

#     # Check if all files exist before proceeding
#     for file_list in dartel_node.inputs.image_files:
#         for file_path in file_list:
#             abs_file_path = os.path.abspath(file_path)
#             if not os.path.exists(abs_file_path):
#                 print(f"File {abs_file_path} does not exist, skipping DARTEL")
#                 return

#     # Set a DataSink node
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output')

#     # Create a workflow
#     wf = Workflow(name='vbm_dartel')
#     wf.base_dir = os.path.join(dartel_dir, 'work')  # Ensure the workflow runs in the Dartel directory
#     wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#     wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#     wf.connect(dartel_node, 'template_files', sink_node, 'templates')

#     # Run the workflow
#     wf.run()



########## new logic based on new data structure :test
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

# def copy_segment_files(base_path: str, condition_folders: list, dartel_dir: str):
#     for condition_folder in condition_folders:
#         segment_base_dir = os.path.join(base_path, condition_folder)
#         for subject_folder in os.listdir(segment_base_dir):
#             subject_folder_path = os.path.join(segment_base_dir, subject_folder)
#             if not os.path.isdir(subject_folder_path):
#                 continue

#             subject_id = find_subject_id(subject_folder_path)
#             if not subject_id:
#                 print(f"No NIfTI file found in {subject_folder_path}")
#                 continue

#             subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
#             if not os.path.isdir(subject_segmentation_dir):
#                 print(f"No segmentation directory found for {subject_id}")
#                 continue

#             for image_type in ['c1', 'c2']:
#                 src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
#                 if os.path.exists(src_file):
#                     dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                     shutil.copy(src_file, dst_file)
#                     print(f"Copied {src_file} to {dst_file}")
#                 else:
#                     print(f"File {src_file} does not exist")

#             for image_type in ['rc1', 'rc2', 'rc3']:
#                 src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
#                 if os.path.exists(src_file):
#                     dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                     shutil.copy(src_file, dst_file)
#                     print(f"Copied {src_file} to {dst_file}")
#                 else:
#                     print(f"File {src_file} does not exist")

# def perform_dartel(dartel_dir: str):
#     rc1_files = [os.path.abspath(os.path.join(dartel_dir, 'rc1', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]
#     rc2_files = [os.path.abspath(os.path.join(dartel_dir, 'rc2', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc2')) if f.endswith('.nii')]
#     rc3_files = [os.path.abspath(os.path.join(dartel_dir, 'rc3', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc3')) if f.endswith('.nii')]

#     print("Current working directory:", os.getcwd())
#     print("rc1 files:", rc1_files)
#     print("rc2 files:", rc2_files)
#     print("rc3 files:", rc3_files)

#     dartel_node = Node(DARTEL(), name='dartel')
#     dartel_node.inputs.image_files = [rc1_files, rc2_files, rc3_files]

#     for file_list in dartel_node.inputs.image_files:
#         for file_path in file_list:
#             abs_file_path = os.path.abspath(file_path)
#             if not os.path.exists(abs_file_path):
#                 print(f"File {abs_file_path} does not exist, skipping DARTEL")
#                 return

#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output')

#     wf = Workflow(name='vbm_dartel')
#     wf.base_dir = os.path.join(dartel_dir, 'work')
#     wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#     wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#     wf.connect(dartel_node, 'template_files', sink_node, 'templates')
    
#     wf.run()



# above did not worked testing new structure

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

# def copy_segment_files(base_path: str, condition_folders: list, dartel_dir: str):
#     for condition_folder in condition_folders:
#         segment_base_dir = os.path.join(base_path, condition_folder)
#         for subject_folder in os.listdir(segment_base_dir):
#             subject_folder_path = os.path.join(segment_base_dir, subject_folder)
#             if not os.path.isdir(subject_folder_path):
#                 continue

#             subject_id = find_subject_id(subject_folder_path)
#             if not subject_id:
#                 print(f"No NIfTI file found in {subject_folder_path}")
#                 continue

#             subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
#             if not os.path.isdir(subject_segmentation_dir):
#                 print(f"No segmentation directory found for {subject_id}")
#                 continue

#             for image_type in ['c1', 'c2']:
#                 src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
#                 if os.path.exists(src_file):
#                     dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                     shutil.copy(src_file, dst_file)
#                     print(f"Copied {src_file} to {dst_file}")
#                 else:
#                     print(f"File {src_file} does not exist")

#             for image_type in ['rc1', 'rc2', 'rc3']:
#                 src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
#                 if os.path.exists(src_file):
#                     dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                     shutil.copy(src_file, dst_file)
#                     print(f"Copied {src_file} to {dst_file}")
#                 else:
#                     print(f"File {src_file} does not exist")

# def perform_dartel(dartel_dir: str):
#     rc1_files = [os.path.abspath(os.path.join(dartel_dir, 'rc1', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]
#     rc2_files = [os.path.abspath(os.path.join(dartel_dir, 'rc2', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc2')) if f.endswith('.nii')]
#     rc3_files = [os.path.abspath(os.path.join(dartel_dir, 'rc3', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc3')) if f.endswith('.nii')]

#     print("Current working directory:", os.getcwd())
#     print("rc1 files:", rc1_files)
#     print("rc2 files:", rc2_files)
#     print("rc3 files:", rc3_files)

#     dartel_node = Node(DARTEL(), name='dartel')
#     dartel_node.inputs.image_files = [rc1_files, rc2_files, rc3_files]

#     for file_list in dartel_node.inputs.image_files:
#         for file_path in file_list:
#             abs_file_path = os.path.abspath(file_path)
#             if not os.path.exists(abs_file_path):
#                 print(f"File {abs_file_path} does not exist, skipping DARTEL")
#                 return

#     # Set a DataSink node to store the outputs
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output')
#     sink_node.inputs.substitutions = [('_report', '_report')]

#     # Create a workflow
#     wf = Workflow(name='vbm_dartel')
#     wf.base_dir = os.path.join(dartel_dir, 'work')  # Ensure the workflow runs in the Dartel directory
#     wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#     wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#     wf.connect(dartel_node, 'template_files', sink_node, 'templates')

#     # Run the workflow
#     wf.run()


#### above does not work trying new code 

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
#     os.makedirs(os.path.join(dartel_dir, 'output', 'final_template'), exist_ok=True)
#     os.makedirs(os.path.join(dartel_dir, 'output', 'flowfields'), exist_ok=True)
#     os.makedirs(os.path.join(dartel_dir, 'output', 'templates'), exist_ok=True)
#     return dartel_dir

# def find_subject_id(subject_folder: str) -> str:
#     for file in os.listdir(subject_folder):
#         if file.endswith('.nii'):
#             return os.path.splitext(file)[0]
#     return None

# def copy_segment_files(base_path: str, condition_folders: list, dartel_dir: str):
#     for condition_folder in condition_folders:
#         segment_base_dir = os.path.join(base_path, condition_folder)
#         for subject_folder in os.listdir(segment_base_dir):
#             subject_folder_path = os.path.join(segment_base_dir, subject_folder)
#             if not os.path.isdir(subject_folder_path):
#                 continue

#             subject_id = find_subject_id(subject_folder_path)
#             if not subject_id:
#                 print(f"No NIfTI file found in {subject_folder_path}")
#                 continue

#             subject_segmentation_dir = os.path.join(subject_folder_path, 'segmentation', '3_segment')
#             if not os.path.isdir(subject_segmentation_dir):
#                 print(f"No segmentation directory found for {subject_id}")
#                 continue

#             for image_type in ['c1', 'c2']:
#                 src_file = os.path.join(subject_segmentation_dir, 'native_class_images', f'{image_type}{subject_id}.nii')
#                 if os.path.exists(src_file):
#                     dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                     shutil.copy(src_file, dst_file)
#                     print(f"Copied {src_file} to {dst_file}")
#                 else:
#                     print(f"File {src_file} does not exist")

#             for image_type in ['rc1', 'rc2', 'rc3']:
#                 src_file = os.path.join(subject_segmentation_dir, 'dartel_input_images', f'{image_type}{subject_id}.nii')
#                 if os.path.exists(src_file):
#                     dst_file = os.path.join(dartel_dir, image_type, f'{image_type}{subject_id}.nii')
#                     shutil.copy(src_file, dst_file)
#                     print(f"Copied {src_file} to {dst_file}")
#                 else:
#                     print(f"File {src_file} does not exist")

# def perform_dartel(dartel_dir: str):
#     rc1_files = [os.path.abspath(os.path.join(dartel_dir, 'rc1', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]
#     rc2_files = [os.path.abspath(os.path.join(dartel_dir, 'rc2', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc2')) if f.endswith('.nii')]
#     rc3_files = [os.path.abspath(os.path.join(dartel_dir, 'rc3', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc3')) if f.endswith('.nii')]

#     print("Current working directory:", os.getcwd())
#     print("rc1 files:", rc1_files)
#     print("rc2 files:", rc2_files)
#     print("rc3 files:", rc3_files)

#     dartel_node = Node(DARTEL(), name='dartel')
#     dartel_node.inputs.image_files = [rc1_files, rc2_files, rc3_files]

#     for file_list in dartel_node.inputs.image_files:
#         for file_path in file_list:
#             abs_file_path = os.path.abspath(file_path)
#             if not os.path.exists(abs_file_path):
#                 print(f"File {abs_file_path} does not exist, skipping DARTEL")
#                 return

#     # Set a DataSink node to store the outputs
#     # sink_node = Node(DataSink(), name='data_sink')
#     # sink_node.inputs.base_directory = os.path.join(dartel_dir, 'output')
#     output_base_dir = os.path.join(dartel_dir, 'output')
#     print("DataSink base directory:", output_base_dir)  # Print the path to verify it

#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = output_base_dir
    

#     # Create a workflow
#     wf = Workflow(name='vbm_dartel')
#     wf.base_dir = os.path.join(dartel_dir, 'work')  # Ensure the workflow runs in the Dartel directory
#     wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
#     wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
#     wf.connect(dartel_node, 'template_files', sink_node, 'templates')

#     # Run the workflow
#     wf.run()


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
    os.makedirs(os.path.join(dartel_dir, 'output', 'final_template'), exist_ok=True)
    os.makedirs(os.path.join(dartel_dir, 'output', 'flowfields'), exist_ok=True)
    os.makedirs(os.path.join(dartel_dir, 'output', 'templates'), exist_ok=True)
    return dartel_dir

def find_subject_id(subject_folder: str) -> str:
    for file in os.listdir(subject_folder):
        if file.endswith('.nii'):
            return os.path.splitext(file)[0]
    return None

def copy_segment_files(base_path: str, condition_folders: list, dartel_dir: str):
    for condition_folder in condition_folders:
        segment_base_dir = os.path.join(base_path, condition_folder)
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
    rc1_files = [os.path.abspath(os.path.join(dartel_dir, 'rc1', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc1')) if f.endswith('.nii')]
    rc2_files = [os.path.abspath(os.path.join(dartel_dir, 'rc2', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc2')) if f.endswith('.nii')]
    rc3_files = [os.path.abspath(os.path.join(dartel_dir, 'rc3', f)) for f in os.listdir(os.path.join(dartel_dir, 'rc3')) if f.endswith('.nii')]

    print("Current working directory:", os.getcwd())
    print("rc1 files:", rc1_files)
    print("rc2 files:", rc2_files)
    print("rc3 files:", rc3_files)

    dartel_node = Node(DARTEL(), name='dartel')
    dartel_node.inputs.image_files = [rc1_files, rc2_files, rc3_files]

    for file_list in dartel_node.inputs.image_files:
        for file_path in file_list:
            abs_file_path = os.path.abspath(file_path)
            if not os.path.exists(abs_file_path):
                print(f"File {abs_file_path} does not exist, skipping DARTEL")
                return

    # Set a DataSink node to store the outputs
    output_base_dir = os.path.join(dartel_dir, 'output')
    print("DataSink base directory:", output_base_dir)  # Print the path to verify it

    sink_node = Node(DataSink(), name='data_sink')
    sink_node.inputs.base_directory = output_base_dir
    sink_node.inputs.substitutions = [('_report', '_report')]

    # Create a workflow
    wf = Workflow(name='vbm_dartel')
    wf.base_dir = os.path.join(dartel_dir, 'work')  # Ensure the workflow runs in the Dartel directory
    wf.connect(dartel_node, 'dartel_flow_fields', sink_node, 'flowfields')
    wf.connect(dartel_node, 'final_template_file', sink_node, 'final_template')
    wf.connect(dartel_node, 'template_files', sink_node, 'templates')

    # Run the workflow
    wf.run()
