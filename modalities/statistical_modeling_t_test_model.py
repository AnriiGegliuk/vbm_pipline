# import os
# from typing import List
# import csv
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import TwoSampleTTestDesign

# def join_filepath(parts: List[str]) -> str:
#     """ Utility function to join file paths. """
#     return os.path.join(*parts)

# def get_file_name_without_extension(file_path: str) -> str:
#     return os.path.splitext(os.path.basename(file_path))[0]

# def get_derivatives_file_paths(base_dir: str, wf_input_name: str, file_pattern: str) -> List[str]:
#     """ Utility function to get file paths matching a pattern in the derivatives directory. """
#     matched_files = []
#     for root, _, files in os.walk(base_dir):
#         for file in files:
#             if file == file_pattern.replace("{wf_input_name}", wf_input_name):
#                 matched_files.append(os.path.join(root, file))
#     return matched_files

# def create_two_sample_t_test_model(contrasts_name: str, contrast1_input_path_list: List[str],
#                                    contrast2_input_path_list: List[str], smoothing_dir_path: str,
#                                    #brain_volume_dir_path: str, 
#                                    model_dir_path: str) -> List[str]:
#     """ Create a two-sample t-test model by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#twosamplettestdesign
#     for the details of the Nipype TwoSampleTTestDesign parameters.

#     Parameters
#     ----------
#     contrasts_name : str
#         Contrast pair name. It is used as a label for the comparison between the two groups.
#     contrast1_input_path_list : list[str]
#         Paths of workflow input files categorized by contrast1.
#     contrast2_input_path_list : list[str]
#         Paths of workflow input files categorized by contrast2.
#     smoothing_dir_path : str
#         Path of the directory storing the analysis results performed by the vbm_smoothing node.
#     #brain_volume_dir_path : str
#         #Path of the directory storing the analysis results performed by the vbm_total_brain_volume node.
#     model_dir_path : str
#         Path of the directory storing the analysis results performed by this node.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """

#     # Get contrast1 smoothed file paths.
#     contrast1_smoothed_file_list = []
#     for wf_input_path in contrast1_input_path_list:
#         wf_input_name = get_file_name_without_extension(wf_input_path)
#         path_list = get_derivatives_file_paths(smoothing_dir_path, wf_input_name, f'smwc1{wf_input_name}.nii')
#         contrast1_smoothed_file_list += path_list

#     # Get contrast2 smoothed file paths.
#     contrast2_smoothed_file_list = []
#     for wf_input_path in contrast2_input_path_list:
#         wf_input_name = get_file_name_without_extension(wf_input_path)
#         path_list = get_derivatives_file_paths(smoothing_dir_path, wf_input_name, f'smwc1{wf_input_name}.nii')
#         contrast2_smoothed_file_list += path_list

#     # Summarize the total brain volumes in a single file.
#     # brain_volume_list = []
#     # for wf_input_path in contrast1_input_path_list + contrast2_input_path_list:
#     #     wf_input_name = get_file_name_without_extension(wf_input_path)
#     #     path_list = get_derivatives_file_paths(brain_volume_dir_path, wf_input_name, 'tbv.csv')
#     #     with open(path_list[0]) as file:
#     #         reader = csv.reader(file)
#     #         for row in reader:
#     #             brain_volume_list.append(float(row[0]))

#     model_subdir_path = join_filepath([model_dir_path, contrasts_name])
#     os.makedirs(model_subdir_path, exist_ok=True)
#     total_brain_volume_file_path = join_filepath([model_subdir_path, 'tbv.csv'])
#     # with open(total_brain_volume_file_path, mode='wt', encoding='utf-8') as file:
#     #     writer = csv.writer(file)
#     #     writer.writerow(brain_volume_list)

#     # Set a two-sample t-test modeling node.
#     model_node = Node(TwoSampleTTestDesign(), name='vbm_stats_modeling')
#     model_node.inputs.group1_files = contrast1_smoothed_file_list
#     model_node.inputs.group2_files = contrast2_smoothed_file_list
#     # model_node.inputs.global_calc_values = brain_volume_list
#     model_node.inputs.spm_mat_dir = model_subdir_path

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = model_dir_path

#     # Creates a workflow.
#     wf = Workflow(name='vbm_stats_modeling')
#     wf.connect([(model_node, sink_node,
#                  [('spm_mat_file', contrasts_name)])])

#     # Run the workflow.
#     try:
#         wf.run()
#     except Exception as e:
#         print(f"Workflow execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(model_subdir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files



# import os
# from typing import List
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import TwoSampleTTestDesign

# def join_filepath(parts: List[str]) -> str:
#     """ Utility function to join file paths. """
#     return os.path.join(*parts)

# def get_file_name_without_extension(file_path: str) -> str:
#     return os.path.splitext(os.path.basename(file_path))[0]

# def get_files_from_directory(directory: str, prefix: str) -> List[str]:
#     """ Utility function to get files from a directory with a specific prefix. """
#     files = []
#     for root, _, filenames in os.walk(directory):
#         for filename in filenames:
#             if filename.startswith(prefix):
#                 files.append(os.path.join(root, filename))
#     return files

# def create_two_sample_t_test_model(contrasts_name: str, smoothing_dir_path: str,
#                                    model_dir_path: str) -> List[str]:
#     """ Create a two-sample t-test model by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#twosamplettestdesign
#     for the details of the Nipype TwoSampleTTestDesign parameters.

#     Parameters
#     ----------
#     contrasts_name : str
#         Contrast pair name. It is used as a label for the comparison between the two groups.
#     smoothing_dir_path : str
#         Path of the directory storing the analysis results performed by the vbm_smoothing node.
#     model_dir_path : str
#         Path of the directory storing the analysis results performed by this node.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """
    
#     smoothed_files_dir = os.path.join(smoothing_dir_path, 'smoothed_files')

#     # Automatically detect contrast files from the smoothed files directory
#     contrast1_files = get_files_from_directory(smoothed_files_dir, 'smwc1T2_')
#     contrast2_files = get_files_from_directory(smoothed_files_dir, 'smwc1T2_')

#     if not contrast1_files or not contrast2_files:
#         print("No smoothed files found for contrasts.")
#         return []

#     # Separate the files into two groups for the test
#     mid_point = len(contrast1_files) // 2
#     group1_files = contrast1_files[:mid_point]
#     group2_files = contrast1_files[mid_point:]

#     model_subdir_path = join_filepath([model_dir_path, contrasts_name])
#     os.makedirs(model_subdir_path, exist_ok=True)

#     # Set a two-sample t-test modeling node.
#     model_node = Node(TwoSampleTTestDesign(), name='vbm_stats_modeling')
#     model_node.inputs.group1_files = group1_files
#     model_node.inputs.group2_files = group2_files
#     model_node.inputs.spm_mat_dir = model_subdir_path

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = model_dir_path

#     # Creates a workflow.
#     wf = Workflow(name='vbm_stats_modeling')
#     wf.connect([(model_node, sink_node,
#                  [('spm_mat_file', contrasts_name)])])

#     # Run the workflow.
#     try:
#         wf.run()
#     except Exception as e:
#         print(f"Workflow execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(model_subdir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files


# import os
# from typing import List
# from nipype import Node, Workflow
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import TwoSampleTTestDesign

# def join_filepath(parts: List[str]) -> str:
#     """ Utility function to join file paths. """
#     return os.path.join(*parts)

# def get_file_name_without_extension(file_path: str) -> str:
#     return os.path.splitext(os.path.basename(file_path))[0]

# def get_files_from_directory(directory: str, prefix: str) -> List[str]:
#     """ Utility function to get files from a directory with a specific prefix. """
#     files = []
#     for root, _, filenames in os.walk(directory):
#         for filename in filenames:
#             if filename.startswith(prefix):
#                 files.append(os.path.join(root, filename))
#     return files

# def split_files_into_groups(files: List[str], condition1_subjects: List[str], condition2_subjects: List[str]) -> (List[str], List[str]):
#     """ Split files into two groups based on subject lists for two conditions. """
#     group1_files = [f for f in files if any(subj in f for subj in condition1_subjects)]
#     group2_files = [f for f in files if any(subj in f for subj in condition2_subjects)]
#     return group1_files, group2_files

# def find_conditions_and_subjects(root_dir: str) -> (List[str], List[str], List[str]):
#     """ Automatically detect conditions and subjects. """
#     conditions = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and d != 'Dartel']
#     condition1_subjects = []
#     condition2_subjects = []
    
#     condition1_path = os.path.join(root_dir, conditions[0])
#     condition2_path = os.path.join(root_dir, conditions[1])
    
#     for subject in os.listdir(condition1_path):
#         subject_path = os.path.join(condition1_path, subject)
#         if os.path.isdir(subject_path):
#             condition1_subjects.append(subject)
    
#     for subject in os.listdir(condition2_path):
#         subject_path = os.path.join(condition2_path, subject)
#         if os.path.isdir(subject_path):
#             condition2_subjects.append(subject)
    
#     return conditions, condition1_subjects, condition2_subjects

# def create_two_sample_t_test_model(root_dir: str, contrasts_name: str) -> List[str]:
#     """ Create a two-sample t-test model by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#twosamplettestdesign
#     for the details of the Nipype TwoSampleTTestDesign parameters.

#     Parameters
#     ----------
#     root_dir : str
#         Path of the root directory containing conditions and subjects.
#     contrasts_name : str
#         Contrast pair name. It is used as a label for the comparison between the two groups.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """
#     conditions, condition1_subjects, condition2_subjects = find_conditions_and_subjects(root_dir)

#     # Print detected conditions
#     print(f"Detected conditions: {conditions}")
#     print(f"Detected subjects for {conditions[0]}: {condition1_subjects}")
#     print(f"Detected subjects for {conditions[1]}: {condition2_subjects}")

#     smoothed_files_dir = os.path.join(root_dir, 'Dartel', 'output', 'smoothed_files', 'smoothed_files')
#     smoothed_files = get_files_from_directory(smoothed_files_dir, 'smwc1T2_')

#     if not smoothed_files:
#         print("No smoothed files found.")
#         return []

#     # Split files into two groups based on conditions
#     group1_files, group2_files = split_files_into_groups(smoothed_files, condition1_subjects, condition2_subjects)

#     if not group1_files or not group2_files:
#         print("Missing files for one or both groups.")
#         return []

#     model_subdir_path = join_filepath([root_dir, 'Dartel', 'output', 'model_dir', contrasts_name])
#     os.makedirs(model_subdir_path, exist_ok=True)

#     # Set a two-sample t-test modeling node.
#     model_node = Node(TwoSampleTTestDesign(), name='vbm_stats_modeling')
#     model_node.inputs.group1_files = group1_files
#     model_node.inputs.group2_files = group2_files
#     model_node.inputs.spm_mat_dir = model_subdir_path

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = join_filepath([root_dir, 'Dartel', 'output'])

#     # Create a workflow.
#     wf = Workflow(name='vbm_stats_modeling')
#     wf.base_dir = join_filepath([root_dir, 'Dartel', 'work'])
#     wf.connect([(model_node, sink_node,
#                  [('spm_mat_file', f'{contrasts_name}.@spm_mat_file')])])
    
#     # Run the workflow.
#     try:
#         wf.run()
#     except Exception as e:
#         print(f"Workflow execution error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(model_subdir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files



# works well as expected

# import os
# from typing import List
# from nipype import Node, Workflow, config, logging
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import TwoSampleTTestDesign

# def join_filepath(parts: List[str]) -> str:
#     """ Utility function to join file paths. """
#     return os.path.join(*parts)

# def get_file_name_without_extension(file_path: str) -> str:
#     return os.path.splitext(os.path.basename(file_path))[0]

# def get_files_from_directory(directory: str, prefix: str) -> List[str]:
#     """ Utility function to get files from a directory with a specific prefix. """
#     files = []
#     for root, _, filenames in os.walk(directory):
#         for filename in filenames:
#             if filename.startswith(prefix):
#                 files.append(os.path.join(root, filename))
#     return files

# def split_files_into_groups(files: List[str], condition1_subjects: List[str], condition2_subjects: List[str]) -> (List[str], List[str]):
#     """ Split files into two groups based on subject lists for two conditions. """
#     group1_files = [f for f in files if any(subj in f for subj in condition1_subjects)]
#     group2_files = [f for f in files if any(subj in f for subj in condition2_subjects)]
#     return group1_files, group2_files

# def find_conditions_and_subjects(root_dir: str) -> (List[str], List[str], List[str]):
#     """ Automatically detect conditions and subjects. """
#     conditions = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and d != 'Dartel']
#     condition1_subjects = []
#     condition2_subjects = []
    
#     condition1_path = os.path.join(root_dir, conditions[0])
#     condition2_path = os.path.join(root_dir, conditions[1])
    
#     for subject in os.listdir(condition1_path):
#         subject_path = os.path.join(condition1_path, subject)
#         if os.path.isdir(subject_path):
#             condition1_subjects.append(subject)
    
#     for subject in os.listdir(condition2_path):
#         subject_path = os.path.join(condition2_path, subject)
#         if os.path.isdir(subject_path):
#             condition2_subjects.append(subject)
    
#     return conditions, condition1_subjects, condition2_subjects

# def create_two_sample_t_test_model(root_dir: str, contrasts_name: str) -> List[str]:
#     """ Create a two-sample t-test model by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#twosamplettestdesign
#     for the details of the Nipype TwoSampleTTestDesign parameters.

#     Parameters
#     ----------
#     root_dir : str
#         Path of the root directory containing conditions and subjects.
#     contrasts_name : str
#         Contrast pair name. It is used as a label for the comparison between the two groups.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """
#     conditions, condition1_subjects, condition2_subjects = find_conditions_and_subjects(root_dir)

#     # Print detected conditions
#     print(f"Detected conditions: {conditions}")
#     print(f"Detected subjects for {conditions[0]}: {condition1_subjects}")
#     print(f"Detected subjects for {conditions[1]}: {condition2_subjects}")

#     smoothed_files_dir = os.path.join(root_dir, 'Dartel', 'output', 'smoothed_files', 'smoothed_files')
#     smoothed_files = get_files_from_directory(smoothed_files_dir, 'smwc1T2_')

#     if not smoothed_files:
#         print("No smoothed files found.")
#         return []

#     # Split files into two groups based on conditions
#     group1_files, group2_files = split_files_into_groups(smoothed_files, condition1_subjects, condition2_subjects)

#     if not group1_files or not group2_files:
#         print("Missing files for one or both groups.")
#         return []

#     model_subdir_path = join_filepath([root_dir, 'Dartel', 'work', 'vbm_stats_modeling', 'vbm_stats_modeling'])
#     os.makedirs(model_subdir_path, exist_ok=True)

#     # Set a two-sample t-test modeling node.
#     model_node = Node(TwoSampleTTestDesign(), name='vbm_stats_modeling')
#     model_node.inputs.group1_files = group1_files
#     model_node.inputs.group2_files = group2_files
#     model_node.inputs.spm_mat_dir = model_subdir_path
#     model_node.inputs.global_calc_omit = True  # Omit global calculation
#     model_node.inputs.threshold_mask_relative = 0.2  # Set masking threshold

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = os.path.join(root_dir, 'Dartel', 'output')
#     sink_node.inputs.substitutions = [(f'{contrasts_name}/SPM.mat', 'SPM.mat')]  # Ensure correct substitution

#     # Creates a workflow.
#     wf = Workflow(name='vbm_stats_modeling')
#     wf.base_dir = os.path.join(root_dir, 'Dartel', 'work')
#     wf.connect(model_node, 'spm_mat_file', sink_node, f'{contrasts_name}.@spm_mat_file')

#     # Increase verbosity of the logs
#     cfg = dict(logging=dict(workflow_level='DEBUG'))
#     config.update_config(cfg)
#     logging.update_logging(config)

#     # Run the workflow with parallel processing
#     try:
#         wf.run('MultiProc', plugin_args={'n_procs': 4})
#     except Exception as e:
#         print(f"Workflow execution error: {e}")
#         return []

#     # Check if the SPM.mat file was created successfully
#     spm_mat_path = os.path.join(model_subdir_path, 'SPM.mat')
#     if not os.path.exists(spm_mat_path):
#         print(f"SPM.mat file not found in {spm_mat_path}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(model_subdir_path):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files




# works well generates statistical_analysis folder but does not place output of estimation there

# import os
# import shutil
# from typing import List
# from nipype import Node, Workflow, config, logging
# from nipype.interfaces.io import DataSink
# from nipype.interfaces.spm.model import TwoSampleTTestDesign, EstimateModel

# def join_filepath(parts: List[str]) -> str:
#     """ Utility function to join file paths. """
#     return os.path.join(*parts)

# def get_file_name_without_extension(file_path: str) -> str:
#     return os.path.splitext(os.path.basename(file_path))[0]

# def get_files_from_directory(directory: str, prefix: str) -> List[str]:
#     """ Utility function to get files from a directory with a specific prefix. """
#     files = []
#     for root, _, filenames in os.walk(directory):
#         for filename in filenames:
#             if filename.startswith(prefix):
#                 files.append(os.path.join(root, filename))
#     return files

# def split_files_into_groups(files: List[str], condition1_subjects: List[str], condition2_subjects: List[str]) -> (List[str], List[str]):
#     """ Split files into two groups based on subject lists for two conditions. """
#     group1_files = [f for f in files if any(subj in f for subj in condition1_subjects)]
#     group2_files = [f for f in files if any(subj in f for subj in condition2_subjects)]
#     return group1_files, group2_files

# def find_conditions_and_subjects(root_dir: str) -> (List[str], List[str], List[str]):
#     """ Automatically detect conditions and subjects. """
#     conditions = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and d != 'Dartel']
#     condition1_subjects = []
#     condition2_subjects = []
    
#     condition1_path = os.path.join(root_dir, conditions[0])
#     condition2_path = os.path.join(root_dir, conditions[1])
    
#     for subject in os.listdir(condition1_path):
#         subject_path = os.path.join(condition1_path, subject)
#         if os.path.isdir(subject_path):
#             condition1_subjects.append(subject)
    
#     for subject in os.listdir(condition2_path):
#         subject_path = os.path.join(condition2_path, subject)
#         if os.path.isdir(subject_path):
#             condition2_subjects.append(subject)
    
#     return conditions, condition1_subjects, condition2_subjects

# def create_two_sample_t_test_model(root_dir: str, contrasts_name: str) -> List[str]:
#     """ Create a two-sample t-test model by Nipype-SPM12.
#     See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#twosamplettestdesign
#     for the details of the Nipype TwoSampleTTestDesign parameters.

#     Parameters
#     ----------
#     root_dir : str
#         Path of the root directory containing conditions and subjects.
#     contrasts_name : str
#         Contrast pair name. It is used as a label for the comparison between the two groups.

#     Returns
#     ----------
#     output_file_path_list : list[str]
#         Paths of the output files generated in the analysis.
#     """
#     conditions, condition1_subjects, condition2_subjects = find_conditions_and_subjects(root_dir)

#     # Print detected conditions
#     print(f"Detected conditions: {conditions}")
#     print(f"Detected subjects for {conditions[0]}: {condition1_subjects}")
#     print(f"Detected subjects for {conditions[1]}: {condition2_subjects}")

#     smoothed_files_dir = os.path.join(root_dir, 'Dartel', 'output', 'smoothed_files', 'smoothed_files')
#     smoothed_files = get_files_from_directory(smoothed_files_dir, 'smwc1T2_')

#     if not smoothed_files:
#         print("No smoothed files found.")
#         return []

#     # Split files into two groups based on conditions
#     group1_files, group2_files = split_files_into_groups(smoothed_files, condition1_subjects, condition2_subjects)

#     if not group1_files or not group2_files:
#         print("Missing files for one or both groups.")
#         return []

#     model_subdir_path = join_filepath([root_dir, 'Dartel', 'work', 'vbm_stats_modeling', 'vbm_stats_modeling'])
#     os.makedirs(model_subdir_path, exist_ok=True)

#     # Set a two-sample t-test modeling node.
#     model_node = Node(TwoSampleTTestDesign(), name='vbm_stats_modeling')
#     model_node.inputs.group1_files = group1_files
#     model_node.inputs.group2_files = group2_files
#     model_node.inputs.spm_mat_dir = model_subdir_path
#     model_node.inputs.global_calc_omit = True  # Omit global calculation
#     model_node.inputs.threshold_mask_relative = 0.2  # Set masking threshold

#     # Set a DataSink node.
#     sink_node = Node(DataSink(), name='data_sink')
#     sink_node.inputs.base_directory = os.path.join(root_dir, 'Dartel', 'output')
#     sink_node.inputs.substitutions = [(f'{contrasts_name}/SPM.mat', 'SPM.mat')]  # Ensure correct substitution

#     # Creates a workflow.
#     wf = Workflow(name='vbm_stats_modeling')
#     wf.base_dir = os.path.join(root_dir, 'Dartel', 'work')
#     wf.connect(model_node, 'spm_mat_file', sink_node, f'{contrasts_name}.@spm_mat_file')

#     # Increase verbosity of the logs
#     cfg = dict(logging=dict(workflow_level='DEBUG'))
#     config.update_config(cfg)
#     logging.update_logging(config)

#     # Run the workflow with parallel processing
#     try:
#         wf.run('MultiProc', plugin_args={'n_procs': 4})
#     except Exception as e:
#         print(f"Workflow execution error: {e}")
#         return []

#     # Check if the SPM.mat file was created successfully
#     spm_mat_path = os.path.join(model_subdir_path, 'SPM.mat')
#     if not os.path.exists(spm_mat_path):
#         print(f"SPM.mat file not found in {spm_mat_path}")
#         return []

#     # Create statistical_analysis directory and copy SPM.mat file
#     analysis_dir = join_filepath([root_dir, 'statistical_analysis'])
#     os.makedirs(analysis_dir, exist_ok=True)
#     shutil.copy(spm_mat_path, analysis_dir)

#     # Estimate the model
#     estimate_model_node = Node(EstimateModel(), name='estimate_model')
#     estimate_model_node.inputs.spm_mat_file = os.path.join(analysis_dir, 'SPM.mat')
#     estimate_model_node.inputs.estimation_method = {'Classical': 1}

#     # Create a new workflow for estimation
#     wf_estimate = Workflow(name='vbm_estimate_model')
#     wf_estimate.base_dir = os.path.join(root_dir, 'Dartel', 'work')
#     wf_estimate.add_nodes([estimate_model_node])

#     try:
#         wf_estimate.run('MultiProc', plugin_args={'n_procs': 4})
#     except Exception as e:
#         print(f"Model estimation error: {e}")
#         return []

#     # Collect the paths of the output files saved in the analysis.
#     output_files = []
#     for root, _, files in os.walk(analysis_dir):
#         for file in files:
#             output_files.append(os.path.join(root, file))

#     return output_files



import os
import shutil
from typing import List
from nipype import Node, Workflow, config, logging
from nipype.interfaces.io import DataSink
from nipype.interfaces.spm.model import TwoSampleTTestDesign, EstimateModel

def join_filepath(parts: List[str]) -> str:
    """ Utility function to join file paths. """
    return os.path.join(*parts)

def get_file_name_without_extension(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]

def get_files_from_directory(directory: str, prefix: str) -> List[str]:
    """ Utility function to get files from a directory with a specific prefix. """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith(prefix):
                files.append(os.path.join(root, filename))
    return files

def split_files_into_groups(files: List[str], condition1_subjects: List[str], condition2_subjects: List[str]) -> (List[str], List[str]):
    """ Split files into two groups based on subject lists for two conditions. """
    group1_files = [f for f in files if any(subj in f for subj in condition1_subjects)]
    group2_files = [f for f in files if any(subj in f for subj in condition2_subjects)]
    return group1_files, group2_files

def find_conditions_and_subjects(root_dir: str) -> (List[str], List[str], List[str]):
    """ Automatically detect conditions and subjects. """
    conditions = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and d != 'Dartel']
    condition1_subjects = []
    condition2_subjects = []
    
    condition1_path = os.path.join(root_dir, conditions[0])
    condition2_path = os.path.join(root_dir, conditions[1])
    
    for subject in os.listdir(condition1_path):
        subject_path = os.path.join(condition1_path, subject)
        if os.path.isdir(subject_path):
            condition1_subjects.append(subject)
    
    for subject in os.listdir(condition2_path):
        subject_path = os.path.join(condition2_path, subject)
        if os.path.isdir(subject_path):
            condition2_subjects.append(subject)
    
    return conditions, condition1_subjects, condition2_subjects

def create_two_sample_t_test_model(root_dir: str, contrasts_name: str) -> List[str]:
    """ Create a two-sample t-test model by Nipype-SPM12.
    See https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.spm.model.html#twosamplettestdesign
    for the details of the Nipype TwoSampleTTestDesign parameters.

    Parameters
    ----------
    root_dir : str
        Path of the root directory containing conditions and subjects.
    contrasts_name : str
        Contrast pair name. It is used as a label for the comparison between the two groups.

    Returns
    ----------
    output_file_path_list : list[str]
        Paths of the output files generated in the analysis.
    """
    conditions, condition1_subjects, condition2_subjects = find_conditions_and_subjects(root_dir)

    # Print detected conditions
    print(f"Detected conditions: {conditions}")
    print(f"Detected subjects for {conditions[0]}: {condition1_subjects}")
    print(f"Detected subjects for {conditions[1]}: {condition2_subjects}")

    smoothed_files_dir = os.path.join(root_dir, 'Dartel', 'output', 'smoothed_files', 'smoothed_files')
    smoothed_files = get_files_from_directory(smoothed_files_dir, 'smwc1T2_')

    if not smoothed_files:
        print("No smoothed files found.")
        return []

    # Split files into two groups based on conditions
    group1_files, group2_files = split_files_into_groups(smoothed_files, condition1_subjects, condition2_subjects)

    if not group1_files or not group2_files:
        print("Missing files for one or both groups.")
        return []

    model_subdir_path = join_filepath([root_dir, 'Dartel', 'work', 'vbm_stats_modeling', 'vbm_stats_modeling'])
    os.makedirs(model_subdir_path, exist_ok=True)

    # Set a two-sample t-test modeling node.
    model_node = Node(TwoSampleTTestDesign(), name='vbm_stats_modeling')
    model_node.inputs.group1_files = group1_files
    model_node.inputs.group2_files = group2_files
    model_node.inputs.spm_mat_dir = model_subdir_path
    model_node.inputs.global_calc_omit = True  # Omit global calculation
    model_node.inputs.threshold_mask_relative = 0.2  # Set masking threshold

    # Set a DataSink node.
    sink_node = Node(DataSink(), name='data_sink')
    sink_node.inputs.base_directory = os.path.join(root_dir, 'Dartel', 'output')
    sink_node.inputs.substitutions = [(f'{contrasts_name}/SPM.mat', 'SPM.mat')]  # Ensure correct substitution

    # Creates a workflow.
    wf = Workflow(name='vbm_stats_modeling')
    wf.base_dir = os.path.join(root_dir, 'Dartel', 'work')
    wf.connect(model_node, 'spm_mat_file', sink_node, f'{contrasts_name}.@spm_mat_file')

    # Increase verbosity of the logs
    cfg = dict(logging=dict(workflow_level='DEBUG'))
    config.update_config(cfg)
    logging.update_logging(config)

    # Run the workflow with parallel processing
    try:
        wf.run('MultiProc', plugin_args={'n_procs': 4})
    except Exception as e:
        print(f"Workflow execution error: {e}")
        return []

    # Check if the SPM.mat file was created successfully
    spm_mat_path = os.path.join(model_subdir_path, 'SPM.mat')
    if not os.path.exists(spm_mat_path):
        print(f"SPM.mat file not found in {spm_mat_path}")
        return []

    # Create statistical_analysis directory and copy SPM.mat file
    analysis_dir = join_filepath([root_dir, 'statistical_analysis'])
    os.makedirs(analysis_dir, exist_ok=True)
    shutil.copy(spm_mat_path, analysis_dir)

    # Estimate the model
    estimate_model_node = Node(EstimateModel(), name='estimate_model')
    estimate_model_node.inputs.spm_mat_file = os.path.join(analysis_dir, 'SPM.mat')
    estimate_model_node.inputs.estimation_method = {'Classical': 1}

    # Create a new workflow for estimation
    wf_estimate = Workflow(name='vbm_estimate_model')
    wf_estimate.base_dir = os.path.join(root_dir, 'Dartel', 'work')
    wf_estimate.add_nodes([estimate_model_node])

    try:
        wf_estimate.run('MultiProc', plugin_args={'n_procs': 4})
    except Exception as e:
        print(f"Model estimation error: {e}")
        return []

    # Define the paths for the estimated model output
    estimate_output_dir = os.path.join(root_dir, 'Dartel', 'work', 'vbm_estimate_model', 'estimate_model')

    # Copy the .nii result files to the statistical_analysis directory
    nii_files = [f for f in os.listdir(estimate_output_dir) if f.endswith('.nii')]
    for nii_file in nii_files:
        shutil.copy(os.path.join(estimate_output_dir, nii_file), analysis_dir)

    # Collect the paths of the output files saved in the analysis.
    output_files = []
    for root, _, files in os.walk(analysis_dir):
        for file in files:
            output_files.append(os.path.join(root, file))

    return output_files