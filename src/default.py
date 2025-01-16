'''
####################################################
#   Modular Filesystem Auto Benchmarking for HPC   #
#                   by Nico Stöhr                  #
####################################################
'''

# IMPORTS 

# os
from os import remove
from os.path import isfile

# shutil
from shutil import copyfile


DEFAULT_GRAPH_CONFIG: str = "/src/defaults/default_graphs_config.json"

DEFAULT_CONFIG: str = "/src/defaults/default_run_config.json"

class Restore:
    def __init__(self, base_path: str) -> None:
        self.base_path: str = base_path

    def restoreRunConfig(self) -> int:
        if isfile(f"{self.base_path}/run_config.json"):
            user_input: str = ""
            valid_input: bool = False
            while not valid_input:
                print("run_config.json already exists.")
                user_input = input("Do you want to restore the default config? (y/n): ")
                user_input = user_input.strip().lower()
                if user_input in ["y", "yes", "n", "no"]: valid_input = True
            if user_input in ["y", "yes"]:
                remove(f"{self.base_path}/run_config.json")
                copyfile(self.base_path+DEFAULT_CONFIG, f"{self.base_path}/run_config.json")
                return 0
            elif user_input in ["n", "no"]:
                return 0
            else: return -1
        else:
            copyfile(self.base_path+DEFAULT_CONFIG, f"{self.base_path}/run_config.json")
            return 0

    def restoreGraphConfig(self) -> int:
        if isfile(f"{self.base_path}/graphs_config.json"):
            user_input: str = ""
            valid_input: bool = False
            while not valid_input:
                print("graphs_config.json already exists.")
                user_input = input("Do you want to restore the default config? (y/n): ")
                user_input = user_input.strip().lower()
                if user_input in ["y", "yes", "n", "no"]: valid_input = True
            if user_input in ["y", "yes"]:
                remove(f"{self.base_path}/graphs_config.json")
                copyfile(self.base_path+DEFAULT_GRAPH_CONFIG, f"{self.base_path}/graphs_config.json")
                return 0
            elif user_input in ["n", "no"]:
                return 0
            else: return -1
        else:
            copyfile(self.base_path+DEFAULT_GRAPH_CONFIG, f"{self.base_path}/graphs_config.json")
            return 0

    def newAppProfile(self, profile_name: str) -> int:
        if isfile(f"{self.base_path}/app_profiles/{profile_name}_config.sh"):
            print(f"{profile_name} profile already exists at {self.base_path}/app_profiles/{profile_name}_config.sh")
            print(f"Use > python3 run.py restoreappprofile {profile_name} < to restore the default template.")
            return -1
        else:
            return self.createNewAppProfile(profile_name)

    def restoreAppProfile(self, profile_name: str) -> int:
        if isfile(f"{self.base_path}/app_profiles/{profile_name}_config.sh"):
            remove(f"{self.base_path}/app_profiles/{profile_name}_config.sh")
        return self.createNewAppProfile(profile_name)
        
    def createNewAppProfile(self, profile_name: str) -> int:
        copyfile(f"{self.base_path}/src/defaults/default_app_profile.sh", f"{self.base_path}/app_profiles/{profile_name}_config.sh")
        print(f"Default config for '{profile_name}' succesfully created at {self.base_path}/app_profiles/{profile_name}_config.sh")
        return 0
    
    def newFilesystemProfile(self, profile_name: str) -> int:
        if isfile(f"{self.base_path}/filesystem_profiles/{profile_name}_config.sh"):
            print(f"{profile_name} profile already exists at {self.base_path}/filesystem_profiles/{profile_name}_config.sh")
            print(f"Use > python3 run.py restorefilesystemprofile {profile_name} < to restore the default template.")
            return -1
        else:
            return self.createNewFilesystemProfile(profile_name)
    
    def restoreFilesystemProfile(self, profile_name: str) -> int:
        if isfile(f"{self.base_path}/filesystem_profiles/{profile_name}_config.sh"):
            remove(f"{self.base_path}/filesystem_profiles/{profile_name}_config.sh")
        return self.createNewFilesystemProfile(profile_name)
    
    def createNewFilesystemProfile(self, profile_name: str) -> int:
        copyfile(f"{self.base_path}/src/defaults/default_filesystem_profile.sh", f"{self.base_path}/filesystem_profiles/{profile_name}_config.sh")
        print(f"Default config for '{profile_name}' succesfully created at {self.base_path}/filesystem_profiles/{profile_name}_config.sh")
        return 0