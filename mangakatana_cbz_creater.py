#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile

"""
This script is forked from JacquesDuflos/mangakatana_cbz_creater and was updated
is meant to turn .zip files downloaded from mangakatana.com to a serie of .cbz files. 
The .zip files contain usually 10 chapters of a same manga stored as a serie of folders. 
The Script will create a .cbz file for each folder in the .zip file.
The .cbz file will be named as the name of the folder and will contain all the files in this folder.
The .cbz file will be stored in the same folder as the .zip file.
The script will also create a folder named "cbz" in the same folder as the .zip file and store all the .cbz files in this folder.
"""


def main():
    # Path to the root folder containing the .zip files
    root_folder = "here_goes_the_path_to_your_zip_files"

    # If no path is provided, use the current directory
    if not root_folder:
        root_folder = os.path.dirname(os.path.abspath(__file__))

    # Browse .zip files in the root folder
    for zip_file in os.listdir(root_folder):
        if zip_file.endswith(".zip"):
            zip_path = os.path.join(root_folder, zip_file)

            # Extract chapter name from .zip file name
            chapter_name = os.path.splitext(zip_file)[0]
            series_name = "-".join(chapter_name.split("_")[:-2])

            cbz_file = os.path.join(root_folder, "cbz")
            if not os.path.exists(cbz_file):
                os.makedirs(cbz_file)

            try:
                count = 0
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    for case_file in zip_ref.namelist():
                        if case_file.endswith("/") and case_file != chapter_name + "/":
                            count += 1
                            subfolder_name = os.path.basename(case_file[:-1])
                            path_cbz = os.path.join(
                                cbz_file, f"{series_name}_{subfolder_name}.cbz"
                            )

                            with zipfile.ZipFile(
                                path_cbz, "w", compression=zipfile.ZIP_DEFLATED
                            ) as cbz:
                                for file in zip_ref.namelist():
                                    if file.startswith(case_file):
                                        file_content = zip_ref.read(file)
                                        cbz_file_path = os.path.join(
                                            subfolder_name, os.path.basename(file)
                                        )
                                        cbz.writestr(cbz_file_path, file_content)
                print(
                    f"ZIP File Process completed : {chapter_name}.zip, {count} CBZ Generated, {len(os.listdir(cbz_file))} Total CBZ"
                )

            except Exception as e:
                print(f"Error reading ZIP File : {zip_path}\n{e}")

    print("Process Complete !")


if __name__ == "__main__":
    main()
