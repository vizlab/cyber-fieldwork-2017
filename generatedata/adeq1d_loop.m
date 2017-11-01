function adeq1d_loop(n,dt,loop,D)
% 移流拡散方程式（１次元、非定常、陽解法）
%  n: 節点の数
%  dt: 時間の刻み幅
%  loop: 全ステップ数
d = 5.0; % １辺の長さ
cf = 200.0; % 発生量
ck = 1.0; % 拡散係数
cv = -3.0; % 流速
% % d = 1.5; % １辺の長さ
% % cf = 1.0*10; % 発生量
% % ck = 0.1; % 拡散係数
% % cv = 1.0; % 流速

h = d/(n - 1); % x方向の刻み幅

x = linspace(0,d,n); % 節点の位置

u = zeros(n,1); % 初期値
% % u(1,1) = 1; % 初期値
f = zeros(n,1);
ic = round(n/2); % 真ん中付近の節点番号
f(ic) = cf; % 真ん中付近でのみ発生
% % f(2) = cf; % 右付近でのみ発生

for k=1:loop
    u = adeq1d(u,n,dt,ck,cv,h,f);
    plot(x,u)
    axis([0 d 0 5])
% %     axis([0 d 0 1])
    pause(dt)
    
%     % 1ステップ目にのみ発生させる場合は
%     % 以下のコメントを外す
%     if k == 1
%         f(ic) = 0.0;
%     end
end

return
end


function u = adeq1d(u0,n,dt,ck,cv,h,f)
% １ステップのみ進める

c1 = ck*dt/h^2;
c2 = cv*dt/(2*h);
u = zeros(n,1); % 初期化
for i=2:n-1
  u(i) = (1 - 2*c1)*u0(i) ...
      + (c1 + c2)*u0(i-1) ...
      + (c1 - c2)*u0(i+1) ...
      + dt*f(i);
end

return
end