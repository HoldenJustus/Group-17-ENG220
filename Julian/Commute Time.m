%% Commute Time Analysis
% Loads "Commute Time.csv" (ACS travel-time-to-work data) into MATLAB and
% compares commute times between places (United States vs. Cuba, NM).
%
% Put this script in the same folder as the CSV and press Run.
%
% Columns in the CSV:
%   Travel Time ID, Travel Time, Year, Commuter Population,
%   Commuter Population Moe, Place, Place ID, share
%   - Commuter Population     = number of workers in that travel-time range
%   - Commuter Population Moe = margin of error (90% confidence) for that count
%   - share                   = fraction of that place's commuters (0-1)

clear; clc; close all;

%% 0) Check that no personal files are hiding MATLAB's plotting functions
% (e.g. a file called plot.m in your MATLAB folder breaks plot())
builtinFuncs = {'plot','bar','barh','pie','errorbar','legend','title','xlabel','ylabel'};
for k = 1:numel(builtinFuncs)
    p = which(builtinFuncs{k});
    if ~isempty(p) && ~startsWith(p, matlabroot) && ~contains(p, 'built-in')
        error(['Your file "%s" has the same name as MATLAB''s %s() function.\n' ...
               'Rename or move that file, then run this script again.'], p, builtinFuncs{k});
    end
end

%% 1) Import the data
filename = 'Commute Time.csv';

% Look for the CSV next to this script first, then in the current folder.
scriptDir = fileparts(mfilename('fullpath'));
if ~isempty(scriptDir) && isfile(fullfile(scriptDir, filename))
    filename = fullfile(scriptDir, filename);
elseif ~isfile(filename)
    [f, p] = uigetfile('*.csv', 'Select Commute Time.csv');
    if isequal(f, 0)
        error('No CSV selected. Unzip the file and pick "Commute Time.csv".');
    end
    filename = fullfile(p, f);
end
fprintf('Reading: %s\n', filename);

opts = detectImportOptions(filename, 'VariableNamingRule', 'preserve');
opts = setvartype(opts, {'Travel Time','Place','Place ID'}, 'string');
T = readtable(filename, opts);

% Rename columns to valid MATLAB names that are easier to type
T.Properties.VariableNames = {'TimeID','TravelTime','Year','Commuters', ...
                              'MOE','Place','PlaceID','Share'};

% If the file ever has more than one year, use the most recent one
yearsInFile = unique(T.Year);
yr = max(yearsInFile);
if numel(yearsInFile) > 1
    fprintf('File has %d years; using the most recent (%d).\n', numel(yearsInFile), yr);
end
T = T(T.Year == yr, :);

disp('Imported table:');
disp(T);

%% 2) Reshape into matrices (rows = travel-time ranges, columns = places)
places  = unique(T.Place, 'stable');     % e.g. "United States", "Cuba, NM"
timeIDs = unique(T.TimeID);              % 0 ... 11
nP = numel(places);
nB = numel(timeIDs);

binNames  = strings(nB, 1);
Commuters = zeros(nB, nP);
MOE       = zeros(nB, nP);
Share     = zeros(nB, nP);

for b = 1:nB
    binNames(b) = T.TravelTime(find(T.TimeID == timeIDs(b), 1));
end
for p = 1:nP
    rows = (T.Place == places(p));
    [~, bi] = ismember(T.TimeID(rows), timeIDs);
    Commuters(bi, p) = T.Commuters(rows);
    MOE(bi, p)       = T.MOE(rows);
    Share(bi, p)     = T.Share(rows);
end

% Travel-time labels in the right order (not alphabetical)
binCats = categorical(binNames, binNames);

% Wide table: one row per travel-time range, % share for each place
ShareTable = array2table(100 * Share, ...
    'VariableNames', matlab.lang.makeValidName(cellstr(places + "_Pct")));
ShareTable = addvars(ShareTable, binNames, 'Before', 1, 'NewVariableNames', 'TravelTime');
fprintf('\nShare of commuters (%%) by travel time, %d:\n', yr);
disp(ShareTable);

%% 3) Estimated average commute time for each place
% The data only gives ranges, so each range is represented by its midpoint.
% "90+ Minutes" has no upper limit, so 100 minutes is ASSUMED for it.
midpoints = [2.5 7 12 17 22 27 32 37 42 52 74.5 100]';
if numel(midpoints) ~= nB
    error('Expected 12 travel-time ranges; update the midpoints list to match the data.');
end

TotalCommuters = sum(Commuters, 1);
AvgMinutes     = (midpoints' * Commuters) ./ TotalCommuters;

SummaryTable = table(places, TotalCommuters', AvgMinutes', ...
    'VariableNames', {'Place','TotalCommuters','EstAvgMinutes'});
fprintf('Summary, %d:\n', yr);
disp(SummaryTable);

%% 4) Group the 12 ranges into 5 broader categories
groupLabels = ["Under 15 min", "15-29 min", "30-44 min", "45-59 min", "60+ min"];
groupOf     = [1 1 1 2 2 2 3 3 3 4 5 5]';     % which group each range belongs to
GroupShare  = zeros(numel(groupLabels), nP);
for g = 1:numel(groupLabels)
    GroupShare(g, :) = sum(Share(groupOf == g, :), 1);
end
GroupTable = array2table(100 * GroupShare, ...
    'VariableNames', matlab.lang.makeValidName(cellstr(places + "_Pct")));
GroupTable = addvars(GroupTable, groupLabels', 'Before', 1, 'NewVariableNames', 'Group');
disp('Share of commuters (%) by broad group:');
disp(GroupTable);

%% 5) Bar graph: % of commuters in each travel-time range, places side by side
figure('Name', 'Commute Time Share by Place');
bar(binCats, 100 * Share, 'grouped');
grid on;
xlabel('Travel Time to Work');
ylabel('Share of Commuters (%)');
title(sprintf('Travel Time to Work, %d', yr));
legend(places, 'Location', 'northeast');

%% 6) Bar graph for each place: number of commuters with margin-of-error bars
for p = 1:nP
    figure('Name', "Commuters - " + places(p));
    x = 1:nB;
    bar(x, Commuters(:, p));
    hold on;
    errorbar(x, Commuters(:, p), min(MOE(:, p), Commuters(:, p)), MOE(:, p), ...
        'k.', 'LineWidth', 1, 'CapSize', 6);   % lower bar stops at 0
    hold off;
    grid on;
    xticks(x);
    xticklabels(binNames);
    xtickangle(45);
    xlabel('Travel Time to Work');
    ylabel('Number of Commuters');
    title(sprintf('%s: Commuters by Travel Time, %d (error bars = MOE)', places(p), yr));
end

%% 7) Bar graph: broad groups, places side by side, with % labels
figure('Name', 'Commute Time - Broad Groups');
bg = bar(categorical(groupLabels, groupLabels), 100 * GroupShare, 'grouped');
grid on;
ylabel('Share of Commuters (%)');
title(sprintf('Commute Time by Broad Group, %d', yr));
legend(places, 'Location', 'northeast');
for p = 1:nP
    text(bg(p).XEndPoints, bg(p).YEndPoints, compose('%.1f%%', 100 * GroupShare(:, p)), ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', 'FontSize', 8);
end

%% 8) Line plot: cumulative share (what % of people get to work within X minutes)
figure('Name', 'Cumulative Commute Time');
plot(1:nB, 100 * cumsum(Share, 1), '-o', 'LineWidth', 1.5);
grid on;
xticks(1:nB);
xticklabels(binNames);
xtickangle(45);
xlabel('Travel Time to Work (up to and including this range)');
ylabel('Cumulative Share of Commuters (%)');
title(sprintf('Cumulative Commute Time, %d', yr));
legend(places, 'Location', 'southeast');
ylim([0 100]);

%% 9) Bar graph: estimated average commute time
figure('Name', 'Estimated Average Commute');
ba = bar(categorical(places, places), AvgMinutes);
grid on;
ylabel('Estimated Average Commute (minutes)');
title(sprintf('Estimated Average Commute Time, %d', yr));
text(ba.XEndPoints, ba.YEndPoints, compose('%.1f min', AvgMinutes), ...
    'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');

%% 10) Save everything to a .mat file for later use
save(fullfile(fileparts(filename), 'commute_time_data.mat'), ...
    'T', 'yr', 'places', 'binNames', 'Commuters', 'MOE', 'Share', ...
    'ShareTable', 'SummaryTable', 'GroupTable', 'AvgMinutes');

fprintf('\nSaved variables to commute_time_data.mat\n');