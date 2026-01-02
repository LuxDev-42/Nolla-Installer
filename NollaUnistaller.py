import json
import os
import shutil
import sys
import tkinter as tk
from tkinter import messagebox

def remove_nolla():
    mc_path = os.path.join(os.getenv("APPDATA"), ".minecraft")

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
            if "Nolla" in data["profiles"]:
                print("Removing launcher profile for Nolla")
                del data["profiles"]["Nolla"]
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

    # Delete Nolla version folder
    version_folder_path = os.path.join(mc_path, "versions", "fabric-loader-0.14.19-1.19.2")
    if os.path.exists(version_folder_path):
        print(f"Removing version folder: {version_folder_path}")
        shutil.rmtree(version_folder_path)

    messagebox.showinfo("Nolla desinstalado", "Nolla desinstalado com sucesso")

root = tk.Tk()
root.title("Desinstalação Nolla")
root.geometry("300x100")

label = tk.Label(root, text="Tem certeza que deseja desinstalar o Nolla?")
label.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

def unistall_nolla():
    remove_nolla()
    sys.exit()

clear_install_button = tk.Button(frame, text="Desinstalar", command=unistall_nolla)
clear_install_button.pack(side=tk.LEFT, padx=10, pady=10)

fast_install_button = tk.Button(frame, text="Cancelar", command=sys.exit)
fast_install_button.pack(side=tk.LEFT, padx=10, pady=10)

root.eval('tk::PlaceWindow . center')

root.mainloop()
