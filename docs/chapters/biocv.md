## Introduction

The BioCV pipeline is a toolchain for evaluating the performance of modern sparse pose detection systems as applied to 3D pose estimation, especially for use in biomechanics and sports.

The pipeline requires the following repositories of the `mc_` suite:

  1) `mc_core`
  2) `mc_reconstruction`
  3) `mc_sds`
  4) (future) `mc_nets`

Most of the BioCV tools are held within the `mc_reconstruction` repository, but you will doubtless want to make use of the calibration tools within `mc_core` as well.

## Outline of the process.

Consider a set of synchronised and calibrated videos observing the motion of a person, where the cameras have overlapping fields of view (note, a circular arrangement of cameras all sharing the same observed area is ideal, but a corridor of cameras can also be considered).

Many pose detection systems are based on single-camera analysis, and will detect a set of sparse keypoints in the image corresponding to parts/points on/in the human body. To elevate these detections to 3D we must first:

  1) match person detections between camera views
  2) track person detections though the scene
  3) robustly reconstruct keypoints in 3D
  4) apply temporal smoothing to remove jitter
  5) resolve keypoint information into meaningful body parameters

To do this, the BioCV pipeline performs:

  1) Occupancy map based cross-camera association and tracking
  2) sparse pose fusion
  3) Kalman filtering
  4) OpenSim IK solve

Other pleasing tools include the ability to:

  1) Render raw sparse pose detections
  2) Render c3d files over video (whether from markerbased or markerless reconstruction)
  3) Render OpenSim solve over video

## Brief walkthrough

### Recording data

We assume that you have a camera system suitable for recording _synchronised_ video - any good machine vision system is capable of this, you may also have some success with broadcast quality TV cameras (with genlocking), GoPros (?) and possibly even iPhones.

As well as hardware synchronisation, it is necessary to have good calibration of the cameras you are using. The `mc_core` repository has tools for camera calibration, and its documentation gives details of the process we use and have had good success with.

### Sparse Pose

In principle the BioCV framework can be used with _any_ sparse pose detector. In practice we have data loaders for AlphaPose and OpenPose - its only minor modifications to extend beyond that however, especially if it means just a change of skeleton while retaining the same data format.

By "Sparse Pose" we mean any "pose" detector that identifies keypoints on/in the body (major joints for example) - rather than body part segmentations (e.g. CDCL) or dense part segmentations (e.g. DensePose) or body model parameters (e.g. VIBE).

Please refer to OpenPose and AlphaPose directly for running those detectors on your video data.

We have been "playing" around with sparse pose detectors and expect to have our own implementation of one in the near future - but we won't be making claims of it being in some way better than the myriad other algorithms that are out there; it's purpose is to aide in our future research ambitions and maybe be useful in the mean time.

### The pipeline

   1) `mc_reconstruction/build/optimised/bin/trackSparsePoses <config file>`
   2) `mc_reconstruction/build/optimised/bin/fuseSparsePoses  <config file>`
   3) smoothing
   4) solving

### Occupancy based cross-camera person association and tracking

Systems such as OpenPose don't know about multiple cameras, and produce detections for independent views. (Yes, we are aware that OpenPose has a 3D reconstruction tool, but as far as we know, it is limited to a single person in the scene).

As such, there is no guarantee that person '1' in camera '3' is the same as person '1' in camera '2'. To be able to get a 3D reconstruction of the person/people in the scene, we must first determine which detection in each view corresponds to which other detection in each other view.

There are various ways to do this. The "obvious" way is to take a representative point from each detection (say, the "neck") and score how close that is to each other "neck" in the other views through epipolar geometry. The end result of that is a distance matrix and a clustering algorithm and, as it happens, a big mess (in our experience) which is hard to resolve without kind of knowing where people are in the first place.

Our preference was instead to use an occupancy map approach. Here, the observed space is divided up into cells which can be projected into each camera view. In so doing, we can deterimine quite quickly how many people each cell is consistent with and get some idea of the most probable locations of people. That then makes it easier to know where people probably are, and where distractors are, and how to resolve cross-camera associations.

Fuller details of the algorithm are available in the `mc_reconstruction` documentation.

After per-frame associations are completed, we can walk through the space of the occupancy maps over time to perform frame-to-frame tracking of the detected people. Again, see the `mc_reconstruction` documentation for details of the algorithm we used.

The relevant tool is part of `mc_reconstruction` and is called `trackSparsePoses`.

### Sparse Pose Fusion

Once we know the cross-camera and temporal associations we can set about recovering 3D reconstructions of the detected keypoints. Basically, this is triangulation, but there are a few reasons why the algorithm ends up being a bit more complicated than that.

First off, individual keypoint detections from individual camera views _might_ be ... crap. This can be caused by occlusions, confusions, or just plain stupidity of the detection algorithm and inherent ambiguity of 2D data. Often we might see OpenPose swap left-and-right for limbs, set both left and right leg detections down just one leg, etc..

As such we don't just naively trust the low-level detections.

For single keypoints (e.g. neck) we employ basic RANSAC approach to keypoint reconstruction. This can induce some extra unwanted jitter in our results but with the keypoints being so jittery anyway we think it is not so bad a cost.

For pairs of keypoints (e.g. left-right elbows, left-right shoulders) we do a 2-point non linear solve using our stochastic solver. During the solve, we _ignore_ the left/right labelling of the keypoints and allow them to solve to an optimal 3D location. After that we apply left/right labelling based on majority voting, or on user-imposed geometry constraints (e.g. we know this person is always facing towards the +ve y-axis, thus their right hand _must_ be towards +ve x); clearly such constraints are not always suitable.

The fusion tool is part of `mc_reconstruction` and is called `fuseSparsePoses` - full documentation is available in `mc_reconstruction`.

The reconstruction is written to a `.c3d` file using the EZC3D library.

### Sparse pose visualisations

We have a couple of tools for visualising the reconstructed 3D pose:

  1) `projectMocap`: Given one or more `.c3d` files (which are assumed to be synchronised to the video) this will render the "markers" in the file on the image. It does not show skeletons, instead aiming to use a low-key render that may not be the easiest to see by allows the precision vs. the images to be seen. Note that if you have synchronised mocap data then you _can_ use those `.c3d` files here (this is actually what the tool was first created for - checking our mocap/video time/calibration alignment)
  2) `compareMocap`: Given one or more `.c3d` files as above, this will render the markers _and_ some skeleton information back onto the video. People from different files will be shown in different colours allowing for some simplistic visual comparisons.



