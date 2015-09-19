f1 = imread('thumb1.bmp');
f2 = imread('thumb2.bmp');

f2crop = imcrop(f2);
figure, imshowpair(f1, f2crop, 'montage')
title('Unregistered')
[optimizer,metric] = imregconfig('monomodal');

%tformSimilarity = imregtform(f1,f2,'similarity',optimizer,metric);

%optimizer.InitialRadius = optimizer.InitialRadius/3.5;
optimizer.MaximumIterations = 300;
optimizer.MinimumStepLength = 1e-6;
optimizer.RelaxationFactor = 0.95;

combined = imregister(f2crop, f1, 'rigid', optimizer, metric);
figure, imshowpair(combined, f1)
title('A: Default registration')

disp(optimizer)
disp(metric)