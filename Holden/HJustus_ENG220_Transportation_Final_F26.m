
%% Cuba, New Mexico Transportation Project
% Creates only three graphs:
% 1. Transportation methods used by workers
% 2. Travel time to work
% 3. Vehicles available per household
%
% Also exports the three CSV files needed by Streamlit:
% modes.csv, time.csv, vehicles.csv
%
% Select the three original ACS ZIP files when prompted.

clear; clc; close all;

%% Select ACS ZIP files
[fileNames, folder] = uigetfile('*.zip', ...
    'Select the three ACS ZIP files', 'MultiSelect', 'on');

if isequal(fileNames, 0)
    error('No files selected.');
end

if ischar(fileNames)
    fileNames = {fileNames};
end

required = ["B08006", "B08303", "B08201"];
zipPaths = struct();

for i = 1:numel(required)
    match = find(contains(string(fileNames), required(i)), 1);

    if isempty(match)
        error('Missing ACS ZIP file for table %s.', required(i));
    end

    zipPaths.(char(required(i))) = ...
        fullfile(folder, fileNames{match});
end

dataDir = fullfile(folder, 'acs_data');
chartDir = fullfile(folder, 'charts');

if ~isfolder(dataDir)
    mkdir(dataDir);
end

if ~isfolder(chartDir)
    mkdir(chartDir);
end

%% Transportation methods (ACS B08006)

modeLines = [3 4 8 14 15 16 17];

modeLabels = [
    "Drove alone"
    "Carpooled"
    "Public transportation"
    "Bicycle"
    "Walked"
    "Taxi/ride-hailing/motorcycle/other"
    "Worked from home"
];

modeExpected = [
    "Drove alone"
    "Carpooled"
    "Public transportation"
    "Bicycle"
    "Walked"
    "Taxi"
    "Worked from home"
];

[modes, check1] = processTable( ...
    zipPaths.B08006, "B08006", modeLines, ...
    modeLabels, modeExpected, dataDir);

%% Travel time to work (ACS B08303)

timeLines = 2:13;

timeLabels = [
    "Less than 5 minutes"
    "5-9 minutes"
    "10-14 minutes"
    "15-19 minutes"
    "20-24 minutes"
    "25-29 minutes"
    "30-34 minutes"
    "35-39 minutes"
    "40-44 minutes"
    "45-59 minutes"
    "60-89 minutes"
    "90 or more minutes"
];

timeExpected = [
    "Less than 5"
    "5 to 9"
    "10 to 14"
    "15 to 19"
    "20 to 24"
    "25 to 29"
    "30 to 34"
    "35 to 39"
    "40 to 44"
    "45 to 59"
    "60 to 89"
    "90 or more"
];

[travelTime, check2] = processTable( ...
    zipPaths.B08303, "B08303", timeLines, ...
    timeLabels, timeExpected, dataDir);

%% Vehicles per household (ACS B08201)

vehicleLines = 2:6;

vehicleLabels = [
    "No vehicle"
    "1 vehicle"
    "2 vehicles"
    "3 vehicles"
    "4+ vehicles"
];

vehicleExpected = [
    "No vehicle"
    "1 vehicle"
    "2 vehicles"
    "3 vehicles"
    "4 or more"
];

[vehicles, check3] = processTable( ...
    zipPaths.B08201, "B08201", vehicleLines, ...
    vehicleLabels, vehicleExpected, dataDir);

%% Export CSV files for Streamlit

writetable(modes, fullfile(folder, 'modes.csv'));
writetable(travelTime, fullfile(folder, 'time.csv'));
writetable(vehicles, fullfile(folder, 'vehicles.csv'));

checks = [check1; check2; check3];
writetable(checks, fullfile(folder, 'checks.csv'));

%% GRAPH 1: Transportation methods

figure('Color','w');

barWithMOE(modes);

ylabel('Percentage of workers');
title('Transportation Methods Used by Workers in Cuba, NM');

saveas(gcf, fullfile(chartDir, 'transportation_methods.png'));

%% GRAPH 2: Travel time to work

figure('Color','w');

barWithMOE(travelTime);

ylabel('Percentage of workers');
xlabel('Travel time to work');
title('Travel Time to Work in Cuba, NM');

saveas(gcf, fullfile(chartDir, 'travel_time.png'));

%% GRAPH 3: Vehicles per household

figure('Color','w');

barWithMOE(vehicles);

ylabel('Percentage of households');
title('Vehicles Available per Household in Cuba, NM');

saveas(gcf, fullfile(chartDir, 'vehicles_per_household.png'));

%% Display results

disp('TRANSPORTATION METHODS');
disp(modes);

disp('TRAVEL TIME');
disp(travelTime);

disp('VEHICLES PER HOUSEHOLD');
disp(vehicles);

disp('DATA CHECKS');
disp(checks);

fprintf('\nFinished processing Cuba, NM transportation data.\n');
fprintf('Exactly three graphs were created.\n');
fprintf('CSV files saved in: %s\n', folder);
fprintf('Graphs saved in: %s\n', chartDir);


%% LOCAL FUNCTIONS

function [out, chk] = processTable(zipPath, tab, lines, labels, expected, dataDir)

    xlsxFile = prepareFile(zipPath, dataDir);

    [rowLabels, geoNames, E, Mo] = readAcsXlsx(xlsxFile, tab);

    % Locate Cuba
    col = find(contains(geoNames, "Cuba", 'IgnoreCase', true), 1);

    assert(~isempty(col), ...
        'Cuba was not found in the %s workbook.', tab);

    % Verify expected category rows
    for i = 1:numel(lines)
        assert(contains(rowLabels(lines(i)), expected(i), ...
            'IgnoreCase', true), ...
            'Unexpected category in %s at row %d: %s', ...
            tab, lines(i), rowLabels(lines(i)));
    end

    % Extract estimates and margins of error
    total = E(1, col);
    totalMOE = Mo(1, col);

    count = E(lines, col);
    countMOE = Mo(lines, col);

    assert(isfinite(total) && total > 0, ...
        'Invalid total estimate in %s.', tab);

    % Calculate percentages
    percent = 100 .* count ./ total;

    percentMOE = percentMarginOfError( ...
        count, countMOE, total, totalMOE);

    % Reliability classifications
    cv = 100 .* (countMOE ./ 1.645) ./ count;

    reliability = repmat("High", numel(lines), 1);
    reliability(cv >= 12) = "Medium";
    reliability(cv >= 40 | ~isfinite(cv)) = "Low";
    reliability(isnan(countMOE)) = "Unknown";

    % Check percentages
    percentSum = sum(percent);

    passed = abs(percentSum - 100) < 0.5 && all(count >= 0);

    assert(passed, ...
        '%s percentages sum to %.2f%%.', tab, percentSum);

    % Create output table
    out = table( ...
        repmat("Cuba, NM", numel(lines), 1), ...
        labels(:), count, countMOE, percent, ...
        percentMOE, reliability, ...
        repmat(total, numel(lines), 1), ...
        'VariableNames', { ...
        'Geography', 'Label', 'Count', 'CountMOE', ...
        'Percent', 'PercentMOE', 'Reliability', 'TotalBase'});

    chk = table( ...
        "Cuba, NM", string(tab), total, percentSum, passed, ...
        'VariableNames', { ...
        'Geography', 'Table', 'TotalBase', 'PercentSum', 'Passed'});

end


function xlsxFile = prepareFile(zipPath, dataDir)

    [~, base] = fileparts(zipPath);

    xlsxFile = fullfile(dataDir, base, [base '.xlsx']);

    if ~isfile(xlsxFile)
        unzip(zipPath, dataDir);
    end

    assert(isfile(xlsxFile), ...
        'Could not find the extracted Excel workbook: %s', xlsxFile);

end


function [labels, geoNames, E, Mo] = readAcsXlsx(xlsxFile, tab)

    C = readcell(xlsxFile, 'Sheet', char(tab + " Values"));

    hdr = C(2,:);

    geoCols = find(cellfun( ...
        @(x) ischar(x) || isstring(x), hdr));

    geoNames = string(hdr(geoCols));

    labels = string(C(4:end,1));

    n = numel(labels);

    E = cellfun(@toNum, C(4:3+n, geoCols));

    Mo = cellfun(@toNum, C(4:3+n, geoCols + 1));

end


function value = toNum(x)

    if isnumeric(x) && ~isempty(x)
        value = double(x(1));
    else
        value = NaN;
    end

end


function moe = percentMarginOfError(count, countMOE, total, totalMOE)

    p = count ./ total;

    radicand = countMOE.^2 - (p.^2) .* totalMOE.^2;

    alternate = countMOE.^2 + (p.^2) .* totalMOE.^2;

    radicand(radicand < 0) = alternate(radicand < 0);

    moe = 100 .* sqrt(radicand) ./ total;

end


function barWithMOE(T)

    x = categorical(T.Label, T.Label);

    bar(x, T.Percent);

    hold on;

    errorbar(1:height(T), T.Percent, T.PercentMOE, ...
        'k.', 'LineWidth', 1.2);

    xtickangle(25);

    grid on;

    upper = max(T.Percent + T.PercentMOE);

    ylim([0 max(upper * 1.15, 1)]);

end
