'''
####################################################
#   Modular Filesystem Auto Benchmarking for HPC   #
#                   by Nico Stöhr                  #
####################################################
'''

# IMPORTS

# os
from os import listdir, getcwd
from os.path import isfile, isdir

# src
from src import default
from src.info import help_graphs

# pandas
from pandas import read_csv

# matplotlib
import matplotlib.pyplot as plt

# sys
from sys import argv

# json
from json import load


# MAIN
def main(argc: int, argv: list[str]) -> int:

    # GLOBAL VARS
    BASE_PATH: str = getcwd()
    GRAPHS_CONFIG: dict = dict()

    # CHECK CONFIG
    if isfile(f"{BASE_PATH}/graphs_config.json"):
        with open(f"{BASE_PATH}/graphs_config.json") as in_json:
            GRAPHS_CONFIG = load(in_json)           
                
    # NO CONFIG
    else:
        print("Error. graphs_config.json not available.")
        print("Try > python3 graphs.py restoreconfig")
        return -1

    # ONE ARG COMMANDS
    if argc == 1: 

        # help
        if argv[0] == "help":
            help_graphs()
            return 0
        
        elif argv[0] == "restoreconfig":
            if default.Restore(BASE_PATH).restoreGraphConfig():
                print("Error while restoring config.")
                return -1
            else:
                print("Succesfully exited.")
                return 0

        # check if argument is csv file
        elif isfile(argv[0]) and argv[0].endswith(".csv"):
            # plot graph
            return plot_csv(argv[0], GRAPHS_CONFIG)
        
        # check if argument is dir of csv files
        elif isdir(argv[0]):
            if not argv[0].endswith("/"): argv[0]+="/"
            result_dir: list[str] = listdir(argv[0])
            result_csvs: list[str] = [x for x in result_dir if x.endswith(".csv")]
            
            # no csv files in dir
            if len(result_csvs) < 1:
                print(f"No .csv files in {argv[0]}")
                return -1
            
            # plot all graphs
            else:
                return_code: int = 0
                for csv_file in result_csvs:
                    return_code = sum([plot_csv(f"{argv[0]}{csv_file}", GRAPHS_CONFIG)])
                return 0 if not return_code else -1

        # invalid path provided
        else:
            print("Invalid path provided.")
            return -1


    # WRONG NUMBER OF ARGUMENTS
    else: 
        print("Invalid number of arguments.")
        print("This script takes 1 argument.")
        return -1


def plot_csv(csv_file_path: str, graphs_config: dict) -> int:

    # find filename position in path
    path_name_split: int = len(csv_file_path) - 1
    while path_name_split >= 0 and csv_file_path[path_name_split] != "/": path_name_split -= 1

    # read in result csv
    data = read_csv(csv_file_path)
        
    plt.figure(figsize=(graphs_config["fig_size_x"], graphs_config["fig_size_y"]))
    
    # create the bar chart
    plt.bar(data[data.columns[0]], data[data.columns[1]], color=graphs_config["bar_color"], edgecolor=graphs_config["edge_color"])
    
    # add labels and title using the first row's headers
    plt.title(f"{data.columns[0]} / {data.columns[1]}", fontsize=16)
    plt.xlabel(data.columns[0], fontsize=graphs_config["title_font_size"])
    plt.ylabel(data.columns[1], fontsize=graphs_config["label_font_size"])
    
    # improve the layout
    plt.xticks(rotation=graphs_config["xticks_rotation"])
    plt.grid(axis='y', linestyle='--', alpha=graphs_config["grid_alpha"])
    
    # set a standard limit for the y-axis
    max_column = data[data.columns[1]].max()
    plt.ylim(0, max_column*1.05)
    
    # save the chart
    plt.tight_layout()
    plt.savefig(f"{csv_file_path[:-4]}_chart.png", dpi=300)

    return 0


exit(main(len(argv)-1, argv[1:])) if __name__ == "__main__" else exit(0)



