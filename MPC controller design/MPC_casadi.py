import casadi as ca
import matplotlib.pyplot as plt
import numpy as np

# Model parameters
tau_v = 0.4701
tau_w = 0.46967

# Control horizon
N = 100


opti = ca.Opti()

# State variables and controls
X = opti.variable(5, N+1)  # state trajectory variables
U = opti.variable(2, N)    # control trajectory variables


x0 = opti.parameter(5)

# Dynamics model
for k in range(N):
    dx = X[3, k] * ca.cos(X[2, k]) * tau_v
    dy = X[3, k] * ca.sin(X[2, k]) * tau_v
    dtheta = X[4, k] * tau_w
    dv = U[0, k]
    dw = U[1, k]

    next_X = X[:, k] + ca.vertcat(dx, dy, dtheta, dv, dw)
    opti.subject_to(X[:, k+1] == next_X)


Q = np.diag([1, 1, 1, 0, 0])  # State weights
R = np.diag([1, 1])           # Control weights

# Cost function
J = 0
for k in range(N):
    J += ca.mtimes([X[:, k].T, Q, X[:, k]]) + ca.mtimes([U[:, k].T, R, U[:, k]])
opti.minimize(J)

# Initial condition
opti.subject_to(X[:, 0] == x0)

# Control input constraints
v_max = 0.26  # Maximum linear velocity
w_max = 1.81  # Maximum angular velocity
opti.subject_to(U[0, :] <= v_max)
opti.subject_to(U[0, :] >= -v_max)
opti.subject_to(U[1, :] <= w_max)
opti.subject_to(U[1, :] >= -w_max)

# Terminal constraints
x_desired = np.array([0, 0, 0, 0, 0])  # Desired final state
opti.subject_to(X[:, N] == x_desired)


opti.solver("ipopt")


T = 40


x = np.array([6, 6, 0, 0, 0])

x_traj = []
u_traj = []

for t in range(T):

    opti.set_value(x0, x)
    sol = opti.solve()


    u = sol.value(U[:, 0])


    x = x + np.array([x[3] * np.cos(x[2]) * tau_v,
                      x[3] * np.sin(x[2]) * tau_v,
                      x[4] * tau_w,
                      u[0],
                      u[1]])

    x_traj.append(x)
    u_traj.append(u)


x_traj = np.array(x_traj)
u_traj = np.array(u_traj)


plt.figure()
plt.plot(x_traj[:, 0], x_traj[:, 1])
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Position')

plt.figure()
plt.plot(x_traj[:, 2])
plt.xlabel('Time')
plt.ylabel('Theta')
plt.title('Orientation')

plt.figure()
plt.plot(u_traj)
plt.xlabel('Time')
plt.ylabel('Control input')
plt.title('Control Inputs')
plt.legend(['v', 'w'])

plt.show()
