## `mc_dev`

The `mc_dev` framework is a suite of tools created for various experiments in multi-camera computer vision, but especially markerless motion capture. Depending how you feel, you can think of the `mc_` as standing for **M**ulti-**C**amera, **M**otion **C**apture or **M**arkerless **C**apture.

The full framework is a general mush of related experiments never meant to be seen in public - however, some key parts have been tidied up to support publications, especially the BioCV dataset.

The main repositories are thus:

  - `mc_base`: a top level directory in which to put the other parts of the project
  - `mc_core`: core framework library and tools, including calibration, image io and renderer.
  - `mc_reconstruction`: Occupancy maps, and sparse-pose-fusion (e.g. take 2D pose detections from OpenPose or AlphaPose and do cross-camera association and 3D reconstruction)
  - `mc_opensim`: A set of Python scripts to take the output of `mc_reconstruction` and pass through OpenSim solvers.  
  - `mc_sds`: implementation of *Stochastic Diffusion Search* - well, more or less. A kind of evolutionary algorithm for non-linear minimisation. Not the fastest solver in the world, but easy to use and quite robust.
  - `mc_grabber`: Tool used for recording images from our machine vision system based on JAI cameras and SISO coaxpress grabbers. This could be of use to others are it _should_ be extendable to other machine vision systems, but I'm not going to try and claim it is anywhere near "consumer grade" software - having said that, I've used far worse "professional" pieces of software...
   - `mc_imgproc`: image processing tools like debayering and ASEF/MSER filters


Dig enough on the CAMERA gitolite server and you'll find other repositories too:

  - `mc_bgs`: tools and libs for background subtraction. Includes a clone of 3rd party IMBS bgs algorithm.
 - `mc_fitting`: Implementations of models like SMPL, STAR, DynaDog and solvers to fit the models to point clouds, motion capture markers, sparse pose, and dense pose
  - `mc_footContact`: Software that relates to our foot-contact papers
  - `mc_skeleton`: Experiments for tracking skeleton athletes.
  - `mc_experiments`: A place for miscellaneous tools and experiments before they get their own repo or get integrated into other repos
  - `mc_torched`: LibTorch related experiments, particularly for NeRF
  - `mc_nets`: MXNet related experiments, calibration board detection, pose detectors, etc...

Especially for the latter repositories, the focus of work shifts around and so expect a fair degree of bit-rot and a lot of experiments have been rapid bodges with no intent to share that were in many ways learning experiments, especially `mc_nets`. 


## `mc_base`

The `mc_base` repo provides a convenient base in which to place all other repositories.

Many of the reposotories will look for other `mc_` family repos in the same root they themselves are in, and `mc_base` makes for a good place to put that root.

Hence, the recommended way of using the whole framework is to first pull `mc_base`, then `mc_core` and any other repos you need.

```bash
   cd /where/you/keep/code-projects
   git clone git@github.com:camera-mc-dev/mc_base mc_dev
   cd mc_dev
   git clone git@github.com:camera-mc-dev/mc_core mc_core
```

There are a couple of convenience scripts within `mc_base`:

You can issue a `git pull` on all the `mc_` family repos that you have available:

```bash
   python3 pullAll.py
```

You can issue a `git status` on all the `mc_` family repos that you current have:

```bash
   python3 statusAll.py
```

More complete build instructions are discussed in each repository, but overall, the `scons` tool is used for building all repositories, and each repository has a `mcdev_<name>_config.py` for setting build options and library paths. `scons` is mostly just Python so it should be simple enough to get a grip of.

### Specific use cases

`mc_dev` is a agglomeration of things used for various experiments, but there are core uses. Specific, public instructions pertinent to those core uses can be found on github:

  1) markerless motion capture pipeline (BioCV dataset): [Instructions here](https://github.com/camera-mc-dev/.github/blob/main/profile/mocapPipe.md)

You will find Dockerfiles or scripts for helping to automate the build process for those specific use cases within the `mc_base` repository under either the `docker` or `buildHelpers` directories. Refer to the instructions for each use case linked above for more details of each.


### Building

If you build from the base directory then dependencies between repositories will be automatically resolved - e.g. the build process will ensure `mc_core` is up to date before building `mc_reconstruction`

The basic build command:

```bash
   scons -j6
```

will build all repos in optimised

Individual targets within repos can be built as well, such as:

```bash
   scons mc_core/build/optimised/bin/renderSyncedSources -j6
```

or

```bash
   scons mc_reconstruction/build/optimised/ -j6
```

### Install

There is also an install command which will install all repository programmes under `/opt/mc_bin/` so you can have `/opt/mc_bin/mc_core/x` for all the `mc_core` tools.

You can change the target directory for the installation from `/opt/mc_bin` to another location using the `installDir` option. For example...


```bash
   scons -j6 install=True installDir=~/bin/mc_bin
```

