function id = cross_corr_tester()
% given the knowledge that the most recently created image in C:/images is
% a fingerprint to be identified, return its id.

% possibly delay

% find name of most recent image in C/images
%d=dir('C:\Images\');
d=dir('*.bmp');
[dx,dx] = sort([d.datenum],'descend');
newest = d(dx(1)).name

% load it as an image
needle = imread(newest);

% load all images to compare it against
d = dir('*.bmp');
correlations = zeros(length(d), 1);
for i = (1:length(d))
    hay = imread(d(i).name);
    % compare against images
    correlations(i) = nxc_applied(hay, needle);
end
    
% find number to return.
best = 5.0;
bestIndex = 0;
for i = (1 : length(correlations))
    if correlations(i) > best
        best = correlations(i);
        bestIndex = i;
    end
end 

% delete the file.
delete(newest);

% return
id = bestIndex;
end