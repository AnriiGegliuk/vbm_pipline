"""
Created on 10/06/2024

@author: Andrii Gegliuk

"""
import os
import re
import shutil
from colorama import init, Fore, Style

init(autoreset=True)

def extract_subject_name(subject_file_path):
    """
    Extracts the subject name from a given file.
    """
    try:
        with open(subject_file_path, 'r') as file:
            content = file.read()
            match = re.search(r'##\$SUBJECT_study_name=\(\s*\d+\s*\)\s*<([^>]+)>', content, re.MULTILINE)
            if match:
                return re.sub(r'\W+', '_', match.group(1))
    except IOError as e:
        print(Fore.RED + Style.BRIGHT + f"Unable to read file {subject_file_path}: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"An error occurred: {e}" + Style.RESET_ALL)
    return None

def find_t2_directories(root_dir):
    """
    Searches for directories containing T2 data within a given root directory.
    """
    t2_dirs = []
    for subdir, dirs, files in os.walk(root_dir):
        if 'method' in files:
            method_file_path = os.path.join(subdir, 'method')
            with open(method_file_path, 'r') as f:
                content = f.read()
                if "RARE" in content: # check if this should be correct naming
                    acqp_file_path = os.path.join(subdir, 'acqp')
                    if os.path.exists(acqp_file_path):
                        with open(acqp_file_path, 'r') as acqp_file:
                            acqp_content = acqp_file.read()
                            if 'T2_3D_RARE' in acqp_content: # check if this should be correct naming
                                t2_dirs.append(subdir)
    return t2_dirs

def create_and_process_t2_dirs(root_dir, output_dir):
    """
    Identifies and processes T2 data directories within a given root directory.
    """
    t2_dirs = find_t2_directories(root_dir)
    
    for t2_dir in t2_dirs:
        subject_file_path = os.path.join(t2_dir, '..', 'subject')
        subject_name = extract_subject_name(subject_file_path)
        
        if subject_name:
            subject_preprocessing_dir = os.path.join(output_dir, subject_name)
            os.makedirs(subject_preprocessing_dir, exist_ok=True)
            
            source_dir = os.path.join(t2_dir, 'pdata', '4', 'nifti')
            nii_files = [file for file in os.listdir(source_dir) if file.endswith('.nii')]
            if nii_files:
                for nii_file in nii_files:
                    source_path = os.path.join(source_dir, nii_file)
                    destination_path = os.path.join(subject_preprocessing_dir, nii_file)
                    
                    try:
                        shutil.copy(source_path, destination_path)
                        print(Fore.GREEN + Style.BRIGHT + f"T2 data {nii_file} copied for {subject_name}")
                    except IOError as e:
                        print(Fore.RED + Style.BRIGHT + f"Failed to copy T2 data for {subject_name}: {e}")
            else:
                print(Fore.RED + Style.BRIGHT + f"No .nii files found in {source_dir} for {subject_name}")
        else:
            print(Fore.RED + Style.BRIGHT + f"No subject name extracted for T2 directory: {t2_dir}")


