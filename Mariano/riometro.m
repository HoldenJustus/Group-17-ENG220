
% Cuba, NM Bus Schedule Analysis
% ENG 220 - Mariano Montenegro
% Source: Rio Metro Route 8 Schedule

clear;
clc;
close all;

% STEP 1: Enter bus departure times
% Using 24-hour time

departureTimes = [8 + 19/60, 15 + 30/60];

% STEP 2: Clean and organize the data

departureTimes = sort(departureTimes);

% Check for missing values
if any(isnan(departureTimes))
    error('Missing departure times found.');
end

% Check for invalid times
if any(departureTimes < 0 | departureTimes >= 24)
    error('Invalid departure time found.');
end

% Remove duplicate departure times
departureTimes = unique(departureTimes);

% STEP 3: Calculate time between departures

timeGap = diff(departureTimes);

gapHours = floor(timeGap);
gapMinutes = round((timeGap - gapHours) * 60);

fprintf('Number of departures: %d\n', ...
    length(departureTimes));

fprintf('Time between departures: %d hours %d minutes\n', ...
    gapHours, gapMinutes);

% STEP 4: Create timeline graph

figure(1);

plot(departureTimes, [1 1], 'o-', ...
    'LineWidth', 3, ...
    'MarkerSize', 12);

hold on;

% Label each departure
text(departureTimes(1), 1.08, '8:19 AM', ...
    'HorizontalAlignment', 'center', ...
    'FontSize', 12);

text(departureTimes(2), 1.08, '3:30 PM', ...
    'HorizontalAlignment', 'center', ...
    'FontSize', 12);

% Label the gap
middleTime = mean(departureTimes);

text(middleTime, 0.88, ...
    '7 hours 11 minutes between departures', ...
    'HorizontalAlignment', 'center', ...
    'FontSize', 11);

% Format graph
xlim([7 17]);
ylim([0.7 1.3]);

xticks([8 10 12 14 16]);
xticklabels({'8 AM','10 AM','12 PM','2 PM','4 PM'});

yticks([]);

xlabel('Time of Day');
title('Rio Metro Route 8 - Cuba Bus Departures');

grid on;
hold off;

% STEP 5: Save graph

exportgraphics(gcf, 'Cuba_Bus_Timeline.png', ...
    'Resolution', 300);

% STEP 6: Save cleaned data

tripNames = ["Morning"; "Afternoon"];

results = table(tripNames, departureTimes', ...
    'VariableNames', {'Trip', 'DepartureHour'});

writetable(results, 'Cuba_Bus_Cleaned_Data.csv');

disp(results);

fprintf('\nBus schedule analysis complete!\n');
