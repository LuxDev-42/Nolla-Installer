# Nolla installer - Version 0.10
# This version aim's install and update the installed Nolla Version.
# Status = complete

import os
import sys
import shutil
from tkinter import messagebox

# Define the path where the executable is located
if getattr(sys, 'frozen', False):
    exe_path = os.path.dirname(sys.executable)
else:
    exe_path = os.path.dirname(os.path.abspath(__file__))

# Define the search string for the nolla folder
search_string = "nolla"

# Find the nolla folder with the highest version number
nolla_folders = [folder for folder in os.listdir(exe_path) if search_string.lower() in folder.lower() and len(folder.split()) == 2 and folder.split()[0].lower() == search_string.lower()]

if not nolla_folders:
    messagebox.showerror("Error", "Nolla file not found.")
else:
    highest_version_folder = max(nolla_folders, key=lambda x: float(x.split()[-1]))
    nolla_path = os.path.join(exe_path, highest_version_folder)

    # Find the Minecraft directory
    mc_path = os.path.join(os.getenv("APPDATA"), ".minecraft") #type: ignore

    # Delete the config, mods and essential folders in the Minecraft directory
    for folder_name in ["config", "mods", "essential"]:
        folder_path = os.path.join(mc_path, folder_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    # Copy the contents of the nolla folder to the Minecraft directory
    for item in os.listdir(nolla_path):
        s = os.path.join(nolla_path, item)
        d = os.path.join(mc_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

    # Show a pop-up window indicating that the installation is complete
    messagebox.showinfo("Installation Complete", "The Nolla Modpack has been successfully installed!")