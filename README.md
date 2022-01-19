# multi-camera, motion-capture, markerless capture c++ framework `mc_dev`

The `mc_dev` framework is a suite of C++ tools created for enabling development of multi-camera markerless motion capture tools, but is likely to be useful to all CAMERA researchers using C++ and multiple cameras.

A brief summary of some of the key features are:

  * Camera calibration: full suite of tools for detection of calibration boards, annotating cross-camera matches, intrinsic calibration and calibration of a network of overlapping cameras, including Ceres based bundle adjustment.
  * Simplistic OpenGL renderer: define models, scene graph, shaders, and camera (camera compatible with calibrations!), and avoid all the low-level OpenGL without needing a full graphics engine.
  * Background subtraction: 
  * Occupancy maps for multi-camera detection, tracking, and cross-camera object associations.
  * Fitting body models (SMPL, STAR, Dynadog) to data (point clouds, mocap, sparse 3D pose, DensePose) - Older stuff using Ceres, newer stuff using MXNet
  * sprint and skeleton projects

The full framework has been split into a number of repositories so that parts can be more easily shared:

  - `mc_base`: a top level directory in which to put the other parts of the project
  - `mc_core`: core framework library and tools, including calibration, image io and renderer.
  - `mc_bgs`: tools and libs for background subtraction. Includes a clone of 3rd party IMBS bgs algorithm.
  - `mc_sds`: implementation of //Stochastic Diffusion Search// - well, more or less. A kind of evolutionary algorithm for non-linear minimisation. Not the fastest solver in the world, but easy to use and quite robust.
  - `mc_imgproc`: image processing tools like debayering and ASEF/MSER filters
  - `mc_grabber`: Tools as deployed on //Boromir// for grabbing images/video from the JAI cameras using the SISO grabbers.
  - `mc_reconstruction`: Occupancy maps, and sparse-pose-fusion (e.g. take 2D pose detections from OpenPose or AlphaPose and do cross-camera association and 3D reconstruction)
  - `mc_fitting`: Implementations of models like SMPL, STAR, DynaDog and solvers to fit the models to point clouds, motion capture markers, sparse pose, and dense pose
  - `mc_footContact`: Tools for the foot contact project for sprinting and skeleton.
  - `mc_skeleton`: Tools and experiments for tracking skeleton athletes
  - `mc_experiments`: A place for miscellaneous tools and experiments before they get their own repo or get integrated into other repos
  - 

## `mc_base`

The `mc_base` repo provides a convenient base in which to place all other repositories.

Many of the reposotories will look for other `mc_` family repos in the same root they themselves are in, and `mc_base` makes for a good place to put that root.

Hence, the recommended way of using the whole framework is to first pull `mc_base`, them `mc_core` and any other repos you need.

```bash
   cd /where/you/keep/code-projects
   git clone camera@rivendell.cs.bath.ac.uk:mc_base mc_dev
   cd mc_dev
   git clone camera@rivendell.cs.bath.ac.uk:mc_core mc_core
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

## Building

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
   scons mc_bgs/build/debug -j6
```

## Install

There is also an install command which will install all repository programmes under `/opt/mc_bin/` so you can have `/opt/mc_bin/mc_core/x` for all the `mc_core` tools.




