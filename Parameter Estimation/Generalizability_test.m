new_data = readtable('new_data.csv');

t = new_data.time;
u1 = new_data.commanded_linear;
u2 = new_data.commanded_angular;
v_actual = new_data.v_actual;
omega_actual = new_data.omega_actual;

tau_linear = 0.47451;
tau_angular = 0.47407;
v_predicted = zeros(size(v_actual));
omega_predicted = zeros(size(omega_actual));

v_predicted(1) = u1(1);
omega_predicted(1) = u2(1);

dt = mean(diff(t));

for i = 2:length(t)
    dv = (u1(i) - v_predicted(i-1))/tau_linear;
    domega = (u2(i) - omega_predicted(i-1))/tau_angular;
    v_predicted(i) = v_predicted(i-1) + dv * dt;
    omega_predicted(i) = omega_predicted(i-1) + domega * dt;
end

figure;
plot(t, v_actual, 'b', 'LineWidth', 2);
hold on;
plot(t, v_predicted, 'r--', 'LineWidth', 2);
xlabel('Time (s)');
ylabel('Linear Velocity (m/s)');
legend('Actual', 'Predicted');
title('Linear Velocity: Actual vs Predicted');

figure;
plot(t, omega_actual, 'b', 'LineWidth', 2);
hold on;
plot(t, omega_predicted, 'r--', 'LineWidth', 2);
xlabel('Time (s)');
ylabel('Angular Velocity (rad/s)');
legend('Actual', 'Predicted');
title('Angular Velocity: Actual vs Predicted');
