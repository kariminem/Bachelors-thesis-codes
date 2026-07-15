# Bachelor's Thesis: Parameter Estimation and Model Predictive Control of a Differential Drive Robot

Full codebase and experimental data from my Bachelor's thesis, focused on system identification and Model Predictive Control (MPC) for a TurtleBot3 differential drive robot, implemented and tested on real hardware using ROS and CasADi.

## Highlights

* Designed and implemented a nonlinear MPC controller in CasADi/IPOPT to regulate a differential drive robot to a target pose under velocity constraints.
* Performed nonlinear system identification of the robot's linear and angular velocity dynamics using least squares curve fitting (lsqcurvefit) on real sensor data.
* Validated the identified model against independent data and tested its generalizability on a separate dataset collected under different maneuvers.
* Built a full ROS data collection pipeline: commanding the robot through a sequence of maneuvers, logging commanded vs actual velocity and pose in real time, and exporting to CSV for offline analysis.
* Closed the loop end to end: identified model to controller design to real time deployment on hardware, with results demonstrated on video.

## Demo

Real robot test of the MPC controller regulating the TurtleBot3 to the origin:

https://github.com/kariminem/Bachelors-thesis-codes/assets/90244177/a7a3fb02-3908-401e-8255-a2fb8e461cdb

(Local copy: [MPC test video/mpc_test_video.mp4](MPC%20test%20video/mpc_test_video.mp4))

## Repository structure

### `Data collection/`
ROS nodes that command the robot through a sequence of linear and angular velocity maneuvers, subscribe to odometry, and log commanded and actual state to CSV at high rate.
* `data_collection.py`: full state logging (position, orientation, linear and angular velocity) used for the primary identification and validation dataset.
* `data_collection_v2.py`: lighter weight logging used for the generalizability dataset.

### `Parameter Estimation/`
MATLAB scripts that estimate and validate the robot's first order velocity dynamics.
* `non_linear_identification.m`: estimates the linear and angular velocity time constants (tau) using nonlinear least squares curve fitting.
* `non_linear_validation.m`: integrates the identified model forward in time with `ode45` and compares predicted vs actual trajectories.
* `Generalizability_test.m`: tests the identified time constants against an independent dataset to confirm the model generalizes beyond the data it was fit on.

### `MPC controller design/`
* `MPC_casadi.py`: the MPC controller itself, formulated in CasADi with the identified dynamics, state and control weight matrices, actuator constraints, and terminal constraints, solved with IPOPT over a receding horizon.
* `testing_MPC.py`: ROS node that runs the controller in closed loop on the physical robot, subscribing to odometry and publishing velocity commands.

### `Collected Data/`
* `data.csv`: primary dataset used for identification and validation.
* `new_data.csv`: independent dataset used for the generalizability test.

### `MPC test video/`
Video of the tuned MPC controller driving the physical robot to the origin from a nonzero initial pose.

## Tech stack

ROS, Python, CasADi, IPOPT, MATLAB, TurtleBot3.
