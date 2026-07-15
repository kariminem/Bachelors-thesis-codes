data = readtable('data.csv');
data = table2array(data);

time = data(:,1);
u1_commanded = data(:,2);
u2_commanded = data(:,3);
x_actual = data(:,4);
y_actual = data(:,5);
theta_actual = data(:,6);
v_actual = data(:,7);
omega_actual = data(:,8);

tau_linear = 0.4701;
tau_angular = 0.46969;

eqns = @(t, x, u1, u2) [x(4)*cos(x(3));
                        x(4)*sin(x(3));
                        x(5);
                        (u1 - x(4))/tau_linear;
                        (u2 - x(5))/tau_angular];

x0 = [x_actual(1); y_actual(1); theta_actual(1); v_actual(1); omega_actual(1)];

x_estimated = zeros(length(time), 5);

for i = 1:length(time)-1
    [T, X] = ode45(@(t,x) eqns(t, x, u1_commanded(i), u2_commanded(i)), [time(i) time(i+1)], x0);
    x0 = X(end,:)';
    x_estimated(i,:) = X(end,:);
end

figure;
subplot(2,1,1);
plot(time, v_actual, 'r', 'LineWidth', 2);
hold on;
plot(time, x_estimated(:,4), 'b', 'LineWidth', 2);
xlabel('Time (s)');
ylabel('Velocity (m/s)');
legend('Actual Linear Velocity', 'Estimated Linear Velocity');
title('Linear Velocity');

subplot(2,1,2);
plot(time, omega_actual, 'r', 'LineWidth', 2);
hold on;
plot(time, x_estimated(:,5), 'b', 'LineWidth', 2);
xlabel('Time (s)');
ylabel('Angular Velocity (rad/s)');
legend('Actual Angular Velocity', 'Estimated Angular Velocity');
title('Angular Velocity');

hold off;
