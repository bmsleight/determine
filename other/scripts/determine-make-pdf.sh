#!/bin/bash
#

full_path ()
{
 BASENAME=$(basename "${1}")
 DIRNAME=$(cd $(dirname "${1}") && pwd)
 FULL_PATH="${DIRNAME}/${BASENAME}"
}

get_global_variables ()
{
 TMP_REPORT_HTML=$(tempfile --prefix=determine --suffix=.html)
 TMP_REPORT_PDF=$(tempfile --prefix=determine --suffix=.pdf)
 TMP_SITE_PDF=$(tempfile --prefix=determine --suffix=.pdf)
 TMP_DEBUG_PS=$(tempfile --prefix=determine --suffix=.html)
 TMP_DEBUG_HTML=$(tempfile --prefix=determine --suffix=.html)
 TMP_DEBUG_PDF=$(tempfile --prefix=determine --suffix=.pdf) 
 TMP_BACKGROUND_HTML=$(tempfile --prefix=determine --suffix=.html)
 TMP_BACKGROUND_PDF=$(tempfile --prefix=determine --suffix=.pdf)
 TMP_BACKGROUND_DIR=$(mktemp -d)
 TMP_PDF_NO_BACK=$(tempfile --prefix=determine --suffix=.html)
 PDFS="$TMP_REPORT_PDF "
}

clean_up ()
{
  rm $TMP_REPORT_HTML
  rm $TMP_REPORT_PDF
  rm $TMP_SITE_PDF
  rm $TMP_DEBUG_PS
  rm $TMP_DEBUG_HTML
  rm $TMP_DEBUG_PDF
  rm $TMP_BACKGROUND_HTML
  rm $TMP_BACKGROUND_PDF
  rm $TMP_BACKGROUND_DIR -R
  rm $TMP_PDF_NO_BACK
}

launch_xvfb ()
{
  DISP=$RANDOM let "DISP %= 500";
  while [ -f /tmp/.X${DISP}-lock ]; do 
	  DISP=$RANDOM let "DISP %= 500";
  done;
  XAUTHORITY=$(tempfile);
  XPID=$(tempfile)
  Xvfb -kb -screen 0 1024x768x24 -dpi 96 -terminate -auth $XAUTHORITY  \
    -nolisten tcp :$DISP >/dev/null 2>&1 & echo $! > $XPID
}

kill_xvfb ()
{
#  PID=$(cat $XPID)
#  kill $PID 
  killall Xvfb
  rm $XAUTHORITY
  rm $XPID
}

get_html ()
{
  xmlstarlet tr $1 $2 >$3
}

html_pdf ()
{
  launch_xvfb
  WKHTMLTOPDF="wkhtmltopdf --margin-top 15 --margin-bottom 15  --page-size A3 --orientation Landscape"
  DISPLAY=:$DISP $WKHTMLTOPDF $1 $2
}


background_html ()
{
echo boo
cat >$TMP_BACKGROUND_HTML <<EOF
<html>
<p align="right"><font size=3><img src="http://www.determine.org.uk/site_media/images/determine-logo.png" width=150></font></p>
</html>
EOF
}

make_background ()
{
  PAGES=$(pdftk $1 dump_data | grep "NumberOfPages" | cut -d\   -f 2)
  PAGES_HTML=" "
  for i in `seq 1 $PAGES`
  do
     PAGES_HTML="$PAGES_HTML $TMP_BACKGROUND_HTML "
  done
  launch_xvfb
  NOW=$(date +"Created: %F %H:%M:%S")
  VERSION=$(svn info | grep Revision | cut -d\  -f 2)
  DISPLAY=:$DISP wkhtmltopdf --page-size A3 --orientation Landscape \
  --margin-top 1 --margin-right 2 --margin-bottom 5   --margin-left 2 \
  --footer-font-size 8  \
  --footer-center "[page] of [topage]" \
  --footer-right "www.determine.org.uk" \
  --footer-left "$NOW, using Determine version: $VERSION" \
  $PAGES_HTML $TMP_BACKGROUND_PDF
  
  # Yes this is terriable code. Its really bad.
  # I feel bad even writing comments about it
  # The Shame....
  cd $TMP_BACKGROUND_DIR
  pdftk $TMP_BACKGROUND_PDF  burst output p_%04d.pdf
  pdftk $1  burst output b_p_%04d.pdf
for i in $(ls p_*.pdf);
do
        echo processing page $i...
        pdftk $i background b_$i output x_$i.pdf
done
pdftk x_p_*.pdf cat output $OUTPUT
 cd /tmp/
  # I am still Hiding....
  # Please fix the above. 
}


while getopts s:dh opt
do
    case "$opt" in
      d)  DEBUG="YES";;
      s)  SITE_URL="$OPTARG";;
      h)  HTML_SKIP="YES";;
      
      \?)		# unknown flag
      	  echo >&2 \
		"usage: $0 [-s site_url] [-d] report.xml report_style.xml output.pdf" 
	  exit 1;;
    esac
done
shift `expr $OPTIND - 1`

#Confirm parameters
if [ -z "$1" -a -z "$2" -a -z "$3" ]; then
    echo "usage: $0 [-s site_url] [-d] report.xml report_style.xml output.pdf" 
    echo
    echo " This script takes the input makes the pdf"
    exit
fi

full_path $1
REPORT_XML=$FULL_PATH
full_path $2
REPORT_STYLE=$FULL_PATH
full_path $3
OUTPUT=$FULL_PATH

get_global_variables
launch_xvfb

if [ "$HTML_SKIP" != "YES" ]; then
  get_html $REPORT_STYLE $REPORT_XML $TMP_REPORT_HTML
  html_pdf $TMP_REPORT_HTML $TMP_REPORT_PDF
else 
  html_pdf $REPORT_XML $TMP_REPORT_PDF
fi

if [ "$SITE_URL" != "" ]; then
  html_pdf $SITE_URL $TMP_SITE_PDF
  PDFS="$PDFS $TMP_SITE_PDF "
fi

if [ "$DEBUG" == "YES" ]; then
  enscript -5 -p $TMP_DEBUG_PS -b "Full Details of Movements" \
  --font=Courier6 --highlight=html --landscape --color \
  --borders --media=A3 --title="XML" \
  --header='$n||Page $% of $=' $REPORT_XML
  ps2pdf $TMP_DEBUG_PS $TMP_DEBUG_PDF
  PDFS="$PDFS $TMP_DEBUG_PDF "
fi

# Combine all pages requested into a single PDF
pdftk $PDFS cat output $TMP_PDF_NO_BACK
#$OUTPUT

background_html
make_background $TMP_PDF_NO_BACK

kill_xvfb
clean_up
