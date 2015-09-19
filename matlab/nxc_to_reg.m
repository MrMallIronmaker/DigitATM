% get cross-correlation with small chunk

% load images
f1 = imread('thumb2.bmp');
f2 = imread('thumb1.bmp');

% crop
%f2crop = f2;%imcrop(f2);
%figure, imshowpair(f1, f2crop, 'montage');

% compute cross-correlation
xc = normxcorr2(f2crop, f1);
figure, imagesc(xc .^ 3), colormap jet

% Find maximum, compute transform coords
[maxA,ind] = max(xc(:));
[x,y] = ind2sub(size(xc),ind);

% actually do the transform
f2_aligned = zeros(size(f1));
[n, m] = size(f2crop);
f2_aligned(x - n : x - 1, y - m : y - 1) = f2crop(:, :);

figure, imshowpair(f2_aligned, f1)

f2_trans = imtranslate(f2, [y-m, x-n], 'OutputView','full', 'FillValues', 127);
figure, imshowpair(f2_trans, f1)

[optimizer,metric] = imregconfig('monomodal');

optimizer.RelaxationFactor = 0.2;

combined = imregister(f2_trans, f1, 'rigid', optimizer, metric);
figure, imshowpair(combined, f1)
title('A: Default registration')

disp(optimizer)
disp(metric)