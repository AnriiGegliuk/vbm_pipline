## works well with correct conditions and no model estimation required since it is estimated durring t_test


import os
from typing import List
from nipype import Node, Workflow
from nipype.interfaces.io import DataSink
from nipype.interfaces.spm.model import EstimateContrast


def perform_statistical_analysis(root_dir: str, contrasts_name: str) -> List[str]:
    """ Perform statistical analysis by Nipype-SPM12.
    See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatemodel and
    https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatecontrast
    for the details of the Nipype EstimateModel and EstimateContrast parameters, respectively.

    Parameters
        ----------
        root_dir : str
            Path of the root directory containing conditions and subjects.
        contrasts_name : str
            Contrast pair name such as <Between-factor A>-<Between-factor B>.

    Returns
        ----------
        output_file_path_list : list[str]
            Paths of the output files generated in the analysis.
    """
    
    # Define paths
    model_dir_path = os.path.join(root_dir, 'statistical_analysis')

    # Debug: Print the contrasts_name
    print(f"Contrasts name provided: {contrasts_name}")

    # Split contrast names based on '-'
    try:
        contrast1_name, contrast2_name = contrasts_name.split('-')
    except ValueError:
        raise ValueError("Contrasts name must be in the format 'contrast1-contrast2'")

    # Debug: Print the parsed contrast names
    print(f"Parsed contrast1_name: {contrast1_name}")
    print(f"Parsed contrast2_name: {contrast2_name}")

    # Set an EstimateContrast node.
    estimate_contrast_node = Node(EstimateContrast(), name='estimate_contrast')
    contrast1 = (f'{contrast1_name}>{contrast2_name}', 'T', ['Group_{1}', 'Group_{2}'], [1, -1])
    contrast2 = (f'{contrast1_name}<{contrast2_name}', 'T', ['Group_{1}', 'Group_{2}'], [-1, 1])

    # Debug: Print the constructed contrast names
    print(f"Constructed contrast1: {contrast1}")
    print(f"Constructed contrast2: {contrast2}")

    estimate_contrast_node.inputs.contrasts = [contrast1, contrast2]
    estimate_contrast_node.inputs.group_contrast = True

    # Set the beta_images and residual_image inputs
    beta_images = [os.path.join(model_dir_path, f'beta_000{i+1}.nii') for i in range(2)]
    estimate_contrast_node.inputs.beta_images = beta_images
    estimate_contrast_node.inputs.residual_image = os.path.join(model_dir_path, 'ResMS.nii')
    estimate_contrast_node.inputs.spm_mat_file = os.path.join(model_dir_path, 'SPM.mat')

    # Set a DataSink node.
    sink_node = Node(DataSink(), name='data_sink')
    sink_node.inputs.base_directory = model_dir_path

    # Create a workflow.
    wf = Workflow(name='vbm_stats_analysis')
    wf.base_dir = os.path.join(root_dir, 'Dartel', 'work')
    
    # Connect the nodes
    wf.connect([(estimate_contrast_node, sink_node, [
        ('spm_mat_file', f'{contrasts_name}.@spm_mat'),
        ('spmT_images', f'{contrasts_name}.@T'),
        ('con_images', f'{contrasts_name}.@con')
    ])])

    # Run the workflow.
    try:
        wf.run('MultiProc', plugin_args={'n_procs': 4})
    except Exception as e:
        print(f"Statistical analysis execution error: {e}")
        return []

    # Collect the paths of the output files saved in the analysis.
    output_files = []
    for root, _, files in os.walk(model_dir_path):
        for file in files:
            output_files.append(os.path.join(root, file))

    return output_files








# works well with correct conditions

# import os
# from typing import List
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import EstimateModel, EstimateContrast


# def perform_statistical_analysis(root_dir: str, contrasts_name: str) -> List[str]:
#     """ Perform statistical analysis by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatemodel and
#     https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatecontrast
#     for the details of the Nipype EstimateModel and EstimateContrast parameters, respectively.

#     Parameters
#         ----------
#         root_dir : str
#             Path of the root directory containing conditions and subjects.
#         contrasts_name : str
#             Contrast pair name such as <Between-factor A>-<Between-factor B>.

#     Returns
#         ----------
#         output_file_path_list : list[str]
#             Paths of the output files generated in the analysis.
#     """
    
#     # Define paths
#     model_dir_path = os.path.join(root_dir, 'statistical_analysis')

#     # Set an EstimateModel node.
#     estimate_model_node = Node(EstimateModel(estimation_method={'Classical': 1}), name='estimate_model')
#     estimate_model_node.inputs.spm_mat_file = os.path.join(model_dir_path, 'SPM.mat')

#     # Debug: Print the contrasts_name
#     print(f"Contrasts name provided: {contrasts_name}")

#     # Split contrast names based on '-'
#     try:
#         contrast1_name, contrast2_name = contrasts_name.split('-')
#     except ValueError:
#         raise ValueError("Contrasts name must be in the format 'contrast1-contrast2'")

#     # Debug: Print the parsed contrast names
#     print(f"Parsed contrast1_name: {contrast1_name}")
#     print(f"Parsed contrast2_name: {contrast2_name}")

#     # Set an EstimateContrast node.
#     estimate_contrast_node = Node(EstimateContrast(), name='estimate_contrast')
#     contrast1 = (f'{contrast1_name}>{contrast2_name}', 'T', ['Group_{1}', 'Group_{2}'], [1, -1])
#     contrast2 = (f'{contrast1_name}<{contrast2_name}', 'T', ['Group_{1}', 'Group_{2}'], [-1, 1])

#     # Debug: Print the constructed contrast names
#     print(f"Constructed contrast1: {contrast1}")
#     print(f"Constructed contrast2: {contrast2}")

#     estimate_contrast_node.inputs.contrasts = [contrast1, contrast2]
#     estimate_contrast_node.inputs.group_contrast = True

#     # Set the beta_images and residual_image inputs
#     beta_images = [os.path.join(model_dir_path, f'beta_000{i+1}.nii') for i in range(2)]
#     estimate_contrast_node.inputs.beta_images = beta_images
#     estimate_contrast_node.inputs.residual_image = os.path.join(model_dir_path, 'ResMS.nii')
#     estimate_contrast_node.inputs.spm_mat_file = os.path.join(model_dir_path, 'SPM.mat')

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = model_dir_path

#     # Create a workflow.
#     wf = Workflow(name='vbm_stats_analysis')
#     wf.base_dir = os.path.join(root_dir, 'Dartel', 'work')
    
#     # Connect the nodes
#     wf.connect(estimate_model_node, 'spm_mat_file', estimate_contrast_node, 'spm_mat_file')
#     wf.connect([(estimate_contrast_node, sink_node, [
#         ('spm_mat_file', f'{contrasts_name}.@spm_mat'),
#         ('spmT_images', f'{contrasts_name}.@T'),
#         ('con_images', f'{contrasts_name}.@con')
#     ])])

#     # Run the workflow.
#     try:
#         wf.run('MultiProc', plugin_args={'n_procs': 4})
#     except Exception as e:
#         print(f"Statistical analysis execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(model_dir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files





########################## working welllll!!!!!!!!!!!!!!!!!!!!! but strange conditions

# import os
# from typing import List
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import EstimateModel, EstimateContrast

# def perform_statistical_analysis(root_dir: str, contrasts_name: str) -> List[str]:
#     """ Perform statistical analysis by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatemodel and
#     https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatecontrast
#     for the details of the Nipype EstimateModel and EstimateContrast parameters, respectively.

#     Parameters
#         ----------
#         root_dir : str
#             Path of the root directory containing conditions and subjects.
#         contrasts_name : str
#             Contrast pair name such as <Between-factor A><Within-factor X>-<Between-factor B><Within-factor X>.

#     Returns
#         ----------
#         output_file_path_list : list[str]
#             Paths of the output files generated in the analysis.
#     """
    
#     # Define paths
#     model_dir_path = os.path.join(root_dir, 'statistical_analysis')

#     # Set an EstimateModel node.
#     estimate_model_node = Node(EstimateModel(estimation_method={'Classical': 1}), name='estimate_model')
#     estimate_model_node.inputs.spm_mat_file = os.path.join(model_dir_path, 'SPM.mat')

#     # Get contrast names such as <Between-factor A><Within-factor X>.
#     index = contrasts_name.find('>-<')
#     contrast1_name = contrasts_name[:(index + 1)]
#     contrast2_name = contrasts_name[(index + 2):]

#     # Set an EstimateContrast node.
#     estimate_contrast_node = Node(EstimateContrast(), name='estimate_contrast')
#     contrast1 = (contrast1_name + '>' + contrast2_name, 'T', ['Group_{1}', 'Group_{2}'], [1, -1])
#     contrast2 = (contrast1_name + '<' + contrast2_name, 'T', ['Group_{1}', 'Group_{2}'], [-1, 1])
#     estimate_contrast_node.inputs.contrasts = [contrast1, contrast2]
#     estimate_contrast_node.inputs.group_contrast = True

#     # Set the beta_images and residual_image inputs
#     beta_images = [os.path.join(model_dir_path, f'beta_000{i+1}.nii') for i in range(2)]
#     estimate_contrast_node.inputs.beta_images = beta_images
#     estimate_contrast_node.inputs.residual_image = os.path.join(model_dir_path, 'ResMS.nii')
#     estimate_contrast_node.inputs.spm_mat_file = os.path.join(model_dir_path, 'SPM.mat')

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = model_dir_path

#     # Create a workflow.
#     wf = Workflow(name='vbm_stats_analysis')
#     wf.base_dir = os.path.join(root_dir, 'Dartel', 'work')
    
#     # Connect the nodes
#     wf.connect(estimate_model_node, 'spm_mat_file', estimate_contrast_node, 'spm_mat_file')
#     wf.connect([(estimate_contrast_node, sink_node, [
#         ('spm_mat_file', f'{contrasts_name}.@spm_mat'),
#         ('spmT_images', f'{contrasts_name}.@T'),
#         ('con_images', f'{contrasts_name}.@con')
#     ])])

#     # Run the workflow.
#     try:
#         wf.run('MultiProc', plugin_args={'n_procs': 4})
#     except Exception as e:
#         print(f"Statistical analysis execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(model_dir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files


# import os
# from typing import List
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import EstimateModel, EstimateContrast

# def detect_conditions(model_dir_path: str) -> List[str]:
#     """ Detect conditions from the model directory path.
    
#     Parameters
#     ----------
#     model_dir_path : str
#         Path of the directory storing the analysis results.

#     Returns
#     ----------
#     conditions : list[str]
#         List of detected condition names.
#     """
#     ignored_dirs = {'Dartel', 'GUI_SPM_STATS', 'general_report.html', 'statistical_analysis'}
#     conditions = []

#     # List all directories in the model_dir_path
#     for item in os.listdir(model_dir_path):
#         item_path = os.path.join(model_dir_path, item)
#         if os.path.isdir(item_path) and item not in ignored_dirs:
#             conditions.append(item)

#     # Sort conditions alphabetically (case-insensitive)
#     conditions = sorted(conditions, key=str.lower)

#     return conditions

# def perform_statistical_analysis(root_dir: str, contrasts_name: str) -> List[str]:
#     """ Perform statistical analysis by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatemodel and
#     https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#estimatecontrast
#     for the details of the Nipype EstimateModel and EstimateContrast parameters, respectively.

#     Parameters
#         ----------
#         root_dir : str
#             Path of the root directory containing conditions and subjects.
#         contrasts_name : str
#             Contrast pair name such as <Between-factor A><Within-factor X>-<Between-factor B><Within-factor X>.

#     Returns
#         ----------
#         output_file_path_list : list[str]
#             Paths of the output files generated in the analysis.
#     """
    
#     # Define paths
#     model_dir_path = os.path.join(root_dir, 'statistical_analysis')

#     # Detect conditions from the model directory
#     conditions = detect_conditions(root_dir)
#     print(conditions)
    
#     if len(conditions) < 2:
#         raise ValueError("At least two conditions are required for contrast analysis.")

#     # Set an EstimateModel node.
#     estimate_model_node = Node(EstimateModel(estimation_method={'Classical': 1}), name='estimate_model')
#     estimate_model_node.inputs.spm_mat_file = os.path.join(model_dir_path, 'SPM.mat')

#     # Define contrasts dynamically based on detected conditions
#     contrast1 = (conditions[0] + '>' + conditions[1], 'T', conditions, [1, -1])
#     contrast2 = (conditions[0] + '<' + conditions[1], 'T', conditions, [-1, 1])
    
#     # Set an EstimateContrast node.
#     estimate_contrast_node = Node(EstimateContrast(), name='estimate_contrast')
#     estimate_contrast_node.inputs.contrasts = [contrast1, contrast2]
#     estimate_contrast_node.inputs.group_contrast = True

#     # Set the beta_images and residual_image inputs
#     beta_images = [os.path.join(model_dir_path, f'beta_{i+1:04d}.nii') for i in range(len(conditions))]
#     estimate_contrast_node.inputs.beta_images = beta_images
#     estimate_contrast_node.inputs.residual_image = os.path.join(model_dir_path, 'ResMS.nii')
#     estimate_contrast_node.inputs.spm_mat_file = os.path.join(model_dir_path, 'SPM.mat')

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = model_dir_path

#     # Create a workflow.
#     wf = Workflow(name='vbm_stats_analysis')
#     wf.base_dir = os.path.join(root_dir, 'Dartel', 'work')
    
#     # Connect the nodes
#     wf.connect(estimate_model_node, 'spm_mat_file', estimate_contrast_node, 'spm_mat_file')
#     wf.connect([(estimate_contrast_node, sink_node, [
#         ('spm_mat_file', f'{contrasts_name}.@spm_mat'),
#         ('spmT_images', f'{contrasts_name}.@T'),
#         ('con_images', f'{contrasts_name}.@con')
#     ])])

#     # Run the workflow.
#     try:
#         wf.run('MultiProc', plugin_args={'n_procs': 4})
#     except Exception as e:
#         print(f"Statistical analysis execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(model_dir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files