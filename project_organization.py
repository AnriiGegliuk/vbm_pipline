import os
from colorama import init, Fore, Style, Back

from modalities.t2_extraction_bruker import create_and_process_t2_dirs
from modalities.utilities.utils import list_projects, select_project
from modalities.utilities.parameters import *


if __name__ == "__main__":
    input_dir = RAW_DATA
    output_dir = ANALYSIS_DATA

    # function listing all directories within input folder (input folder expected to have only raw data under the specified project name)
    projects = list_projects(input_dir)

    if projects:
        # processing data based on the project that was selected
        selected_project = select_project(projects)

        if selected_project:
            project_input_dir = os.path.join(input_dir, selected_project)

            if not any(os.listdir(project_input_dir)):
                print(Fore.RED + Style.BRIGHT + f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis." + Style.RESET_ALL)
            else:

                project_output_dir = os.path.join(output_dir, selected_project, 'T2', 'preprocessing')
                os.makedirs(project_output_dir, exist_ok=True)
                print(Back.GREEN + f"Processing data for project {selected_project}..." + Style.RESET_ALL )
                
                # STEP T1: Data extraction and preparation
                create_and_process_t2_dirs(project_input_dir, project_output_dir)