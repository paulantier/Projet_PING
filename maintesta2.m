
close all; clear all; %Nettoyage du plan de travail

%Initialisation générale
nb_images=6372; %Définition du nombre d'images de la base à traiter

%Initialisation masque
temp_casserole=55; %Définition de la température max d'analyse avant
% laquelle on considère qu'un point est un élément solide de casserolle
bornemask=(temp_casserole+183)/0.007; %Equivalent en intensité de pixel
%de la température definie ci dessus
vide = logical(zeros(120,160));


% Traitement
for w=1:nb_images %Pour chaque image de la base
    nomIm=sprintf("%d.png",w);
    I1=uint16(imread(nomIm));
    I2(:,:)=256*uint16(I1(:,:,1)) + uint16(I1(:,:,2)); %On la convertit
    %depuis son format 2 fois 8bit pour obtenir l'image 16 bits

    if w>1
        mask(:,:) = I2(:,:)>bornemask; %On initialise un masque des points 
        %très chauds de l'image dans le but de détecter la présence ou non
        %d'une casserole
        casseroles = bwareaopen(mask,40); %On filtre des possibles points
        %chauds mais trop petit pour être des casseroles

        %On cherche maintenant à déterminer une zone d'intérêt qui sera la
        %zone d'air au dessus de la casserole détectée :
        %Pour ce faire on définit une zone d'encadrement de la casserole
        % dans les deux coordonnées de l'image.
        
        %On initialise les valeurs des maximums avant de faire des calculs
        %pixel par pixel
        min_i=120;
        min_j=160;
        max_i=0;
        max_j=0;
        for j=1:160 %Pour tout pixel de chaque image
            for i=1:120
                if casseroles(i,j)==1
                    max_i=max(i,max_i);
                    max_j=max(j,max_j);
                    min_i=min(i,min_i);
                    min_j=min(j,min_j);
                    if max_j == j
                        imax_j=i; %On note la coordonnée i de la matrice 
                    end           %pour laquelle j est maximale
                    if min_j == j %de même avec j minimale
                        imin_j=i;
                    end
                end
            end
        end

        mask2 = logical(zeros(120,160)); %On initialise ici deux masques
        %qui réprésenteront respectivement la zone carrée au dessus de la
        %casserole et la zone en dessous de la casserole qui ne nous
        %intéresse pas dans l'encadrement.
        mask3 = logical(zeros(120,160));
        ffbord=max(1,min_i-70); %Précaution pour éviter des problèmes d'indices aux bords
        mask2(ffbord:max_i,min_j:max_j)=1;
        mask3(min(imax_j,imin_j):120,min_j:max_j)=1;
        mask4 = max(vide,mask2-mask3); %le masque 4 permet de travailler avec
        %une matrice booléenne.
        maskfinal(:,:) = (mask4(:,:) & ~(casseroles(:,:)==1));

        I4 = uint8(min((I2 - I3),255)); %On calcule la soustraction de notre matrice
        % à l'instant t moins celle à l'instant t-1.
        I5 = imbinarize(I4,0.15); %On effectue un seuillage global pour convertir en binaire cette image
        I6 = bwareaopen(I5,10); %On utilise une opération morphologique pour supprimer les tas de pixels bruités
        % (bwareaopen permet de supprimer les zones de pixels ayant une
        % aire inférieure à une constante
        I7 = I5 - I6; %I7 contient la position des pixels bruités
        I4(I7==1)=0; %Que l'on supprime ensuite sur notre image de soustraction
        I8 = imbinarize(I4,0.1); %On réeffectue la même opération avec un seuil binaire différent
        I9 = bwareaopen(I8,5);
        I10 = I8 - I9;
        I4(I10==1)=0;
        I11 = imbinarize(I4,0.05); %On refait un dernière seuillage binaire pour enlever les pixels de valeur négligeable
        I12= I11-I8; 
        I4(I12==1)=0;
        I4(I11==0)=0;
        I4(maskfinal==0)=0;
        nomRes=sprintf("resultats/%d.png",w);
        imwrite(I4, nomRes);
    end
    
    I3=I2;

end

run("moviemaker.m")

