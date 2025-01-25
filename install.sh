#!/bin/bash

# install the shit it needs lol
cd ~/
sudo pacman -S base-devel git
git clone https://aur.archlinux.org/paru.git paru
cd paru && makepkg -si && cd ~/ && sudo rm -rf paru
sudo pacman -S stow python python-pip
python -m pip install python-questionary
python -m pip install python-rich

# Run installer
python ./installer.py