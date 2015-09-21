% get cross-correlation with small chunk

% load images
f1 = imread('imreg_1.bmp');
f2 = imread('imreg_2.bmp');

% crop
f2crop = f2;%imcrop(f2);
%figure, imshowpair(f1, f2crop, 'montage');

% compute cross-correlation
xc = normxcorr2(f2crop, f1);

% weight by distance from center
sigma = size(xc, 1) / 6;
center_weight = size(xc, 1) * size(xc, 2) * 5;
gauss = fspecial('gaussian', size(xc), sigma);
xc = xc .* (1 + center_weight * gauss);

figure, imagesc(xc .^ 3), colormap jet

% Find maximum, compute transform coords
[maxXC,ind] = max(xc(:));
maxXC
[x,y] = ind2sub(size(xc),ind);

% actually do the transform
f2_aligned = zeros(size(f1));
[n, m] = size(f2crop);
f2_aligned(x - n : x - 1, y - m : y - 1) = f2crop(:, :);

figure, imshowpair(f2_aligned, f1)

f2_trans = imtranslate(f2, [y-m, x-n], 'OutputView','full');
figure, imshowpair(f2_trans, f1)

[optimizer,metric] = imregconfig('monomodal');

optimizer.RelaxationFactor = 0.2;

combined = imregister(f2_trans, f1, 'rigid', optimizer, metric);
figure, imshowpair(combined, f1)
title('A: Default registration')