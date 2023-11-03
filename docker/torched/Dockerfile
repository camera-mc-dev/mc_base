# base on an NVidia cuda, Ubuntu 20.04 system
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# -----------------------------
# system installs
# -----------------------------

RUN apt-get update
RUN apt-get -y install build-essential
RUN ln -s /usr/share/zoneinfo/Europe/London /etc/localtime
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get -y install git
RUN apt-get -y install cuda-toolkit-11-8
RUN apt-get -y install libcudnn8-dev
RUN apt-get -y install wget
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install intel-mkl-full





# -----------------------------
# mc_base
# -----------------------------

# clone
#RUN git clone camera@rivendell.cs.bath.ac.uk:mc_base mc_dev
RUN git clone git@github.com:camera-mc-dev/mc_base mc_dev
RUN apt install scons
RUN apt install pandoc
WORKDIR /
RUN mkdir deps

# ----------------------------
# mc_core
# ----------------------------

# clone
WORKDIR mc_dev
#RUN git clone camera@rivendell.cs.bath.ac.uk:mc_core
RUN git clone git@github.com:camera-mc-dev/mc_core


# dependencies
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
	ffmpeg

# openCV we do ourselves.
WORKDIR /deps
RUN git clone https://github.com/opencv/opencv.git
RUN git clone https://github.com/opencv/opencv_contrib.git

WORKDIR /deps/opencv_contrib
RUN git checkout 4.6.0
WORKDIR /deps/opencv
RUN git checkout 4.6.0
RUN mkdir build
WORKDIR /deps/opencv/build
RUN cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules  -DOPENCV_GENERATE_PKGCONFIG=ON -DWITH_CUDA=ON WITH_OPENMP=ON ../
RUN make -j4
RUN make install

# and we need HighFive for hdf5 files
WORKDIR /deps/
RUN apt install libhdf5-dev
RUN apt install libboost-serialization-dev
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
RUN mkdir build
WORKDIR /deps/nanoflann/build
RUN cmake ../
RUN make -j6
RUN make install

# now we can build mc_core
WORKDIR mc_dev
RUN scons mc_core/build/optimised/bin -j6


# ----------------------------
# mc_torched
# ----------------------------

# get lib-torch
#WORKDIR /deps
#RUN wget https://download.pytorch.org/libtorch/cu118/libtorch-cxx11-abi-shared-with-deps-2.1.0%2Bcu118.zip
RUN wget 'https://download.pytorch.org/libtorch/cu118/libtorch-shared-with-deps-2.1.0+Bcu118.zip'



# get mc_torched
WORKDIR /mc_dev
#RUN git clone camera@rivendell.cs.bath.ac.uk:mc_core
RUN git clone git@github.com:camera-mc-dev/mc_torched

# adjust dependency paths of mc_torched
RUN sed -i 's|/data2/software|/deps|g' mc_torched/mcdev_torched_config.py

# build
RUN scons mc_torched/build/optimised/bin -j8


