
nb_images=6372;
chargement=0;
f = waitbar(0,"Progression...");

video = VideoWriter('videofumeetest.avi');
video.Quality=100;
open(video);
for w=2000:nb_images
  I = im2uint8(imread(sprintf('resultats/%d.png',w)));
  writeVideo(video,I);
  writeVideo(video,I);
  chargement=chargement+1;
  waitbar(chargement/(nb_images-1),f,"Progression...");
end
close(video);
close(f);