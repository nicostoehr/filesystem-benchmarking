# DEBUG MODE
DEBUG = False

from os import chdir, listdir, mkdir, getcwd
from subprocess import run, call, PIPE, CompletedProcess
from time import perf_counter


class BaseInstall:
    def __init__(self, base_path: str, fs_name: str, fs_dir: str, profile_dir: str) -> None:
        self.BASE_PATH: str = base_path
        self.FS_NAME: str = fs_name
        self.FS_DIR: str = fs_dir
        self.PROFILE_DIR: str = profile_dir

    # GIT CLONES THE FS AND CHANGES DIR INTO THE FS DIR
    def init_fs(self) -> int:
        chdir(self.FS_DIR)

        # remember fs dir
        dir_before: set[str] = set(listdir())

        print(f"Downloading {self.FS_NAME}...")

        # run fs's config git clone
        c1: CompletedProcess[bytes] = run(f"bash {self.PROFILE_DIR}/{self.FS_NAME}_config.sh source_url", shell=True)

        # use remembered fs dir to switch into new fs dir
        chdir(f"{self.FS_DIR}/{list(set(listdir())-dir_before)[0]}")

        return 0 if not c1.returncode else -1
    
    # COMPILE AND READY FS
    def compile_fs(self) -> int:
        print(f"Compiling {self.FS_NAME}...")

        # run fs's config compilation
        c2: CompletedProcess[bytes] = run((f"source {self.PROFILE_DIR}/{self.FS_NAME}_config.sh modules" if not DEBUG else "")
                                          +f"bash {self.PROFILE_DIR}/{self.FS_NAME}_config.sh compilation", shell=True)

        return 0 if not c2.returncode else -1
        

class BaseRun:
    def __init__(self, base_path: str, fs_name: str, fs_dir: str, profile_dir: str) -> None:
        self.BASE_PATH: str = base_path
        self.FS_NAME: str = fs_name
        self.FS_DIR: str = fs_dir
        self.PROFILE_DIR: str = profile_dir

    def run(self) -> list:
        chdir(f"{self.FS_DIR}/{self.FS_NAME}")

        r1: CompletedProcess[bytes] = run(f"bash {self.PROFILE_DIR}/{self.APP_NAME}_config.sh execution", shell=True)

        return 0 if not r1.returncode else -1
    
    def stop(self) -> list:
        chdir(f"{self.FS_DIR}/{self.FS_NAME}")

        r2: CompletedProcess[bytes] = run(f"bash {self.PROFILE_DIR}/{self.APP_NAME}_config.sh termination", shell=True)

        return 0 if not r2.returncode else -1