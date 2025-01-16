#0 MODULE LIST
modules() {
    module load mpi/OpenMPI/4.1.5-GCC-12.2.0 devel/CMake/3.21.1
}

#1 GIT LINK:
source_url() {
    git clone --recurse-submodules https://storage.bsc.es/gitlab/hpc/gekkofs.git
}

#2 Installation commands:
compilation() {
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$PWD/gekkofs_deps/install/lib:$PWD/gekkofs_deps/install/lib64
    ./scripts/dl_dep.sh gekkofs_deps/git
    echo This step may take a while...
    srun -N 1 \
     --job-name=compile_gekkofs_deps \
     --output=compile_output.log \
     --ntasks=1 \
     --time=00:20:00 \
     --partition=parallel \
     -A m2_zdvresearch \
     bash -c 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/gekkofs_deps/install/lib:/lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/gekkofs_deps/install/lib64 && module load mpi/OpenMPI/4.1.5-GCC-12.2.0 devel/CMake/3.21.1 && ./scripts/compile_dep.sh /lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/gekkofs_deps/git /lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/gekkofs_deps/install && mkdir /lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/daemon && mkdir /lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/build && cd /lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/build && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=/lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/gekkofs_deps/install -DCMAKE_INSTALL_PREFIX=/lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/daemon .. && make -j8 install'
    cp /lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/src/defaults/gekkofs_config /lustre/miifs01/project/zdvresearch/nstoehr/bachelor/filesystem-benchmarking/filesystems/gekkofs/gekkofs_config
}

#3 Run command:
execution() {
    /scripts/run/gkfs -c gekkofs_config start
}

#4 Kill command:
termination() {
    /scripts/run/gkfs -c gekkofs_config stop
}



# Check which function to call based on the argument
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 {modules|source_url|compilation|execution|termination}"
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
    termination)
        termination
        ;;
    *)
        echo "Invalid argument: $1"
        echo "Usage: $0 {modules|source_url|compilation|execution|termination}"
        exit 1
        ;;
esac