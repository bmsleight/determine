convert -size 1180x250 xc:transparent -font URWPalladioL-Bold -pointsize 240 \
   -fill black  -draw \
   "fill black text 20,220 'determine'  rectangle 290,25   363,160
    fill red circle 327,63 327,83
    fill DarkOrange circle 327,121 327,141
    fill white  rectangle  810,60  855,90" \
    -transparent white \
    -draw "fill Green circle 835,63 835,83" \
   ../../django/determine/site_media/images/determine-v001-large.png


convert ../../django/determine/site_media/images/determine-v001-large.png -resize 800x   ../../django/determine/site_media/images/determine-logo.png
#convert -size 700x148 xc:white ../../django/determine/site_media/images/determine-v001-large.png -resize 700x  -composite ../../django/determine/site_media/images/determine-logo-header.png
convert ../../django/determine/site_media/images/determine-v001-large.png -resize 100x ../../django/determine/site_media/images/determine-logo-small.png
convert ../../django/determine/site_media/images/determine-v001-large.png -crop 100x250+276+0 ../../django/determine/site_media/images/determine-t.png 
convert ../../django/determine/site_media/images/determine-v001-large.png -crop 100x250+276+0 -resize 32x ../../django/determine/site_media/images/determine-t-small.png 
convert ../../django/determine/site_media/images/determine-t.png -resize 32x32\> -size 32x32 xc:white +swap -gravity center  -composite ../../django/determine/site_media/images/favicon.png
convert -size 16x16 xc:transparent -draw "fill DarkOrange circle 8,8 10,10" ../../django/determine/site_media/images/bullet.png

