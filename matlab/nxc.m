% get cross-correlation with small chunk

% load images
f1 = imread('thumb1.bmp');
f2 = imread('thumb2.bmp');

% crop
f2crop = f2;%imcrop(f2);
%figure, imshowpair(f1, f2crop, 'montage');

% compute cross-correlation
xc = normxcorr2(f2crop, f1);
figure, imagesc(xc .^ 5), colormap jet

% Find maximum, compute transform coords
[maxA,ind] = max(xc(:));
[x,y] = ind2sub(size(xc),ind);

% actually do the transform
f2_aligned = zeros(size(f1));
[n, m] = size(f2crop);
f2_aligned(x - n : x - 1, y - m : y - 1) = f2crop(:, :);

imshowpair(f2_aligned, f1)