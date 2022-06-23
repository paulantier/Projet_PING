close all;

for w = 1600:1605
    nomIm = sprintf("%d.png", w);
    I = uint16(imread(nomIm));
    [a, b, c] = size(I);
    I2 = double(zeros(a, b, 3));
    temp_map = double(zeros(a, b));

    for i=1:a
        for j=1:b
            temp = double((I(i, j, 1)*256 + I(i, j, 2)))*0.007 - 183;
            temp_map(i, j) = temp;
        end
    end

    %nomRes = sprintf("resultats_temp/%d.png", w);
    %temp_map_double = temp_map;
    %temp_map = uint8(temp_map*255/140);
    %imwrite(temp_map, nomRes) 
    figure(),
    imshow(temp_map,[]);
end

%run("moviemaker_temp.m")