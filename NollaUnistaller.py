# - Nolla unistaller: Made from (dd/mm/yy) 16/05/23 to 18/05/23. I just deletes all the files realated to the modpack.
# - First, it will be asked if the user really wants to unistall. After confirmation, options to doing a backup are presented, otherwise the program 
# will close

import datetime
import json
import os
import shutil
import sys
import tkinter as tk
from tkinter import messagebox

#Find the Minecraft directory
mc_path = os.path.join(os.getenv("APPDATA"), ".minecraft") #type: ignore

# > Functions section

# Complete removal of the files and closes the program
def full_delete():
    nolla_folders = ["config", "essential", "mods"]
    nolla_files = ["NollaLogo128x128-min.png", ".NollaModList_v0.80.txt", "options.amecsapi.txt", "options.txt"]

    # Delete Nolla folders
    for folder in nolla_folders:
        folder_path = os.path.join(mc_path, folder)
        if os.path.exists(folder_path):
            print(f"Removing folder: {folder_path}")
            shutil.rmtree(folder_path)

    # Delete Nolla files
    for file in nolla_files:
        file_path = os.path.join(mc_path, file)
        if os.path.exists(file_path):
            print(f"Removing file: {file_path}")
            os.remove(file_path)

    # Delete launcher profile for Nolla
    launcher_profiles_path = os.path.join(mc_path, "launcher_profiles.json")
    if os.path.exists(launcher_profiles_path):
        with open(launcher_profiles_path, "r+") as f:
            data = json.load(f)
            if "profiles" in data:
                profiles = data["profiles"]
                if "*fabric-loader-1.20.1*" in profiles:
                    print("Removing launcher profile for Nolla")
                    del profiles["fabric-loader-1.20.1"]
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()

    # Delete Nolla version folder
    version_folder_path = os.path.join(mc_path, "versions", "fabric-loader-*-1.20.1")
    if os.path.exists(version_folder_path):
        print(f"Removing version folder: {version_folder_path}")
        shutil.rmtree(version_folder_path)

    messagebox.showinfo("Nolla desinstalado", "Nolla desinstalado com sucesso")

    sys.exit()

# Backup Function
def backup_exec():
    # create a new directory to store the backup
    backup_dir = os.path.join(os.path.expanduser("~"), "Documents", "Nolla_Backups")
    os.makedirs(backup_dir, exist_ok=True)

    # create a timestamped folder for this backup
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%Mh")
    backup_folder = os.path.join(backup_dir, f"Nolla_backup_{timestamp}")

    # Remove existing backup folder if it exists
    if os.path.exists(backup_folder):
        shutil.rmtree(backup_folder)

    os.makedirs(backup_folder)

    # copy files to the backup folder
    files_to_copy = ["options.txt", "options.amecsapi.txt"]
    folders_to_copy = ["config", "essential"]
    backup_successful = False  # Flag to track if any backup was made

    for file in files_to_copy:
        source_path = os.path.join(mc_path, file)
        destination_path = os.path.join(backup_folder, file)
        if os.path.exists(source_path):
            shutil.copy2(source_path, destination_path)
            backup_successful = True

    for folder in folders_to_copy:
        source_path = os.path.join(mc_path, folder)
        destination_path = os.path.join(backup_folder, folder)
        if os.path.exists(source_path):
            shutil.copytree(source_path, destination_path)
            backup_successful = True

    # Show messagebox if any backup was made
    if backup_successful:
        messagebox.showinfo("Backup feito", f"Seus arquivos foram salvos em {backup_folder}")
    else:
        messagebox.showinfo("Warning", "No files or folders to backup.")
        sys.exit()

# Gui for offering a backup
def backup_optionGUI():
    root = tk.Tk()
    root.title("Fazer Backup?")
    root.geometry("350x100")

    label = tk.Label(root, text="Gostaria de fazer um backup para manter suas configurações")
    label.pack(pady=8)

    frame = tk.Frame(root)
    frame.pack(pady=8)

    def do_backup():
        root.destroy()
        backup_exec()
        full_delete()
        sys.exit()

    clear_install_button = tk.Button(frame, text="Fazer backup e desinstalar", command=do_backup)
    clear_install_button.pack(side=tk.LEFT, padx=10, pady=10)

    fast_install_button = tk.Button(frame, text="Desinstalar completamente", command=full_delete)
    fast_install_button.pack(side=tk.LEFT, padx=10, pady=10)

    root.eval('tk::PlaceWindow . center')

    root.mainloop()

# First Gui for unistalling

root = tk.Tk()
root.title("Desinstalação Nolla")
root.geometry("300x100")

label = tk.Label(root, text="Tem certeza que deseja desinstalar o Nolla?")
label.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

# The function executed in the first GUI to start everything.
def unistall_nolla():
    root.destroy()
    backup_optionGUI()

clear_install_button = tk.Button(frame, text="Desinstalar", command=unistall_nolla)
clear_install_button.pack(side=tk.LEFT, padx=10, pady=10)

fast_install_button = tk.Button(frame, text="Cancelar", command=sys.exit)
fast_install_button.pack(side=tk.LEFT, padx=10, pady=10)

root.eval('tk::PlaceWindow . center')

root.mainloop()