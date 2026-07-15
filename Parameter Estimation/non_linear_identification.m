data = csvread('data.csv', 1, 0);
time = data(:, 1);
u1 = data(:, 2);
u2 = data(:, 3);
v_actual = data(:, 7);
omega_actual = data(:, 8);

fun = @(tau, t) [u1 + (v_actual - u1).*exp(-t/tau(1)), u2 + (omega_actual - u2).*exp(-t/tau(2))];

tau0 = [1, 1]; %inital condition

t = time - min(time);

options = optimset('Display','iter');
tau = lsqcurvefit(fun, tau0, t, [u1, u2], [], [], options);

disp(['Estimated tau_linear: ', num2str(tau(1))])
disp(['Estimated tau_angular: ', num2str(tau(2))])
