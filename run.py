'''
####################################################
#   Modular Filesystem Auto Benchmarking for HPC   #
#                   by Nico Stöhr                  #
####################################################
'''

# DEBUG MODE
DEBUG = False

# IMPORTS 

# src
from src import info, default, state
from src.info import help_run

#base
from app_profiles.app_base import app_base
from filesystem_profiles.filesystem_base import filesystem_base

# os
from os import getcwd, mkdir, listdir
from os.path import isdir, isfile

# sys
from sys import argv

# shutil
from shutil import rmtree

# json
from json import load

#datetime
from datetime import datetime


# MAIN 
def main(argc: int, argv: list[str]) -> int:

    # GLOBAL VARS
    BASE_PATH: str = getcwd()
    APPLICATION_LIST: list[str] = []
    FILESYSTEM_LIST: list[str] = []
    INSTALLED_APPLICATIONS: list[str] = []
    INSTALLED_FILESYSTEMS: list[str] = []

    # CHECK CONFIG
    if isfile(f"{BASE_PATH}/run_config.json"):
        with open(f"{BASE_PATH}/run_config.json") as in_json:
            json_dump = load(in_json)
            APPLICATION_LIST = json_dump["APPS_TO_RUN"]
            FILESYSTEM_LIST = json_dump["FILESYSTEMS_TO_RUN"]            
                
    # NO CONFIG
    else:
        print("Error. run_config.json not available.")
        print("Try > python3 run.py restoreconfig")
        return -1
    
    # CHECK FOR RESULTS, APPS, FILESYSTEMS, PROFILES, SAVES DIRECTORIES
    if not isdir(f"{BASE_PATH}/results"): mkdir(f"{BASE_PATH}/results") 
    if not isdir(f"{BASE_PATH}/apps"): mkdir(f"{BASE_PATH}/apps") 
    if not isdir(f"{BASE_PATH}/filesystems"): mkdir(f"{BASE_PATH}/filesystems") 
    if not isdir(f"{BASE_PATH}/saves"): mkdir(f"{BASE_PATH}/saves")
    if not isdir(f"{BASE_PATH}/app_profiles"): 
        print("app_profiles directory does not exist. Exiting programm.")
        return -1
    if not isdir(f"{BASE_PATH}/filesystem_profiles"):
        print("filesystem_profiles directory does not exist. Exiting programm.")
        return -1
    
    # INSTALLED APPS
    INSTALLED_APPLICATIONS = listdir(f"{BASE_PATH}/apps")
    INSTALLED_FILESYSTEMS = listdir(f"{BASE_PATH}/filesystems")

    # CHECK FOR APPLICATION PROFILES AND BASE PROFILE
    for application in APPLICATION_LIST:
        if not isfile(f"{BASE_PATH}/app_profiles/{application}_config.sh"):
            print(f"No {application}_config.sh in app_profiles dir found.")
            return -1
    if not isdir(f"{BASE_PATH}/app_profiles/app_base"):
        print("Base app profile not found.\nDid you delete it?")
        return -1
    else:
        if not isfile(f"{BASE_PATH}/app_profiles/app_base/app_base.py"):
            print("Base app profile's base.py not found.\nDid you delete it?")
            return -1
        
    # CHECK FOR FILESYSTEM PROFILES AND BASE PROFILE
    for filesystem in FILESYSTEM_LIST:
        if not isfile(f"{BASE_PATH}/filesystem_profiles/{filesystem}_config.sh"):
            print(f"No {filesystem}_config.sh in filesystem_profiles dir found.")
            return -1
    if not isdir(f"{BASE_PATH}/filesystem_profiles/filesystem_base"):
        print("Base filesystem profile not found.\nDid you delete it?")
        return -1
    else:
        if not isfile(f"{BASE_PATH}/filesystem_profiles/filesystem_base/filesystem_base.py"):
            print("Base filesystem profile's base.py not found.\nDid you delete it?")
            return -1

    # COMMANDS
    if argc > 0:
        for i, x in enumerate(argv): argv[i] = x.lower()

        # ONE ARG COMMANDS
        if argc == 1:

            # HELP 
            if argv[0] == "help":
                help_run()
                return 0
            
            # SETUP
            elif argv[0] == "setup":
                for app in list(set(APPLICATION_LIST) - set(INSTALLED_APPLICATIONS)):

                    installation = app_base.BaseInstall(BASE_PATH, app, f"{BASE_PATH}/apps", f"{BASE_PATH}/app_profiles")
        
                    # init app
                    if installation.init_app(): 
                        print(f"Error in {app} app initialization.")
                        return -1
                    else: print(f"{app} initialized succesfully.")
                    
                    # compile app
                    if installation.compile_app(): 
                        print(f"Error in {app} app compile.")
                        return -1
                    else: print(f"{app} compiled succesfully.")

                for fs in list(set(FILESYSTEM_LIST) - set(INSTALLED_FILESYSTEMS)):

                    installation = filesystem_base.BaseInstall(BASE_PATH, fs, f"{BASE_PATH}/filesystems", f"{BASE_PATH}/filesystem_profiles")
                    
                    # init fs
                    if installation.init_fs():
                        print(f"Error in {fs} filesystem initialization.")
                        return -1
                    else: print(f"{fs} initialized succesfully.")

                    # compile fs
                    if installation.compile_fs(): 
                        print(f"Error in {fs} filesystem compile.")
                        return -1
                    else: print(f"{fs} compiled succesfully.")
        
            # RESTORECONFIG
            elif argv[0] == "restoreconfig":
                if default.Restore(BASE_PATH).restoreRunConfig():
                    print("Error while restoring config.")
                    return -1
                else:
                    print("Succesfully exited.")
                    return 0

            # MISSING ARGS
            elif argv[0] in [
                "newappprofile",
                "restoreappprofile",
                "newfilesystemprofile",
                "restorefilesystemprofile",
                "savestate",
                "loadstate",]:
                print("Missing argument. Try again or use > python3 run.py help < for usage.")
                return -1

            # NO MATCH
            else: 
                print(f"Could not match {argv[0]}.\nTry > python3 run.py help")
                return -1

        # TWO ARG COMMANDS
        elif argc == 2:

            # NEWPROFILE *PROFILE NAME*
            if argv[0] == "newappprofile":
                return default.Restore(BASE_PATH).newAppProfile(argv[1])
            
            # RESTOREPROFILE *PROFILE NAME*
            elif argv[0] == "restoreappprofile":
                return default.Restore(BaseException).restoreAppProfile(argv[1])
            
            # SAVESTATE *FILENAME*
            elif argv[0] == "savestate":
                return state.save(BASE_PATH).saveState(argv[1])

            # LOADSTATE *FILENAME*
            elif argv[0] == "loadstate":
                return state.save(BASE_PATH).loadState(argv[1])
            
            # NO MATCH
            else: 
                print(f"Could not match {argv[0]}.\nTry > python3 run.py help")
                return -1
        
        # TOO MANY ARGUMENTS (3+)
        else: 
            print("Too many arguments given.\nTry > python3 run.py help")
            return -1

    # RUN
    else:
        # CHECK FOR ALL APPS
        for app in APPLICATION_LIST:
            if not app in INSTALLED_APPLICATIONS:
                print(f"{app} is not installed.\nRun > python3 run.py setup")
                return -1
        
        # CHECK FOR ALL FILESYSTEMS
        for fs in FILESYSTEM_LIST:
            if not fs in INSTALLED_FILESYSTEMS:
                print(f"{fs} is not installed.\nRun > python3 run.py setup")
                return -1

        TIMING_TABLE: dict[dict[str, float]] = dict()

        # FOR ALL FILESYSTEMS
        for current_filesystem in ["default"]+FILESYSTEM_LIST:
            
            # START FILESYSTEM
            filesystem_run: filesystem_base.BaseRun = None
            if not current_filesystem == "default":                
                filesystem_run = filesystem_base.BaseRun(BASE_PATH, current_filesystem, f"{BASE_PATH}/filesystems", f"{BASE_PATH}/filesystem_profiles")
                filesystem_run.run()

            # TIMING TABLE FS
            TIMING_TABLE[current_filesystem] = dict()

            # FOR ALL APPS
            for current_app in APPLICATION_LIST:
                
                app_run = app_base.BaseRun(BASE_PATH, current_app, f"{BASE_PATH}/apps", f"{BASE_PATH}/app_profiles")

                app_run_result = app_run.run()

                if app_run_result[0]: 
                    print(f"Error in {current_app} execution.")
                    return -1
                else:
                    print(f"{current_filesystem} | {current_app} run complete: {app_run_result[1]:.2f}s")
                    TIMING_TABLE[current_filesystem][current_app] = app_run_result[1]

            # STOP FILESYSTEM
            if filesystem_run:
                filesystem_run.stop()


            # ALL FILESYSTEM APPS COMPLETE
            print(f"{current_filesystem} testing complete.")

        # ALL FILESYSTEMS COMPLETE
        print(f"Filesystem testing complete.")

        # GET CURRENT DATETIME
        current_datetime: str = str(datetime.now())

        # FORMATE DATE AND TIME FOR RESULT NAME
        formated_datetime = f"{current_datetime[:10]}_{current_datetime[11:19].replace(':', '-')}"

        # CREATE RESULT OUTPUT DIR
        mkdir(f"{BASE_PATH}/results/{formated_datetime}")

        # OPEN APP RESULT FILES AND WRITE RESULTS TO .CSV
        for app_name in APPLICATION_LIST:
            with open(f"{BASE_PATH}/results/{formated_datetime}/{app_name}.csv", "w") as time_output_file:
                # writing headline
                time_output_file.write("Filesystem,Time Passed (seconds)")
                for fs_name, app_dict in TIMING_TABLE.items():
                    for app_time in app_dict.values():
                        # writing time of fs for current app
                        time_output_file.write(f"\n{fs_name},{app_time:.2f}")

                


        
    
        

exit(main(len(argv)-1, argv[1:])) if __name__ == "__main__" else exit(0)
