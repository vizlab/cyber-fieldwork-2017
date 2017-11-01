
X = adv_dif_2d(0, 50, (0:0.01:5));
t= 0:0.01:5;
for i = 1:length(t)
surf(X(:,:,i));
zlim([0 1]);
caxis([0 1]);
drawnow;
pause(0.01);
end