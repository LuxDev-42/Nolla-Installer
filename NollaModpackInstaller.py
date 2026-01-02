import json
import os
import shutil
import sys
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox

messagebox.showwarning("Aviso de atualização", "Certifique-se que Minecraft e seu devido launcher estejam fechados antes de prosseguir.\n\nCaso constrário, o Modpack pode não ser instalado corretamente.")

# Define the path where the executable is located
print("Definindo diretório de trabalho...")
if getattr(sys, 'frozen', False): 
    exe_path = os.path.dirname(sys.executable)
else:
    exe_path = os.path.dirname(os.path.abspath(__file__))

# Define the search string for the nolla folder
search_string = "nolla"

# Find the nolla folder with the highest version number
print("Verificando arquivos Nolla disponíveis...")
nolla_folders = [folder for folder in os.listdir(exe_path) if search_string.lower() in folder.lower() and len(folder.split()) == 2 and folder.split()[0].lower() == search_string.lower()]

if not nolla_folders:
    messagebox.showerror("Error", "Arquivo Nolla não encontrado.")
    sys.exit()
else:
    highest_version_folder = max(nolla_folders, key=lambda x: float(x.split()[-1]))
    nolla_path = os.path.join(exe_path, highest_version_folder)
    nolla_version = highest_version_folder.split()[-1]

# Find the Minecraft directory
print("Procurando .Minecraft...")
mc_path = os.path.join(os.getenv("APPDATA"), ".minecraft") #type: ignore

# Check if nolla_metadata.xml exists and parse it
print("Obtendo versão Nolla instalado...")
metadata_file = os.path.join(mc_path, "mods", "nolla_metadata.xml")
if os.path.exists(metadata_file):
    tree = ET.parse(metadata_file)
    root = tree.getroot()
    installed_version = root.find("version").text #type: ignore
else:
    installed_version = "0.00"

def update_profile():
    launcher_profiles_path = os.path.join(mc_path, 'launcher_profiles.json')
    data = json.load(f) #type: ignore
    # Check if the profile is already present
    if 'fabric-loader-1.20.1' in data["profiles"]:
        # The profile exists; update it
        print("Updating profile...")
        data["profiles"]["fabric-loader-1.20.1"]["name"] = "Nolla"
        data["profiles"]["fabric-loader-1.20.1"]["icon"] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACABAMAAAAxEHz4AAAAGFBMVEX/KkD/////pC5WIQC0cyCysrLDw8NHcEyKeIT6AAAACHRSTlP/////////AN6DvVkAAAJPSURBVGjezdnBkYUgDADQtEALtJAWfgvsfQ9rC7S/AiIIAYIC38we/g7mDVFEFNDFgCgqR00CgIiVABRiEQDVWAAA9AmjAWDEVACgWxgK5AfiHnTLFIA6BLfNEXQzA1CKDZDtO7AJrB3RBhQTINNRiLgL1EEMQLEAosmki2YXOIDqA858IQ5ABCA6cDCQXyGfv8UVEEITUCyAuFUcYO4mPG8HSuAAqhcAB5hcse1hBgISAgtQNloANWkdw8gJ2+VKXgQeoOpAyDt/+XQv/BQHExNQLCD8DOlmJFZraAKKD4SmvAMJoPmAYgDJzREAjELQw3koELWhyw4nwkShBhbwp0qzggHyRwWYDos43GAkLyQPyLuQA3Fjkn4Av2QNHYBgA2m67wFVQw8guECc74rZ1EPAdqBUAtQAdH9+NFdXhE8BOl/aQf1xcb2d9AoApTSCB/Z/1gD6OG3HyYvnFb0I2J9q0nb+UkJSwFTA5tmBYx2UDkC9EvCdlzaWA+dJ/B6gCUCuBbS/gJUKVgA+FgFQB/aCWh8KbgO6WYMHyC8FehmA6TGzgUj4BACmAlAD5AEAa5XWC7RqiCq4LkdLK9XbALAAaK7WbwCNGo75LHnhLb6xPAHoGs7ZBPJ3s+EAKYT5jHg/HQXoBuAfKuQ0OAaoCfGUTs3DgwGoA3oeUBGuj7X8UTQKoAVM84mPduOBZMWXADAPoAUsn0M9HCh8mC4NIz0BoD/OB+Dm1/0egFy4uVet2zscncD3d3nesNP1gt2+N+x4vmDX9xU730t3//8BP73sL+DuoDsAAAAASUVORK5CYII="

        # Write the updated data back to the JSON file
        with open(launcher_profiles_path, 'w') as f:
            json.dump(data, f, indent=4)

        print("Profile updated successfully!")
    else:
        # The profile doesn't exist; proceed to check for the Fabric version
        print("Checking for Fabric version...")
        
        # Construct the path to the Fabric Modloader
        fabric_version_path = os.path.join(mc_path, 'versions', 'fabric-loader-0.14.23-1.20.1', 'fabric-loader-0.14.23-1.20.1.jar')
        
        # Check if the Fabric version jar file exists
        if os.path.exists(fabric_version_path):
            # The Fabric version is present; create the profile
            print("Creating profile...")
            data["profiles"]["fabric-loader-1.20.1"] = {
                "lastUsed": "2023-10-23T17:08:32-0400",
                "lastVersionId": "fabric-loader-0.14.23-1.20.1",
                "created": "2023-10-23T17:08:32-0400",
                "name": "fabric-loader-1.20.1",
                "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACABAMAAAAxEHz4AAAAGFBMVEX/KkD/////pC5WIQC0cyCysrLDw8NHcEyKeIT6AAAACHRSTlP/////////AN6DvVkAAAJPSURBVGjezdnBkYUgDADQtEALtJAWfgvsfQ9rC7S/AiIIAYIC38we/g7mDVFEFNDFgCgqR00CgIiVABRiEQDVWAAA9AmjAWDEVACgWxgK5AfiHnTLFIA6BLfNEXQzA1CKDZDtO7AJrB3RBhQTINNRiLgL1EEMQLEAosmki2YXOIDqA858IQ5ABCA6cDCQXyGfv8UVEEITUCyAuFUcYO4mPG8HSuAAqhcAB5hcse1hBgISAgtQNloANWkdw8gJ2+VKXgQeoOpAyDt/+XQv/BQHExNQLCD8DOlmJFZraAKKD4SmvAMJoPmAYgDJzREAjELQw3koELWhyw4nwkShBhbwp0qzggHyRwWYDos43GAkLyQPyLuQA3Fjkn4Av2QNHYBgA2m67wFVQw8guECc74rZ1EPAdqBUAtQAdH9+NFdXhE8BOl/aQf1xcb2d9AoApTSCB/Z/1gD6OG3HyYvnFb0I2J9q0nb+UkJSwFTA5tmBYx2UDkC9EvCdlzaWA+dJ/B6gCUCuBbS/gJUKVgA+FgFQB/aCWh8KbgO6WYMHyC8FehmA6TGzgUj4BACmAlAD5AEAa5XWC7RqiCq4LkdLK9XbALAAaK7WbwCNGo75LHnhLb6xPAHoGs7ZBPJ3s+EAKYT5jHg/HQXoBuAfKuQ0OAaoCfGUTs3DgwGoA3oeUBGuj7X8UTQKoAVM84mPduOBZMWXADAPoAUsn0M9HCh8mC4NIz0BoD/OB+Dm1/0egFy4uVet2zscncD3d3nesNP1gt2+N+x4vmDX9xU730t3//8BP73sL+DuoDsAAAAASUVORK5CYII="
            }

            # Write the updated data back to the JSON file
            with open(launcher_profiles_path, 'w') as f:
                json.dump(data, f, indent=4)

            print("Profile created successfully!")
        else:
            # The Fabric version is not found; show an error notification and exit
            print("Fabric version not found.")
            messagebox.showerror("Update Error", "The Fabric Modloader version 1.20.1 was not found. Please make sure you have the correct version of Minecraft (1.20.1) installed. If the issue persists, consider manual installation.")

# Removing old files in .minecraft for stability function
print("Deletando arquivos antigos...")
# Old folders removal
for folder_name in ["config", "mods", "essential"]:
    folder_path = os.path.join(mc_path, folder_name)
    if os.path.exists(folder_path):
        print(f"Removendo a pasta {folder_name}")
        shutil.rmtree(folder_path)
# Old files removal (config and info)
file_names = ["options.amecsapi.txt", "options.txt"]
for name in file_names:
    file_path = os.path.join(mc_path, name)
    if os.path.exists(file_path):
        print(f"Removendo o arquivo {name}")
        os.remove(file_path)
    else:
        print(f"No files found with name {name} at {file_path}")

metadata_file = os.path.join(mc_path, "mods", "nolla_metadata.xml")

if os.path.exists(metadata_file):
    tree = ET.parse(metadata_file)
    root = tree.getroot()
    installed_version = root.find("version").text #type: ignore
else:
    installed_version = "0.00"

    # Copy the contents of the nolla folder to the Minecraft directory

    for item in os.listdir(nolla_path):
        s = os.path.join(nolla_path, item)
        d = os.path.join(mc_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

update_profile()

print("Enviando um 'vai se fuder' pro thales")
messagebox.showinfo("Instalação finalizada", "Vai se fuder, Thales)")
