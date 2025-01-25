#!/bin/bash

# Read from dependencies source file
IFS=$'\n' read -d '' -r -a dependencies < ./resources/installer-dependencies.txt

# Format dependencies into array; keys are package names, values are package types
# ex: the line 'arch git' indicates package 'git' from official arch repositories

# Isolate missing packages
missingPackages=()
for package in "${dependencies[@]}"; do
    currentPackage=($package)
    packageType="${currentPackage[0]}"
    packageName="${currentPackage[1]}"
    # Supported types: 'arch', 'aur', 'makepkg', 'pip'
    if [[ "$type" == "pip" ]]; then
        if [[ ! $(pacman -Q "python" &>/dev/null) ]]; then
            missingPackages+="${currentPackage[@]}\n" # python not installed
        else
            python -c "import $packageName" && echo $? > result
            [ ! $result ] && missingPackages+="${currentPackage[@]}\n" # python package not found
        fi
    elif [[ ! $(pacman -Q "$packageName" &>/dev/null) ]]; then
        missingPackages+="${currentPackage[@]}\n" # package not found with pacman
    fi
done
missingPackages+=("@@" "EOF")

# Prompt user to install missing dependencies
if [[ ${#missingPackages[@]} > 0 ]]; then

    # Install dependencies
    needSudo=1
    IFS=$'\n' read -d '' -r -a dependencies < ./resources/installer-dependencies
    while "${missingPackages[@]}"; do
        if [[ "$1" == "@@" ]]; then
            shift && packageType="$1" && packageName="$2" && shift 2
            case $packageType in
                arch|pacman)
                    [ $needSudo ] && sudo pacman -S "$packageName" \
                        || pacman -S "$packages" echo $? > result \
                        && [ ! $result ] && needSudo=0 \
                        && sudo pacman -S "$packageName"
                        shift
                    ;;
                aur|paru)
                    paru -S "$packageName"
                    ;;
                makepkg)
                    source="$1"
                    args=()
                    while ! "$1" == "@@"; do 
                        args+="$1" && shift
                    done
                    rm -rf "$packageName"
                    git clone "$source" "$packageName" && cd "$packageName"
                    makepkg "$args" && cd .. && rm -rf "$packageName"
                    ;;
                pip)
                    python -m pip install "$packageName" && echo $? > result
                    [ ! $result ] || sudo pacman -S "$packageName"
                    shift
                    ;;
                EOF)
                    break
                    ;;
                *)
                    printf "Unknown package type $packageType"
                    exit
                    ;;
            esac
        else
            break
        fi
    done
fi

# Run installer
python ./installer.py