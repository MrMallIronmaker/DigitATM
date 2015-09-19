% get cross-correlation with small chunk
function maxXC = nxc_applied(f1, f2)

% compute cross-correlation
xc = normxcorr2(f2, f1);
xc2 = normxcorr2(f1, f2);

%xcdiff = xc2 - rot90(xc,2);

% weight by distance from center
sigma = size(xc, 1) / 6;
center_weight = size(xc, 1) * size(xc, 2) * 5;
gauss = fspecial('gaussian', size(xc), sigma);
xc = xc .* (1 + center_weight * gauss);

figure, imagesc(xc .^ 3), colormap jet

% Find maximum, compute transform coords
[maxXC,ind] = max(xc(:));
end