'''
####################################################
#   Modular Filesystem Auto Benchmarking for HPC   #
#                   by Nico Stöhr                  #
####################################################
'''

# IMPORTS 

# os
from os import listdir, remove
from os.path import isfile

# json
from json import dumps, load


def read_file(file_path: str) -> list[str]:
    temp_data: list[str] = []
    with open(file_path, "r") as temp_file:
        temp_data = temp_file.readlines()
    return temp_data


class save:
    def __init__(self, base_path: str) -> None:
        self.base_path: str = base_path


    # SAVE THE ENTIRE PROGRAM STATE INTO A SINGLE FILE
    def saveState(self, file_name: str) -> int:
        # check if file exists already
        if isfile(f"{self.base_path}/saves/{file_name}.mfabstate"):
            print(f"{file_name}.mfabstate already exists.\nPlease delete this file or choose a different file name and try again.")
            return -1
        
        # prepare save state
        app_profile_list: list[str] = listdir(f"{self.base_path}/app_profiles")
        filesystem_profile_list: list[str] = listdir(f"{self.base_path}/filesystem_profiles")
        app_profile_list.remove("app_base")
        filesystem_profile_list.remove("filesystem_base")

        save_dict: dict[str, list[str]] = dict()
        
        # read in profiles
        for profile_file in app_profile_list:
            save_dict[f"app_profiles/{profile_file}"] = read_file(f"{self.base_path}/app_profiles/{profile_file}")
        for profile_file in filesystem_profile_list:
            save_dict[f"filesystem_profiles/{profile_file}"] = read_file(f"{self.base_path}/filesystem_profiles/{profile_file}")

        # read in run config
        save_dict["run_config.json"] = read_file(f"{self.base_path}/run_config.json")

        # read in graphs config
        save_dict["graphs_config.json"] = read_file(f"{self.base_path}/graphs_config.json")

        # save state
        with open(f"{self.base_path}/saves/{file_name}.mfabstate", "w") as save_file:
            save_file.writelines(dumps(save_dict))
        
        return 0
        
            
    # LOAD THE ENTIRE PROGRAM STATE FROM A SINGLE FILE
    def loadState(self, file_name: str) -> int:
        valid_input: bool = False

        confirmation_input: str = ""
        
        # ask for confirmation
        print("Overwrite current program state?\nDoing a backup is strongly recommended, use > python3 run.py savestate *filename*")
        while not valid_input:
            confirmation_input = input("This will overwrite all program settings and existing profiles.\nProceed? (Y/N): ")
            confirmation_input = confirmation_input.strip().lower()
            if confirmation_input in ["y", "n", "yes", "no"]: valid_input = True
            else: print("Incorrect input. Try again.")

        # exit loadstate
        if confirmation_input in ["n", "no"]: 
            print("Loadstate aborted.")
            return 0
        
        # check for file errors
        if not file_name.endswith(".mfabstate"): file_name += ".mfabstate"

        if "/" in file_name:
            if not isfile(file_name):
                print("File does not exist.")
                return -1
        else:
            file_name = f"{self.base_path}/saves/{file_name}"
            if not isfile(file_name):
                print("File does not exist.")
                return -1

        # start loadstate
        load_dict: dict[str, list[str]] = dict()
        with open(file_name, "r") as load_file:
            load_dict = load(load_file)

        # load files
        for file_path, file_data in load_dict.items():
            if isfile(file_path): remove(file_path)
            
            with open(file_path, "w") as new_file:
                new_file.writelines(file_data)

        return 0
