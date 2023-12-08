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
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install intel-mkl-full libmkl-dev


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
	libncurses-dev \
	libassimp-dev \
	scons \
	pandoc \
	vim \
	rsync


# openCV we do ourselves - yes this makes the build slow but we get more control.
RUN apt-get update --fix-missing
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
# Try and build openpose 
# Long time since we last did this...
# -----------------------------

WORKDIR /deps/
RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
WORKDIR /deps/openpose/
RUN git submodule update --init --recursive --remote
RUN bash ./scripts/ubuntu/install_deps.sh
RUN apt-get -y install protobuf-compiler \
                libboost-all-dev libhdf5-dev libatlas-base-dev

# I found that the models didn't download and broke the build,
# but I could get them via a google drive instead:
RUN pip install gdown
RUN gdown https://drive.google.com/uc?id=1QCSxJZpnWvM00hx49CJ2zky7PWGzpcEh
RUN apt install unzip
RUN unzip models.zip

RUN mkdir build
WORKDIR /deps/openpose/build
RUN cmake ../
RUN make -j6




# -----------------------------
# Next job, EZC3D
# -----------------------------
WORKDIR /deps/
RUN apt -y install swig
RUN git clone https://github.com/pyomeca/ezc3d.git
WORKDIR ezc3d/build
RUN cmake ../ -DBINDER_PYTHON3=ON
RUN make
RUN make install



# -----------------------------
# Copy in mc_dev (could change to pulling from github once public...)
# We wont build yet - we mostly want it for out version of the OpenSim
# build script....
# -----------------------------
COPY mc_dev /mc_dev


# ----------------------------
# And my favourite build... OpenSim...
# This takes an age, but at least our script makes it "easy"
# ----------------------------
WORKDIR /deps/opensim
RUN apt-get install -y libfmt-dev
RUN apt-get install -y lsb-release
RUN apt-get install sudo # only because the script tries to use sudo... a bit weird to have it unless we set up a user account..
ENV JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libmkl_def.so:/usr/lib/x86_64-linux-gnu/libmkl_avx2.so:/usr/lib/x86_64-linux-gnu/libmkl_core.so:/usr/lib/x86_64-linux-gnu/libmkl_intel_lp64.so:/usr/lib/x86_64-linux-gnu/libmkl_intel_thread.so:/usr/lib/x86_64-linux-gnu/libiomp5.so
RUN bash /mc_dev/mc_reconstruction/scripts/opensim-core-linux-build-script.sh -j 6 -p /deps/opensim

WORKDIR /deps/opensim/install/sdk/Python
RUN python3 setup.py install

RUN echo /deps/opensim/install/sdk/Simbody/lib/ >> /etc/ld.so.conf
RUN echo /deps/opensim/install/sdk/lib/         >> /etc/ld.so.conf
RUN echo /deps/opensim/install/opensim-core-dependencies/casadi/lib/  >> /etc/ld.so.conf
RUN echo /usr/local/cuda-11.7/lib64/ >> /etc/ld.so.conf
RUN ldconfig





# ------------------------------
# Now we can build the mc_dev stuff
# -----------------------------



# now we can build mc_dev
WORKDIR /mc_dev
RUN sed -i s@/opt/opensim@/deps/opensim@g mc_reconstruction/mcdev_recon_config.py 
RUN sed -i 's@"/deps/opensim/install/sdk/include/OpenSim/",@&\n                        "/deps/opensim/install/sdk/spdlog/include/",@' mc_reconstruction/mcdev_recon_config.py
RUN scons -j6 install=true


# ------------------------------------
# Final "debugging" fixes. YMMV, as they say.
# ------------------------------------

# for some reason, even though we've used a cuda-11.7 base container,
# install cuda-11.7 toolkit, and built everything with cuda 11.7, openpose
# complains about missing a cuda-12 library. Well, this is the easy fix.
RUN apt-get -y install cuda-toolkit-12


# ------------------------------------
# We don't want to be running everything as root,
# so we'll add a user for the container, and let them sudo if needs be.
# ------------------------------------

ARG DOCKER_USER=default_user
ARG UID=1001
ARG GID=1001
RUN groupadd -g $GID -o $DOCKER_USER
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $DOCKER_USER
RUN usermod -aG sudo $DOCKER_USER
RUN echo "$DOCKER_USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers && \
    chmod 0440 /etc/sudoers && \
    chmod g+w /etc/passwd

USER $DOCKER_USER

RUN echo dataRoot = "/data"\; > ~/.mc_dev.common.cfg
RUN echo shadersRoot = "/mc_dev/mc_core/shaders"\; >> ~/.mc_dev.common.cfg
RUN echo coreDataRoot = "/mc_dev/mc_core/data"\; >> ~/.mc_dev.common.cfg
RUN echo scriptsRoot = "/mc_dev/mc_core/python"\; >> ~/.mc_dev.common.cfg
RUN echo maxSingleWindowWidth = 1920\; >> ~/.mc_dev.common.cfg
RUN echo maxSingleWindowHeight = 1280\; >> ~/.mc_dev.common.cfg
RUN echo netsRoot  = "/mc_dev/mc_nets/data/"\; >> ~/.mc_dev.common.cfg
RUN echo ffmpegPath = "/usr/bin/ffmpeg"\; >> ~/.mc_dev.common.cfg

