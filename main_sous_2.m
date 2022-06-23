clc; clear all; close all;

max_intensity = 2^16;
froid = 37;
chaud = 40;
casserole = 40;
nblignes = 120;
nbcolonnes = 160;

% I3 = double(zeros(160, 120, 3));

for w = 2000:6372
    haut_casserole = ones(nbcolonnes, 1);
    haut_casserole = nblignes*haut_casserole;

    nomIm = sprintf("%d.png", w);
    I = uint16(imread(nomIm));
    I2 = double(zeros(nblignes, nbcolonnes, 3));

    for i=1:nblignes
        for j=1:nbcolonnes
            temp = double((I(i, j, 1)*256 + I(i, j, 2)))*0.007 - 183;

            if temp <= froid
                I2(i, j, 3) = max_intensity;

            elseif temp > chaud
                I2(i, j, 1) = max_intensity;

                if temp > casserole && i <= haut_casserole(j)
                    haut_casserole(j) = i;
                end

            else
                I2(i, j, 2) = 2^16;

            end
        end
    end


    I4 = I2;
    
    if w > 2000
        I2 = I2 - I3;
    end
    
    I3 = I4;
    
    nomRes = sprintf("resultats/%d.png", w);
    I2 = uint8(I2);

%     for bas=1:nblignes
%         for colonne=1:nbcolonnes
%             if bas > haut_casserole(colonne) || haut_casserole(colonne) == nblignes
%                 I2(bas, colonne, 1) = 0;
%                 I2(bas, colonne, 2) = 0;
%                 I2(bas, colonne, 3) = 0;
%             elseif bas < haut_casserole(colonne)-15
%                 I2(bas, colonne, 1) = 0;
%                 I2(bas, colonne, 2) = 0;
%                 I2(bas, colonne, 3) = 0;
%             end
%         end
%     end

    imwrite(I2, nomRes) 
end

run("moviemaker.m")