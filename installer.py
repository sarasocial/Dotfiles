#!/usr/bin/env python

import os
import sys
import subprocess
import questionary
from rich.console import Console
from rich.text import Text

console = Console()

def clear():
    os.system("clear")

def title():
    clear()
    console.print(Text("""
┌───────────────────────────────────────────┐
│                                           │
│    ██╗     ██╗   ██╗███╗   ██╗ █████╗     │
│    ██║     ██║   ██║████╗  ██║██╔══██╗    │
│    ██║     ██║   ██║██╔██╗ ██║███████║    │
│    ██║     ██║   ██║██║╚██╗██║██╔══██║    │
│    ███████╗╚██████╔╝██║ ╚████║██║  ██║    │
│    ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    │
│                                           │
└───────────────────────────────────────────┘
""", style="bold red"))

# Copy configuration file
def copy_config(src, dest):
    with open(src, "r") as source:
        with open(dest, "w") as destination:
            destination.write(source.read())

# Stow files
def stow_files():
    title()
    console.print("Stowing dotfiles...", style="bold green")
    subprocess.run(["stow", "--adopt", "dots"], check=True)

# Install packages
def install_packages():
    title()
    package_choice = questionary.select(
        "Install needed packages?",
        choices=["Yes", "No"]
    ).ask()

    if package_choice == "Yes":
        subprocess.run(["bash", "pacman.sh"], check=True)
    else:
        console.print("Skipping package installation.", style="bold yellow")

# Install tpm plugins
def install_tpm_plugins():
    title()
    tpm_choice = questionary.select(
        "Install TPM plugins?",
        choices=["Yes", "No"]
    ).ask()

    if tpm_choice == "Yes":
        tpm_dir = os.path.expanduser("~/.tmux/plugins")
        subprocess.run(["rm", "-rf", tpm_dir], check=True)
        os.makedirs(tpm_dir, exist_ok=True)
        subprocess.run(["git", "clone", "https://github.com/tmux-plugins/tpm", os.path.join(tpm_dir, "tpm")], check=True)
        script_path = os.path.join(tpm_dir, "tpm/scripts/install_plugins.sh")
        if os.path.isfile(script_path):
            subprocess.run([script_path], check=True)
        else:
            console.print(f"Error: El script no existe en la ruta {script_path}", style="bold red")
    else:
        console.print("Skipping TPM plugins installation.", style="bold yellow")

# Homescreen prompt
def home():
    title()
    proceed = questionary.select(
        choices=["Install Dotfiles", "Help", "Exit"]
    ).ask()
    return proceed


# Installation prompt sequence
def install_options():
    title()
    options={}
    options["Keyboard"] = questionary.select(
         # Select an option from /options/keyboard
        "Select your keyboard layout",
        choices=["US", "LATAM"]
    ).ask()
    options["Graphics"] = questionary.select(
         # Select an option from /options/graphics
        "Select your graphics drivers", 
        choices=["NVIDIA", "Open Source (AMD/Intel/Nouveau)"]
    ).ask()
    options["Hyprland"] = questionary.select(
        # Select either hyprland or hyprland-git packages
        "Select your Hyprland version",
        choices=["Hyprland", "Hyprland Git"]
    ).ask()
    console.print("You have selected the following options:")
    for option, choice in thisdict.items():
        console.print("  - ", option, ": ",  choice)
    
    options["cancel"] = questionary.select(
        # Select either hyprland or hyprland-git packages
        "Do you want to proceed to installation with these selections?",
        choices=["Proceed", "Cancel"]
    ).ask()
    return options


# Run installation with chosen options
def install():
    options = install_options()

    # Cancel if requested
    if options["proceed"] == False:
        return False
    
    # Copy keyboard layout
    if options["keyboard"] == "US":
        copy_config(f"./options/us.conf", "./dots/.config/hypr/source/keyboard.conf")
    else:
        copy_config(f"./options/latam.conf", "./dots/.config/hypr/source/keyboard.conf")

    # Copy graphics
    if options["graphics"] == "NVIDIA":
        copy_config("./options/nvidia.conf", "./dots/.config/hypr/source/nvidia.conf")
    else:
        copy_config("./options/nvidia-dummy.conf", "./dots/.config/hypr/source/nvidia.conf")

    stow_files()
    install_packages()
    install_tpm_plugins()

    subprocess.run(["matugen", "image", "./example_wallpaper.jpg"], check=True, stdout=subprocess.DEVNULL)

    clear()


def main():
    title()
    installed = False

    # Main options loop
    while installed == False:
        home_choice = home() # Get initial menu choice
        if home_choice == "Install Dotfiles":
            success = install() # attempt installation
            if success == True:
                installed = True # confirm installation success
        elif home_choice == "Help":
            # Show help menu
        else:
            sys.exit()

    # Post-installation

    # Set wallpaper and theme
    console.print("""
┌────────────────────────────┐
│                            │
│     ░█▀▄░█▀█░█▀█░█▀▀░█     │
│     ░█░█░█░█░█░█░█▀▀░▀     │
│     ░▀▀░░▀▀▀░▀░▀░▀▀▀░▀     │
│                            │
└────────────────────────────┘
""", style="bold green")

if __name__ == "__main__":
    main()