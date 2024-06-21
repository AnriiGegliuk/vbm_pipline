"""
Created on 04/28/2024

@author: Andrii Gegliuk

"""
import os
import json

def list_projects(input_dir):
    """
    Lists all subdirectories within a specified directory.
    
        Args:
            - input_dir (str): The directory from which to list subdirectories.

        Returns:
            - list: A list of subdirectory names, or an empty list if an error occurs.
    """
    try:
        dir_list=[d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
        return list(filter(lambda x:not os.path.basename(x).startswith("_"),dir_list))
    except OSError as e:
        print(f"Error accessing directory {input_dir}: {e}")
        return []
    

def select_project(projects):
    """
    Prompts the user to select a project from a list of projects.

        Args:
            - projects (list of str): A list of project names to choose from.

        Returns:
            - str: The selected project name, or None if the selection is invalid.
    """
    for idx, project in enumerate(projects):
        print(f"{idx + 1}: {project}")
    choice = int(input("Select a project number: ")) - 1
    if 0 <= choice < len(projects):
        return projects[choice]
    else:
        print("Invalid project. There is no project with this index.")
        return None