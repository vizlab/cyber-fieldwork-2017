function X = adv_dif_2d(Usegpu, mesh_size, t)
%% 引数一覧
% Usegpu : GPUを利用するかを0, 1で与える
% mesh_size : 計算領域をmesh_size x mesh_sizeで分割
% t : 計算させる時間を1次元配列で与える

%% パラメータ設定
D = 1e-3; % 拡散係数
u = 0.15; % x方向の速度
v = 0.02; % y方向の速度

lx = 1.0; % 計算領域の全長 (x)
ly = 1.0; % 計算領域の全長 (y)
[x, y] = meshgrid(linspace(0, lx, mesh_size), linspace(0, ly, mesh_size)); % 座標マップを作成
dx = x(1, 2) - x(1, 1); % 1マス間の距離を計算 (x)
dy = y(2, 1) - y(1, 1); % 1マス間の距離を計算 (y)
dt = t(2)-t(1); % 1ステップあたりの時間間隔を計算

%% GPU使用?不使用を決定
if(Usegpu>=1)
    disp(['Use GPU']);
    gpu = gpuDevice;
    F = gpuArray(double(((x-0.3).^2+(y-0.3).^2)<=0.1^2)); % 初期条件は(0.3, 0.3)を中心とした半径0.1の円の内部が1になるように指定
    rows = gpuArray.colon(1, mesh_size)';
    cols = gpuArray.colon(1, mesh_size);
else
    disp(['Do not use GPU']);
    F = double(((x-0.3).^2+(y-0.3).^2)<=0.1^2); % 初期条件は(0.3, 0.3)を中心とした半径0.1の円の内部が1になるように指定
    rows = [1:mesh_size];
    cols = [1:mesh_size];
    [cols, rows] = meshgrid(cols, rows);
end
disp(['mesh_size : ' num2str(mesh_size) ' x ' num2str(mesh_size)]);

%% 関数定義
    function fn = mystencil(row, col)
        % 上下左右のインデックスを計算
        up = row+1;
        down = row-1;
        left = col-1;
        right = col+1;
        
        % 計算領域だけを計算
        if((row == 1)||(row==mesh_size)||(col==1)||(col==mesh_size))
            fn = 0;
        else
            % 拡散項 (2次精度中心差分法)
            Dx = D*(F(row, left) - 2*F(row, col) +  F(row, right))/(dx^2);
            Dy = D*(F(down, col) - 2*F(row, col) +  F(up, col))/(dy^2);
            
            % 移流項 (1次精度風上差分法)
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
            
            % アップデート
            fn = F(row, col) + (Dx + Dy - (fu + fv))*dt;
        end        
    end

    function fn = boundary(row, col)
        % 境界の処理
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

%% メイン処理
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