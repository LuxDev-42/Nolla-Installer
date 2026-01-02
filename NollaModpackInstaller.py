# Nolla installer - Version 0.55
# - This version have little final modifications before personal distribuition, like:
#       > Now it locates the XML in the mods folder
# Status = finished (stable)

import datetime
import fnmatch
import json
import os
import shutil
import subprocess
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
mc_path = os.path.join(os.getenv("APPDATA"), ".minecraft") # type: ignore

# Check if nolla_metadata.xml exists and parse it
print("Obtendo versão Nolla instalado...")
metadata_file = os.path.join(mc_path, "mods", "nolla_metadata.xml")
if os.path.exists(metadata_file):
    tree = ET.parse(metadata_file)
    root = tree.getroot()
    installed_version = root.find("version").text #type: ignore
else:
    installed_version = "0.00"

#Functions Section

# update the JSON file function
def update_profile():
        launcher_profiles_path = os.path.join(mc_path, 'launcher_profiles.json')
        
        print("Atualizando perfil...")
        
        try:
            # Open the JSON file for reading
            with open(launcher_profiles_path, 'r') as f:
                data = json.load(f)
            
            # Update the data in memory
            data["profiles"]["fabric-loader-1.19.2"]["name"] = "Nolla"
            data["profiles"]["fabric-loader-1.19.2"]["icon"] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACABAMAAAAxEHz4AAAAGFBMVEX/KkD/////pC5WIQC0cyCysrLDw8NHcEyKeIT6AAAACHRSTlP/////////AN6DvVkAAAJPSURBVGjezdnBkYUgDADQtEALtJAWfgvsfQ9rC7S/AiIIAYIC38we/g7mDVFEFNDFgCgqR00CgIiVABRiEQDVWAAA9AmjAWDEVACgWxgK5AfiHnTLFIA6BLfNEXQzA1CKDZDtO7AJrB3RBhQTINNRiLgL1EEMQLEAosmki2YXOIDqA858IQ5ABCA6cDCQXyGfv8UVEEITUCyAuFUcYO4mPG8HSuAAqhcAB5hcse1hBgISAgtQNloANWkdw8gJ2+VKXgQeoOpAyDt/+XQv/BQHExNQLCD8DOlmJFZraAKKD4SmvAMJoPmAYgDJzREAjELQw3koELWhyw4nwkShBhbwp0qzggHyRwWYDos43GAkLyQPyLuQA3Fjkn4Av2QNHYBgA2m67wFVQw8guECc74rZ1EPAdqBUAtQAdH9+NFdXhE8BOl/aQf1xcb2d9AoApTSCB/Z/1gD6OG3HyYvnFb0I2J9q0nb+UkJSwFTA5tmBYx2UDkC9EvCdlzaWA+dJ/B6gCUCuBbS/gJUKVgA+FgFQB/aCWh8KbgO6WYMHyC8FehmA6TGzgUj4BACmAlAD5AEAa5XWC7RqiCq4LkdLK9XbALAAaK7WbwCNGo75LHnhLb6xPAHoGs7ZBPJ3s+EAKYT5jHg/HQXoBuAfKuQ0OAaoCfGUTs3DgwGoA3oeUBGuj7X8UTQKoAVM84mPduOBZMWXADAPoAUsn0M9HCh8mC4NIz0BoD/OB+Dm1/0egFy4uVet2zscncD3d3nesNP1gt2+N+x4vmDX9xU730t3//8BP73sL+DuoDsAAAAASUVORK5CYII="
            
            # Write the updated data back to the JSON file
            with open(launcher_profiles_path, 'w') as f:
                json.dump(data, f, indent=4)
                
            print("Perfil atualizado com sucesso!")
            messagebox.showinfo("Perfil atualizado com sucesso!", "Você verá um perfil chamado Nolla nas versões de minecraft ")
            
        except Exception as e:
            print("Error updating profile:", e)

# install nolla function
def install_nolla():
    # Copy the contents of the nolla folder to the Minecraft directory (first remove info files)
    file_path = os.path.join(mc_path, "nolla_metadata.xml")
    if os.path.exists(file_path):
        print(f"Removendo nolla_metadata.xml")
        os.remove(file_path)
    
    modlist_path = os.path.join(mc_path, f".NollaModList_v{installed_version}.txt")
    if os.path.exists(modlist_path):
        print(f"Removendo .NollaModList_v{installed_version}.txt")
        os.remove(modlist_path)
    
    for item in os.listdir(nolla_path):
        s = os.path.join(nolla_path, item)
        d = os.path.join(mc_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None, dirs_exist_ok=True)
        else:
            if not os.path.exists(d):
                shutil.copy2(s, d)
    print(f"Versão atualizada: {nolla_version}")
    update_profile()
    
    # Show a pop-up window indicating that the installation is complete
    messagebox.showinfo("atualização completa", f"Nolla {nolla_version} instalado com sucesso. Pode abrir o Launcher!")

# Removing old files in .minecraft for stability function
def remove_old_folders():
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

# Backup Mods folder Function
def backup_mods(mc_path):
        # create a new directory to store the backup
        backup_dir = os.path.join(os.path.expanduser("~"), "Documents", "mod_backups")
        os.makedirs(backup_dir, exist_ok=True)

        # create a timestamped folder for this backup
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y_%H-%Mh")
        backup_folder = os.path.join(backup_dir, f"mods_backup_{timestamp}")
        os.makedirs(backup_folder)

        # copy the entire mods folder to the backup folder
        shutil.copytree(os.path.join(mc_path, "mods"), os.path.join(backup_folder, "mods"))

        # show a message box confirming the backup was successful
        messagebox.showinfo("Backup feito", f"Seus mods foram salvos em {backup_folder}")

# Nolla installer
def nolla_process():
    #Nolla installer here

    # Search for the fabric modloader 
    modloader_pattern = "*fabric*loader*1.19.2*.jar"
    modloader_path = None
    for root, dirs, files in os.walk(os.path.join(mc_path, "versions")):
        for file in files:
            if fnmatch.fnmatch(file, modloader_pattern):
                modloader_path = os.path.join(root, file)
                break
        if modloader_path:
            break
    
    # If modloader is missing, popen and wait the fabric installer 
    if not modloader_path:
        messagebox.showinfo("Fabric Modloader Ausente", "A versão correta do Modloader Fabric é requerido para o funcionamento do Modpack.\n\nLembre de instalar a versão Minecraft 1.19.2.\n\nA versão do modloader pode ser a mais recente.")

        # Search for the Fabric Installer
        print("Procurando instalador Fabric...")
        installer_pattern = "*fabric*installer*.*"
        fabric_installer_path = None
        for file in os.listdir(exe_path):
            if fnmatch.fnmatch(file, installer_pattern):
                fabric_installer_path = os.path.join(exe_path, file)
                break

        if not fabric_installer_path:
            messagebox.showerror("Erro de instalação", "O executável de instalação do Fabric não pôde ser encontrado.")
            sys.exit()
        
        # Open the fabric installer (It is intended for future versions to make this section AUTOMATED without user input)
        print("\n\n\nAguardando por atualização...\n\nlembre-se de que a versão Minecraft correta é a 1.19.2.\n\nA versão do modloader pode ser a mais recente (recomendado)")
        subprocess.Popen(fabric_installer_path, cwd=mc_path).wait()

        # Check if the correct fabric version was installed
        print("Checando versão...")
        modloader_pattern = "*fabric*loader*1.19.2*.jar"
        modloader_path = None
        for root, _, files in os.walk(os.path.join(mc_path, "versions")):
            for file in files:
                if fnmatch.fnmatch(file, modloader_pattern):
                    modloader_path = os.path.join(root, file)
                    break
            if modloader_path:
                break
        
        # If the correct modloader is installed, proceed instalation
        if modloader_path:
            print("Fabric modloader correto instalado")
            remove_old_folders()
            install_nolla()
        else:
            messagebox.showerror("Erro de atualização", "O Modloader Fabric não pôde ser encontrado.\n\nVerifique se a versão correta do Minecraft (1.19.2) foi instalado.\n\n Caso o erro persista, instale manualmente.")
            sys.exit()
        # End of the fabric instalation process (to be AUTOMATED) 
    else:
        # Check if the installed version matches the highest version folder
        print("Comparando versões...")
        print(f"nolla instalado: {installed_version}")
        print(f"nolla disponível: {nolla_version}")
        if installed_version == highest_version_folder.split()[-1]: # Nolla is updated
            print("Nolla atualizado")
            messagebox.showinfo("Nolla atualizado", "A versão mais recente do Modpack Nolla está instalado!")
            sys.exit()
        else:
            print("Nova atualização nolla encontrada!")
            if not os.path.isfile(os.path.join(mc_path, "nolla_metadata.xml")): #Nolla is not installed (backup option was already given at this point)
                remove_old_folders()
                install_nolla()
            elif installed_version == "0.00":
                print("Nolla não está instalado")
                print("Installando Nolla")
                install_nolla()
            elif installed_version > highest_version_folder.split()[-1]:
                messagebox.showinfo("Nolla instalado", "A versão instalada é mais recente do que a versão disponível do Modpack Nolla.")
                sys.exit()
            else:
                # Ask installation mode
                update_nolla_gui()

# GUI for the Nolla updating function
def update_nolla_gui():
    root = tk.Tk()
    root.title("Modo de atualização")
    root.geometry("600x150")

    label = tk.Label(root, text="Uma nova atualização Nolla foi encontrada.\nDeseja fazer uma atualização limpa ou uma atualização rápida?")
    label.pack(pady=5)

    warning = tk.Label(root, text="Uma atualização rápida mantém os dados porém é sujeito a erros.", fg="red")
    warning.pack()

    frame = tk.Frame(root)
    frame.pack(pady=5)

    def clear_install():
        root.destroy()
        remove_old_folders()
        install_nolla()

    clear_install_button = tk.Button(frame, text="Atualização limpa", command=clear_install)
    clear_install_button.pack(side=tk.LEFT, padx=10, pady=10)

    def fast_install():
        root.destroy()
        install_nolla()

    fast_install_button = tk.Button(frame, text="Atualização rápida", command=fast_install)
    fast_install_button.pack(side=tk.LEFT, padx=10, pady=10)

    root.eval('tk::PlaceWindow . center')

    root.mainloop()

# check if the "mods" folder exists in the Minecraft directory
if os.path.isdir(os.path.join(mc_path, "mods")):
    if os.path.isfile(os.path.join(mc_path, "nolla_metadata.xml")):
        print("Nolla XML detectado.")
        nolla_process()
    else:
        root = tk.Tk()
        root.title("Pasta de mods detectado")
        root.geometry("500x150")

        label = tk.Label(root, text="Mods foram detectados na sua pasta .minecraft.")
        label.pack(pady=5)

        warning = tk.Label(root, text="Se prosseguir, o instalador apaga os mods presentes em prol de estabilidade", fg="blue")
        warning.pack()

        warning = tk.Label(root, text="Recomenda-se que um backup da sua pasta de mods seja feito antes de prosseguir", fg="red")
        warning.pack()

        frame = tk.Frame(root)
        frame.pack(pady=5)

        def proceed():
            root.destroy()
            nolla_process()

        proceed_button = tk.Button(frame, text="Prosseguir", command=proceed)
        proceed_button.pack(side=tk.LEFT, padx=10, pady=10)

        def backup():
            root.destroy()
            backup_mods(mc_path)
            nolla_process()

        Backup_button = tk.Button(frame, text="Fazer Backup", command=backup) # type: ignore
        Backup_button.pack(side=tk.LEFT, padx=10, pady=10)

        root.eval('tk::PlaceWindow . center')

        root.mainloop()
else:
    nolla_process()