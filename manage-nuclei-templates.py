#!/usr/bin/env python3

import os
import shutil
import subprocess
import uuid  # for generating unique filenames

# Function to count total number of templates matching keywords
def count_templates(template_dir, keywords=None):
    if keywords:
        template_count = 0
        for root, _, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.yaml'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if any(keyword.lower() in content.lower() for keyword in keywords):
                            template_count += 1
        return template_count
    else:
        templates = subprocess.run(['find', template_dir, '-type', 'f', '-name', '*.yaml'], stdout=subprocess.PIPE, universal_newlines=True)
        total_templates = len(templates.stdout.strip().split('\n'))
        return total_templates

# Function to remove duplicates using fdupes
def remove_duplicates(template_dir):
    subprocess.run(['sudo', 'apt-get', 'install', 'fdupes'])  # Install fdupes if not already installed
    subprocess.run(['fdupes', '-rdN', template_dir])

# Function to organize templates into folders based on keywords
def organize_templates(template_dir, keywords):
    organized_dir = os.path.join(template_dir, 'organized')
    os.makedirs(organized_dir, exist_ok=True)

    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                
                # Determine the appropriate folder based on keywords
                target_dir = None
                for keyword in keywords:
                    if keyword.lower() in file.lower():
                        target_dir = os.path.join(organized_dir, keyword)
                        break
                
                if target_dir is None:
                    target_dir = os.path.join(organized_dir, 'other')
                
                os.makedirs(target_dir, exist_ok=True)
                
                # Generate a unique filename to avoid overwriting existing files
                unique_filename = str(uuid.uuid4())[:8] + '_' + file
                target_file_path = os.path.join(target_dir, unique_filename)
                
                shutil.move(file_path, target_file_path)

if __name__ == "__main__":
    # Get user input for template directory
    template_dir = input("Enter the path to the directory containing templates: ").strip()
    if not os.path.isdir(template_dir):
        print(f"Error: {template_dir} is not a valid directory.")
        exit(1)

    # Get user input for keywords
    keywords_input = input("Enter keywords to organize templates (comma-separated, e.g., CVE,XSS,RCE): ").strip()
    keywords = keywords_input.split(',') if keywords_input else []

    total_templates = count_templates(template_dir, keywords)
    print(f"Total templates found: {total_templates}")

    print("Removing duplicates...")
    remove_duplicates(template_dir)

    print("Organizing templates...")
    organize_templates(template_dir, keywords)

    print("Organizing complete.")
