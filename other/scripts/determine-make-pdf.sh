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
  WKHTMLTOPDF="wkhtmltopdf --page-size A3 --orientation Landscape"
  DISPLAY=:$DISP $WKHTMLTOPDF $1 $2
}


while getopts s:d opt
do
    case "$opt" in
      d)  DEBUG="YES";;
      s)  SITE_URL="$OPTARG";;
      
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

get_html $REPORT_STYLE $REPORT_XML $TMP_REPORT_HTML
html_pdf $TMP_REPORT_HTML $TMP_REPORT_PDF

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

pdftk $PDFS cat output $OUTPUT

kill_xvfb
clean_up
