# DEBUG MODE
DEBUG = False

from os import chdir, listdir, mkdir, getcwd
from subprocess import run, call, PIPE, CompletedProcess
from time import perf_counter


class BaseInstall:
    def __init__(self, base_path: str, app_name: str, app_dir: str, profile_dir: str) -> None:
        self.BASE_PATH: str = base_path
        self.APP_NAME: str = app_name
        self.APP_DIR: str = app_dir
        self.PROFILE_DIR: str = profile_dir

    # GIT CLONES THE APP AND CHANGES DIR INTO THE APP
    def init_app(self) -> int:
        chdir(self.APP_DIR)

        # remember app dir
        dir_before: set[str] = set(listdir())

        print(f"Downloading {self.APP_NAME}...")

        # run app's config git clone
        c1: CompletedProcess[bytes] = run(f"bash {self.PROFILE_DIR}/{self.APP_NAME}_config.sh source_url", shell=True)

        # use remembered app dir to switch into new app dir
        chdir(f"{self.APP_DIR}/{list(set(listdir())-dir_before)[0]}")

        return 0 if not c1.returncode else -1
    
    # COMPILE AND READY APP
    def compile_app(self) -> int:
        print(f"Compiling {self.APP_NAME}...")

        # run app's config compilation
        c2: CompletedProcess[bytes] = run((f"source {self.PROFILE_DIR}/{self.APP_NAME}_config.sh modules; " if not DEBUG else "")
                                          +f"bash {self.PROFILE_DIR}/{self.APP_NAME}_config.sh compilation", shell=True)

        return 0 if not c2.returncode else -1
        

class BaseRun:
    def __init__(self, base_path: str, app_name: str, app_dir: str, profile_dir: str) -> None:
        self.BASE_PATH: str = base_path
        self.APP_NAME: str = app_name
        self.APP_DIR: str = app_dir
        self.PROFILE_DIR: str = profile_dir

    def run(self) -> list:
        chdir(f"{self.APP_DIR}/{self.APP_NAME}")

        # start timer
        t0 = perf_counter()

        # run app
        r1: CompletedProcess[bytes] = run(f"bash {self.PROFILE_DIR}/{self.APP_NAME}_config.sh execution", shell=True)

        # stop timer 
        t1 = perf_counter()

        return [0 if not r1.returncode else -1, t1-t0]