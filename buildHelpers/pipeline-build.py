import os,sys



"""
    Build the markerless motion capture pipeline including openpose and opensim.
    
    Set the depsDir and then run.
    
    Assumes a fresh ubuntu 22.04 LTS system. 
    
    Will install cuda-toolkit 11.8
    
    CAUTION!! Script will modify your /etc/ld.so.conf file !!
    
"""

# where to download dependencies
depsDir = "/data2/software/"

# which version of openCV to use
ocvVersion = "4.6.0"

# where to install mc_dev binaries
mcbinDir = "/opt/mc_bin"


cwd = os.getcwd()
if cwd[-6:].find("mc_dev") < 0:
	print( "Expected to be in root of mc_dev (mc_base) directory" )
	exit(0)



# -----------------------------
# system installs
# -----------------------------

os.system("sudo apt-get update")
os.system("sudo apt-get -y install build-essential")
os.system("sudo apt-get -y install apt-utils")
os.system("sudo apt-get -y install git")
os.system("sudo apt-get -y install cuda-toolkit-11-8")
os.system("sudo apt-get -y install libcudnn8-dev")
os.system("sudo apt-get -y install wget")
os.system("DEBIAN_FRONTEND=noninteractive sudo apt-get -y install intel-mkl-full libmkl-dev")

# -----------------------------
# Pull in the mc_dev repos relevant to the mocap pipeline
# -----------------------------
os.system("bash cloneMocapRepos.sh")


# -----------------------------
# dependencies from package manager.
# -----------------------------


os.system("sudo apt install -y \
                                libsfml-dev \
                                libglew-dev \
                                libfreetype-dev \
                                libegl-dev \
                                libeigen3-dev \
                                libboost-filesystem-dev \
                                libmagick++-dev \
                                libconfig++-dev \
                                libsnappy-dev \
                                libceres-dev \
                                libavformat-dev \
                                libavcodec-dev \
                                libavutil-dev \
                                libswscale-dev \
                                ffmpeg \
                                libncurses-dev \
                                libassimp-dev \
                                scons \
                                pandoc \
                                vim \
                                rsync" )




# -----------------------------
# OpenCV
# we could get it from the package manager, but we'll do ourselves - 
#   yes this makes the build slow but we get more control.
# -----------------------------

os.system("sudo apt-get update --fix-missing")
os.system("sudo apt-get -y install cmake")


os.chdir(depsDir)
os.system("git clone https://github.com/opencv/opencv.git")
os.system("git clone https://github.com/opencv/opencv_contrib.git")

os.system("sudo apt-get -y install python3-pip")
os.system("python3 -m pip install numpy scipy matplotlib")

os.chdir("opencv_contrib")
os.system("git checkout %s"%ocvVersion)

os.chdir("../opencv")
os.system("git checkout %s"%ocvVersion)
os.system("mkdir build")
os.chdir("build")
os.system("cmake -DOPENCV_ENABLE_NONFREE=ON -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules  -DOPENCV_GENERATE_PKGCONFIG=ON -DWITH_CUDA=ON -D WITH_OPENMP=ON -D CUDA_ARCH_BIN=75,80,86 ../")
os.system("make -j8")
os.system("sudo make install")

# -----------------------------
# HighFive for hdf5 files
# -----------------------------
os.chdir(depsDir)
os.system("sudo apt-get -y install libhdf5-dev")
os.system("sudo apt-get -y install libboost-serialization-dev")
os.system("git clone https://github.com/BlueBrain/HighFive.git")
os.chdir("HighFive")
os.system("mkdir build")
os.chdir("build")
os.system("cmake HIGHFIVE_UNIT_TESTS=OFF ../")
os.system("make -j8")
os.system("sudo make install")

# -----------------------------
# Nanoflann is used in various places.
# -----------------------------
os.chdir(depsDir)
os.system("git clone https://github.com/jlblancoc/nanoflann.git")
os.chdir("nanoflann")
os.system("git checkout d804d14325a7fcefc111c32eab226d15349c0cca")  # TODO: why did we want this specific commit?
os.system("mkdir build")
os.chdir("build")
os.system("cmake ../")
os.system("make -j8")
os.system("sudo make install")


# -----------------------------
# Try and build openpose 
# -----------------------------

os.chdir(depsDir)
os.system("git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose")
os.chdir("openpose/")
os.system("git submodule update --init --recursive --remote")
os.system("bash ./scripts/ubuntu/install_deps.sh")
os.system("sudo apt-get -y install protobuf-compiler \
                libboost-all-dev libhdf5-dev libatlas-base-dev")

# I found that the models didn't download and broke the build,
# but I could get them via a google drive instead:
os.system("pip install gdown")
os.system("gdown https://drive.google.com/uc?id=1QCSxJZpnWvM00hx49CJ2zky7PWGzpcEh")
os.system("sudo apt install unzip")
os.system("unzip models.zip")

os.system("mkdir build")
os.chdir("build")
os.system("cmake ../")
os.system("make -j8")


# -----------------------------
# EZC3D
# -----------------------------
os.chdir(depsDir)
os.system("sudo apt -y install swig")
os.system("git clone https://github.com/pyomeca/ezc3d.git")
os.mkdir("ezc3d/build")
os.chdir("ezc3d/build")
os.system("cmake ../ -DBINDER_PYTHON3=ON")
os.system("make -j8")
os.system("sudo make install")


# -----------------------------
# OpenSim
# -----------------------------
os.chdir(depsDir)
os.system("mkdir opensim")
os.chdir("opensim")
os.system("sudo apt-get install -y libfmt-dev")
os.system("sudo apt-get install -y lsb-release")
os.system("export JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8")
ldpre = "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libmkl_def.so:/usr/lib/x86_64-linux-gnu/libmkl_avx2.so:/usr/lib/x86_64-linux-gnu/libmkl_core.so:/usr/lib/x86_64-linux-gnu/libmkl_intel_lp64.so:/usr/lib/x86_64-linux-gnu/          libmkl_intel_thread.so:/usr/lib/x86_64-linux-gnu/libiomp5.so"
os.system("%s bash %s/mc_reconstruction/scripts/opensim-core-linux-build-script.sh -j 6 -p /%s/opensim"%(ldpre, cwd, depsDir))

os.chdir("%s/opensim/install/sdk/Python"%depsDir)
os.system("%s sudo python3 setup.py install"%ldpre)

os.system("sudo \"echo /deps/opensim/install/sdk/Simbody/lib/ >> /etc/ld.so.conf\"")
os.system("sudo \"echo /deps/opensim/install/sdk/lib/         >> /etc/ld.so.conf\"")
os.system("sudo \"echo /deps/opensim/install/opensim-core-dependencies/casadi/lib/  >> /etc/ld.so.conf\"")
os.system("sudo \"echo /usr/local/cuda-11.7/lib64/ >> /etc/ld.so.conf\"")
os.system("sudo ldconfig")

# -----------------------------
# now we can build mc_dev
# -----------------------------
os.chdir(cwd)
os.system("sed -i s@/opt/opensim@/%s/opensim@g mc_reconstruction/mcdev_recon_config.py"%depsDir)
os.system("sed -i \'s@\"%s/opensim/install/sdk/include/OpenSim/\",@&\n                        \"%s/opensim/install/sdk/spdlog/include/\",@\' mc_reconstruction/mcdev_recon_config.py"%(depsDir, depsDir))
os.system("scons -j6 install=true installDir=%s"%mcbinDir )


