function adeq1d_loop(n,dt,loop,D)
% ������ɢ����ʽ������Ԫ���Ƕ�����ꖽⷨ��
%  n: �������
%  dt: �r�g�ο̤߷�
%  loop: ȫ���ƥå���
d = 5.0; % ���x���L��
cf = 200.0; % �k����
ck = 1.0; % ��ɢ�S��
cv = -3.0; % ����
% % d = 1.5; % ���x���L��
% % cf = 1.0*10; % �k����
% % ck = 0.1; % ��ɢ�S��
% % cv = 1.0; % ����

h = d/(n - 1); % x����ο̤߷�

x = linspace(0,d,n); % �����λ��

u = zeros(n,1); % ���ڂ�
% % u(1,1) = 1; % ���ڂ�
f = zeros(n,1);
ic = round(n/2); % ����и����ι��㷬��
f(ic) = cf; % ����и����ǤΤ߰k��
% % f(2) = cf; % �Ҹ����ǤΤ߰k��

for k=1:loop
    u = adeq1d(u,n,dt,ck,cv,h,f);
    plot(x,u)
    axis([0 d 0 5])
% %     axis([0 d 0 1])
    pause(dt)
    
%     % 1���ƥå�Ŀ�ˤΤ߰k����������Ϥ�
%     % ���¤Υ����Ȥ��⤹
%     if k == 1
%         f(ic) = 0.0;
%     end
end

return
end


function u = adeq1d(u0,n,dt,ck,cv,h,f)
% �����ƥåפΤ��M���

c1 = ck*dt/h^2;
c2 = cv*dt/(2*h);
u = zeros(n,1); % ���ڻ�
for i=2:n-1
  u(i) = (1 - 2*c1)*u0(i) ...
      + (c1 + c2)*u0(i-1) ...
      + (c1 - c2)*u0(i+1) ...
      + dt*f(i);
end

return
end