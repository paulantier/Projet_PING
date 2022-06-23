
close all;

froid=38;
chaud=50;
nb_images=1000;
chargement=0;
f= waitbar(0,"Progression...");

for w=1:nb_images
    nomIm=sprintf("%d.png",w);
    I=uint16(imread(nomIm));
    [a,b,c]=size(I);
    I2=double(zeros(a,b,3));
    for i=1:a
        for j=1:b
            temp=(double(I(i,j,1))*256+double(I(i,j,2)))*0.007-183;
            if temp < froid
                I2(i,j,3)=froid;
            elseif temp > chaud
                I2(i,j,1)=chaud;
            else
                I2(i,j,2)=temp;
            end
        end
    end
    chargement=chargement+1;
    waitbar(chargement/(nb_images-1),f,"Progression...");
    nomRes=sprintf("resultats/%d.png",w);
    imwrite(I2, nomRes) 

end

close(f);