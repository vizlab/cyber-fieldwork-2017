function X = adv_dif_2d(Usegpu, mesh_size, t)
%% ����һ�E
% Usegpu : GPU�����ä��뤫��0, 1���뤨��
% mesh_size : Ӌ���I���mesh_size x mesh_size�Ƿָ�
% t : Ӌ�㤵����r�g��1��Ԫ���Ф��뤨��

%% �ѥ��`���O��
D = 1e-3; % ��ɢ�S��
u = 0.15; % x������ٶ�
v = 0.02; % y������ٶ�

lx = 1.0; % Ӌ���I���ȫ�L (x)
ly = 1.0; % Ӌ���I���ȫ�L (y)
[x, y] = meshgrid(linspace(0, lx, mesh_size), linspace(0, ly, mesh_size)); % ���˥ޥåפ�����
dx = x(1, 2) - x(1, 1); % 1�ޥ��g�ξ��x��Ӌ�� (x)
dy = y(2, 1) - y(1, 1); % 1�ޥ��g�ξ��x��Ӌ�� (y)
dt = t(2)-t(1); % 1���ƥåפ�����Εr�g�g����Ӌ��

%% GPUʹ��?��ʹ�ä�Q��
if(Usegpu>=1)
    disp(['Use GPU']);
    gpu = gpuDevice;
    F = gpuArray(double(((x-0.3).^2+(y-0.3).^2)<=0.1^2)); % ����������(0.3, 0.3)�����ĤȤ����뾶0.1�΃Ҥ��ڲ���1�ˤʤ�褦��ָ��
    rows = gpuArray.colon(1, mesh_size)';
    cols = gpuArray.colon(1, mesh_size);
else
    disp(['Do not use GPU']);
    F = double(((x-0.3).^2+(y-0.3).^2)<=0.1^2); % ����������(0.3, 0.3)�����ĤȤ����뾶0.1�΃Ҥ��ڲ���1�ˤʤ�褦��ָ��
    rows = [1:mesh_size];
    cols = [1:mesh_size];
    [cols, rows] = meshgrid(cols, rows);
end
disp(['mesh_size : ' num2str(mesh_size) ' x ' num2str(mesh_size)]);

%% �v�����x
    function fn = mystencil(row, col)
        % �������ҤΥ���ǥå�����Ӌ��
        up = row+1;
        down = row-1;
        left = col-1;
        right = col+1;
        
        % Ӌ���I�������Ӌ��
        if((row == 1)||(row==mesh_size)||(col==1)||(col==mesh_size))
            fn = 0;
        else
            % ��ɢ� (2�ξ������Ĳ�ַ�)
            Dx = D*(F(row, left) - 2*F(row, col) +  F(row, right))/(dx^2);
            Dy = D*(F(down, col) - 2*F(row, col) +  F(up, col))/(dy^2);
            
            % ����� (1�ξ����L�ϲ�ַ�)
            if(u>=0)
                fu = u*(F(row, col) - F(row, left))/dx;
            else
                fu = u*(F(row, right) - F(row, col))/dx;
            end
            if(v>=0)
                fv = v*(F(row, col) - F(down, col))/dy;
            else
                fv = v*(F(up, col) - F(row, col))/dy;
            end
            
            % ���åץǩ`��
            fn = F(row, col) + (Dx + Dy - (fu + fv))*dt;
        end        
    end

    function fn = boundary(row, col)
        % ����΄I��
        if(row == 1)
            fn = Ft(mesh_size-1, col);
        elseif(row == mesh_size)
            fn = Ft(2, col);
        else
            if(col == 1)
                fn = Ft(row, mesh_size-1);
            elseif(col == mesh_size)
                fn = Ft(row, 2);
            else
                fn = Ft(row, col);
            end            
        end
    end

%% �ᥤ��I��
timer = tic();
X(:,:,1) = double(((x-0.3).^2+(y-0.3).^2)<=0.2^2);
for i = 2:length(t)
    Ft = arrayfun(@mystencil, rows, cols);
    if(Usegpu>=1)
        wait(gpu);
    end
    Fn = arrayfun(@boundary, rows, cols);
    if(Usegpu>=1)
        wait(gpu);
        X(:,:,i) = gather(Fn);
    else
        X(:,:,i) ;
    end
    F = Fn;
end
toc(timer)
end