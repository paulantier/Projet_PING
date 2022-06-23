
close all;

froid=38;
chaud=50;
nb_images=1000;
chargement=0;
f= waitbar(0,"Progression...");

for w=1:nb_images
    nomIm=sprintf("%d.png",w);
    I1=uint16(imread(nomIm));
    [a,b,c]=size(I1);
    I2=uint16(zeros(a,b));
    I2(:,:)=I1(:,:,1)*256+I1(:,:,2);
    chargement=chargement+1;
    waitbar(chargement/(nb_images-1),f,"Progression...");
    nomRes=sprintf("resultats/%d.png",w);
    imwrite(I2, nomRes) 

end

close(f);
delete(f);