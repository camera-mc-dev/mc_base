# base on an NVidia cuda, Ubuntu 20.04 system
FROM nvidia/cuda:11.6.0-devel-ubuntu20.04

# -----------------------------
# system installs
# -----------------------------

RUN apt-get update
RUN apt-get -y install build-essential
RUN ln -s /usr/share/zoneinfo/Europe/London /etc/localtime
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get -y install git
RUN apt-get -y install cuda-toolkit-11-6
RUN apt-get -y install libcudnn8-dev
RUN apt-get -y install wget
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install intel-mkl-full





# -----------------------------
# mc_base
# -----------------------------

# clone
RUN git clone camera@rivendell.cs.bath.ac.uk:mc_base mc_dev
RUN apt install scons
RUN apt install pandoc
WORKDIR /
RUN mkdir deps

# ----------------------------
# mc_core
# ----------------------------

# clone
WORKDIR mc_dev
RUN git clone camera@rivendell.cs.bath.ac.uk:mc_core


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
# mc_bgs
# ----------------------------

WORKDIR mc_dev
RUN scons mc_bgs/build/optimised/bin -j6

# ----------------------------
# mc_sds
# ----------------------------

WORKDIR mc_dev
RUN scons mc_sds/build/optimised/bin -j6

# ----------------------------
# mc_imgproc
# ----------------------------

RUN apt install libfftw3-dev
WORKDIR mc_dev
RUN scons mc_bgs/build/optimised/bin -j6

# ----------------------------
# mc_reconstruction
# ----------------------------

WORKDIR /
RUN git clone https://github.com/pyomeca/ezc3d.git
WORKDIR /deps/ezc3d
RUN mkdir build
WORKDIR /deps/ezc3d/build
RUN cmake ../
RUN make -j6
RUN make install

WORKDIR mc_dev
RUN scons mc_reconstruction/build/optimised/bin -j6


# ----------------------------
# mc_nets
# ----------------------------

# Update CMake
RUN apt-get -y install software-properties-common lsb-release
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
RUN apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
RUN apt update
RUN apt install kitware-archive-keyring
RUN rm /etc/apt/trusted.gpg.d/kitware.gpg
RUN apt-get update
RUN apt-get -y install cmake=3.19.5-0kitware1ubuntu20.04.1 cmake-data=3.19.5-0kitware1ubuntu20.04.1

# we need mxnet
WORKDIR /deps
RUN wget https://dlcdn.apache.org/incubator/mxnet/1.9.1/apache-mxnet-src-1.9.1-incubating.tar.gz -O mxnet-1.9.1.tar.gz
RUN tar -xzf mxnet-1.9.1
WORKDIR /deps/mxnet-1.9.1
RUN mkdir build
WORKDIR /deps/mxnet-1.9.1/build
RUN apt install ninja-build ccache
RUN cmake -DCMAKE_CUDA_COMPILER=/usr/local/cuda-11.6/bin/nvcc -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-11.6 -DMKL_INCLUDE_DIR=/usr/include/mkl/ ../
RUN make -j6


