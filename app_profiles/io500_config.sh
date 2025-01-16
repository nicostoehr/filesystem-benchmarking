#!/bin/bash

#0 MODULE LIST
modules() {
    module load mpi/OpenMPI/4.1.5-GCC-12.2.0 lang/Python/3.10.8-GCCcore-12.2.0
}


#1 GIT LINK:
source_url() {
    git clone https://github.com/IO500/io500
}


#2 Installation commands:
compilation() {
    ./prepare.sh
    ./io500 --list > config-all.ini
}


#3 Run command:
execution() {
    ./io500 config-all.ini
}

# Check which function to call based on the argument
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 {modules|source_url|compilation|execution}"
    exit 1
fi

case $1 in
    modules)
        modules
        ;;
    source_url)
        source_url
        ;;
    compilation)
        compilation
        ;;
    execution)
        execution
        ;;
    *)
        echo "Invalid argument: $1"
        echo "Usage: $0 {modules|source_url|compilation|execution}"
        exit 1
        ;;
esac