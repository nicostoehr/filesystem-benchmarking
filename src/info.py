'''
####################################################
#   Modular Filesystem Auto Benchmarking for HPC   #
#                   by Nico Stöhr                  #
####################################################
'''

def help_run() -> None:
    print("This is the help command.\n"+
          "Possile 1 argument commands:\n\n"+
          "help\n"+
          "setup\n"+
          "restoreconfig\n"+
          "\n"+
          "Possible 2 argument commands:\n\n"+
          "newappprofile *profile_name*\n"+
          "restoreappprofile *profile_name*\n"+
          "savestate *state_name*\n"+
          "loadstate *state_name*\n"
          )
    



def help_graphs() -> None:
    print("This is the graphs.py help function.\n"+
          "Use >python3 graphs.py <Result File .csv>\n"+
          "to create a graph for an application"+
          "or"+
          "use >python3 graphs.py <Result Dir>\n"+
          "to create a graph for all applications in the result dir."+
          "This function only takes 1 argument."
          )
    