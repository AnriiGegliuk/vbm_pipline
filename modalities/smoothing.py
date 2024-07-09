# import os
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm import Smooth
# from typing import List

# def join_filepath(parts: List[str]) -> str:
#     """ Utility function to join file paths. """
#     return os.path.join(*parts)

# def get_subject_id_from_filename(filename: str) -> str:
#     return filename.split('T2_')[-1].split('.')[0]

# def smooth_brain_images(root_derivatives_dir_path: str, fwhm: List[int]) -> List[str]:
#     """ Smooth brain MRI images by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.preprocess.html#smooth
#     for the details of the Nipype Smooth parameters.

#     Parameters
#     ----------
#     root_derivatives_dir_path : str
#         Path of the root derivatives directory.
#     fwhm : list[int]
#         Full width at half maximum (FWHM) applied to smoothing.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """

#     normalize_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')
#     smooth_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'output', 'smoothed_files')

#     # Create the smoothing directory if it doesn't exist
#     os.makedirs(smooth_dir, exist_ok=True)

#     normalize_files = []
#     subject_ids = []

#     # Collecting normalized files
#     for root, _, files in os.walk(normalize_dir):
#         for file in files:
#             if file.startswith('mwc1') and file.endswith('.nii'):
#                 normalize_files.append(os.path.join(root, file))
#                 subject_ids.append(get_subject_id_from_filename(file))

#     # Sort files by subject ID
#     normalize_files.sort(key=get_subject_id_from_filename)

#     print(f"normalize_files: {normalize_files}")

#     # Create a smoothing node.
#     smoothing_node = Node(Smooth(), name='smoothing')
#     smoothing_node.inputs.fwhm = fwhm
#     smoothing_node.inputs.in_files = normalize_files

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = smooth_dir

#     # Create a workflow.
#     wf = Workflow(name='vbm_smoothing')
#     wf.base_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'work')
#     wf.connect(smoothing_node, 'smoothed_files', sink_node, 'smoothed_files')

#     # Run the workflow.
#     try:
#         wf.run()
#     except Exception as e:
#         print(f"Workflow execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, dirs, files in os.walk(smooth_dir):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files



import os
from nipype import Node, Workflow
from nipype.interfaces.io import DataSink
from nipype.interfaces.spm import Smooth
from typing import List

def join_filepath(parts: List[str]) -> str:
    """ Utility function to join file paths. """
    return os.path.join(*parts)

def get_subject_id_from_filename(filename: str) -> str:
    return filename.split('T2_')[-1].split('.')[0]

def smooth_brain_images(root_derivatives_dir_path: str, fwhm: List[int]) -> List[str]:
    """ Smooth brain MRI images by Nipype-SPM12.
    See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.preprocess.html#smooth
    for the details of the Nipype Smooth parameters.

    Parameters
    ----------
    root_derivatives_dir_path : str
        Path of the root derivatives directory.
    fwhm : list[int]
        Full width at half maximum (FWHM) applied to smoothing.

    Returns
    ----------
    output_file_path_list : list[str]
        Paths of the output files generated in the analysis.
    """

    normalize_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'output')
    smooth_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'output', 'smoothed_files')

    # Create the smoothing directory if it doesn't exist
    os.makedirs(smooth_dir, exist_ok=True)

    normalize_files = []
    subject_ids = []

    # Collecting normalized files
    for root, _, files in os.walk(normalize_dir):
        for file in files:
            if file.startswith('mwc1') and file.endswith('.nii'):
                normalize_files.append(os.path.join(root, file))
                subject_ids.append(get_subject_id_from_filename(file))

    # Sort files by subject ID
    normalize_files.sort(key=get_subject_id_from_filename)

    print(f"normalize_files: {normalize_files}")

    # Create a smoothing node.
    smoothing_node = Node(Smooth(), name='smoothing')
    smoothing_node.inputs.fwhm = fwhm
    smoothing_node.inputs.in_files = normalize_files

    # Set a DataSink node.
    sink_node = Node(DataSink(), name='data_sink')
    sink_node.inputs.base_directory = root_derivatives_dir_path  # Use the root directory
    sink_node.inputs.container = 'Dartel/output/smoothed_files'

    # Create a workflow.
    wf = Workflow(name='vbm_smoothing')
    wf.base_dir = os.path.join(root_derivatives_dir_path, 'Dartel', 'work')
    wf.connect(smoothing_node, 'smoothed_files', sink_node, 'smoothed_files')

    # Run the workflow.
    try:
        wf.run()
    except Exception as e:
        print(f"Workflow execution error: {e}")
        return []

    # Collect the paths of the output files saved in the analysis.
    output_files = []
    for root, dirs, files in os.walk(smooth_dir):
        for file in files:
            output_files.append(os.path.join(root, file))

    return output_files