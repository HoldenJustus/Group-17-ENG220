
% Cuba, New Mexico Transportation Analysis
% ENG 220 - Mariano Montenegro
% Source: 2024 ACS 5-Year Census Data
% Table B08006

clear;
clc;
close all;

% STEP 1: Read the Census CSV file

filename = 'acs2024_5yr_B08006_04000US35.csv';

data = readtable(filename, ...
    'VariableNamingRule', 'preserve');

fprintf('Original rows: %d\n', height(data));

% STEP 2: Find the locations

locations = ["Cuba, NM"; ...
    "Sandoval County, NM"; ...
    "New Mexico"; ...
    "United States"];

[found, rowIndex] = ismember(locations, ...
    string(data.name));

if any(~found)
    error('One or more locations are missing.');
end

% STEP 3: Select transportation categories

codes = {'B08006001', ... % Total workers
    'B08006003', ...       % Drive alone
    'B08006004', ...       % Carpool
    'B08006008', ...       % Public transit
    'B08006014', ...       % Bicycle
    'B08006015', ...       % Walk
    'B08006016', ...       % Other transportation
    'B08006017'};          % Work from home

% STEP 4: Extract the numbers

counts = zeros(length(locations), length(codes));

for i = 1:length(locations)

    for j = 1:length(codes)

        value = data{rowIndex(i), codes{j}};

        if iscell(value)
            value = value{1};
        end

        if ischar(value) || isstring(value)
            value = str2double(value);
        end

        counts(i,j) = value;

    end
end

% STEP 5: Clean and validate data

missingValues = sum(isnan(counts(:)));
negativeValues = sum(counts(:) < 0);

fprintf('Missing values: %d\n', missingValues);
fprintf('Negative values: %d\n', negativeValues);

if missingValues > 0 || negativeValues > 0
    error('Missing or invalid Census values found.');
end

% STEP 6: Organize transportation data

totalWorkers = counts(:,1);
transportCounts = counts(:,2:end);

methods = {'Drive Alone', 'Carpool', ...
    'Public Transit', 'Bicycle', ...
    'Walk', 'Other', 'Work From Home'};

% Check totals without requiring exact equality
% Small differences may occur in published estimates

for i = 1:length(locations)

    categoryTotal = sum(transportCounts(i,:));

    difference = categoryTotal - totalWorkers(i);

    fprintf('%s: Difference = %.0f workers\n', ...
        locations(i), difference);

    if abs(difference) > 0.01 * totalWorkers(i)
        warning('Large difference found for %s', ...
            locations(i));
    end

end

% STEP 7: Calculate percentages

percent = transportCounts ./ totalWorkers * 100;

% STEP 8: Create cleaned data table

results = table(string(methods'), ...
    transportCounts(1,:)', percent(1,:)', ...
    transportCounts(2,:)', percent(2,:)', ...
    'VariableNames', {'Method', ...
    'CubaCount', 'CubaPercent', ...
    'CountyCount', 'CountyPercent'});

disp('Transportation Analysis Results:');
disp(results);

% Save cleaned data

writetable(results, 'Cuba_Cleaned_Data.csv');

% STEP 9: Graph 1 - Cuba transportation methods

figure(1);

bar(percent(1,:));

set(gca, 'XTick', 1:length(methods), ...
    'XTickLabel', methods);

xtickangle(40);

ylabel('Percentage of Workers (%)');
title('How Workers in Cuba, NM Get to Work');

ylim([0 100]);
grid on;

exportgraphics(gcf, 'Cuba_Transportation.png');

% STEP 10: Graph 2 - Cuba vs Sandoval County

figure(2);

bar(percent(1:2,:)');

set(gca, 'XTick', 1:length(methods), ...
    'XTickLabel', methods);

xtickangle(40);

ylabel('Percentage of Workers (%)');
title('Cuba vs Sandoval County Transportation');

legend('Cuba', 'Sandoval County', ...
    'Location', 'best');

ylim([0 100]);
grid on;

exportgraphics(gcf, 'Cuba_vs_County.png');

% STEP 11: Graph 3 - Regional comparison

figure(3);

bar(percent(:,1));

set(gca, 'XTick', 1:length(locations), ...
    'XTickLabel', locations);

xtickangle(25);

ylabel('Workers Driving Alone (%)');
title('Driving Alone: Regional Comparison');

ylim([0 100]);
grid on;

exportgraphics(gcf, 'Driving_Comparison.png');

% STEP 12: Display final results

fprintf('\n--- Cuba Transportation Summary ---\n');

fprintf('Total workers: %.0f\n', totalWorkers(1));

for j = 1:length(methods)

    fprintf('%s: %.1f%%\n', ...
        methods{j}, percent(1,j));

end

fprintf('\nAnalysis complete!\n');
