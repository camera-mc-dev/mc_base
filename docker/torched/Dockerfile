# base on an NVidia cuda, Ubuntu 20.04 system
# FROM nvidia/cuda:11.8.0-devel-ubuntu20.04
FROM nvidia/cuda:11.7.1-devel-ubuntu20.04

# -----------------------------
# system installs
# -----------------------------

RUN apt-get update
RUN apt-get -y install build-essential
RUN apt-get -y install apt-utils
RUN ln -s /usr/share/zoneinfo/Europe/London /etc/localtime
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get -y install git
RUN apt-get -y install cuda-toolkit-11-7
RUN apt-get -y install libcudnn8-dev
RUN apt-get -y install wget
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install intel-mkl-full


# ----------------------------
# Do some mc_core dependencies here
# ----------------------------


WORKDIR /
RUN mkdir deps


RUN apt install -y \
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
        scons \
        pandoc



# openCV we do ourselves.
RUN apt-get -y install cmake

WORKDIR /deps
RUN git clone https://github.com/opencv/opencv.git
RUN git clone https://github.com/opencv/opencv_contrib.git

RUN apt-get -y install python3-pip
RUN python3 -m pip install numpy scipy matplotlib

WORKDIR /deps/opencv_contrib
RUN git checkout 4.6.0
WORKDIR /deps/opencv
RUN git checkout 4.6.0
RUN mkdir build
WORKDIR /deps/opencv/build
RUN cmake -DOPENCV_ENABLE_NONFREE=ON -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules  -DOPENCV_GENERATE_PKGCONFIG=ON -DWITH_CUDA=ON -D WITH_OPENMP=ON -D CUDA_ARCH_BIN=75,80,86 ../
RUN make -j8
RUN make install

# and we need HighFive for hdf5 files
WORKDIR /deps/
RUN apt-get -y install libhdf5-dev
RUN apt-get -y install libboost-serialization-dev
RUN git clone https://github.com/BlueBrain/HighFive.git
WORKDIR /deps/HighFive
RUN mkdir build
WORKDIR /deps/HighFive/build
RUN cmake HIGHFIVE_UNIT_TESTS=OFF ../
RUN make -j6
RUN make install

# and we use nanoflann in various places
WORKDIR /deps/
RUN git clone https://github.com/jlblancoc/nanoflann.git
WORKDIR /deps/nanoflann
RUN git checkout d804d14325a7fcefc111c32eab226d15349c0cca
RUN mkdir build
WORKDIR /deps/nanoflann/build
RUN cmake ../
RUN make -j6
RUN make install




# -----------------------------
# Copy in the source - do thus until
# the repos are public
# -----------------------------
COPY mc_dev /mc_dev




# -----------------------------
# mc_base
# -----------------------------

#
# Note, right now we can't clone.
# Once the repos are public, we can.
#

# clone
#RUN git clone camera@rivendell.cs.bath.ac.uk:mc_base mc_dev
#RUN git clone git@github.com:camera-mc-dev/mc_base mc_dev

# ----------------------------
# mc_core
# ----------------------------

# clone
WORKDIR /mc_dev
#RUN git clone camera@rivendell.cs.bath.ac.uk:mc_core
#RUN git clone git@github.com:camera-mc-dev/mc_core


# dependencies
# now we can build mc_core
WORKDIR /mc_dev/mc_core/
RUN scons build/optimised/bin -j6


# ----------------------------
# mc_torched
# ----------------------------

# get lib-torch
WORKDIR /deps
#RUN wget https://download.pytorch.org/libtorch/cu118/libtorch-cxx11-abi-shared-with-deps-2.1.0%2Bcu118.zip
#RUN wget 'https://download.pytorch.org/libtorch/cu118/libtorch-shared-with-deps-2.1.0+Bcu118.zip'
RUN wget 'https://download.pytorch.org/libtorch/cu117/libtorch-cxx11-abi-shared-with-deps-2.0.1%2Bcu117.zip'
RUN apt-get -y install unzip
RUN unzip libtorch*.zip


# get mc_torched - actually, we're copying things in now, so, don't!
WORKDIR /mc_dev
#RUN git clone camera@rivendell.cs.bath.ac.uk:mc_core
#RUN git clone git@github.com:camera-mc-dev/mc_torched

WORKDIR /mc_dev/mc_torched
RUN git checkout temporal


# adjust dependency paths of mc_torched
RUN sed -i 's|/data2/software|/deps|g' mcdev_torched_config.py

# forgot this
RUN apt-get -y install libncurses-dev

# build
RUN scons build/optimised/bin -j8

RUN echo -e "\n/deps/libtorch/lib/\n" >> /etc/ld.so.conf
RUN ldconfig
RUN apt-get -y install vim
