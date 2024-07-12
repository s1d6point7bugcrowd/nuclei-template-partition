#!/usr/bin/env python3

import os
import shutil
import subprocess

# Function to count total number of templates
def count_templates(template_dir):
    templates = subprocess.run(['find', template_dir, '-type', 'f', '-name', '*.yaml'], stdout=subprocess.PIPE, universal_newlines=True)
    total_templates = len(templates.stdout.strip().split('\n'))
    return total_templates

# Function to remove duplicates using fdupes
def remove_duplicates(template_dir):
    subprocess.run(['sudo', 'apt-get', 'install', 'fdupes'])  # Install fdupes if not already installed
    subprocess.run(['fdupes', '-rdN', template_dir])

# Function to organize templates into blocks of specified size
def organize_templates(template_dir, block_size):
    partitioned_dir = os.path.join(template_dir, 'partitioned')
    os.makedirs(partitioned_dir, exist_ok=True)

    current_dir = 1
    counter = 0

    for filename in os.listdir(template_dir):
        if filename.endswith('.yaml'):
            source_file = os.path.join(template_dir, filename)
            target_dir = os.path.join(partitioned_dir, str(current_dir))
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(source_file, target_dir)
            counter += 1

            if counter == block_size:
                current_dir += 1
                counter = 0

if __name__ == "__main__":
    # Get user input for template directory
    template_dir = input("Enter the path to the directory containing templates: ").strip()
    if not os.path.isdir(template_dir):
        print(f"Error: {template_dir} is not a valid directory.")
        exit(1)

    # Get user input for block size
    block_size = input("Enter the number of templates in each block: ").strip()
    try:
        block_size = int(block_size)
        if block_size <= 0:
            raise ValueError
    except ValueError:
        print("Error: Block size must be a positive integer.")
        exit(1)

    total_templates = count_templates(template_dir)
    print(f"Total templates found: {total_templates}")

    print("Removing duplicates...")
    remove_duplicates(template_dir)

    print(f"Organizing templates into blocks of {block_size}...")
    organize_templates(template_dir, block_size)

    print("Organizing complete.")
