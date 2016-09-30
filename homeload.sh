#!/bin/bash
USER=$1
SERVER=www.homeloadtv.com
API="/api/?do"

function setListState {
    curl "http://$SERVER$API=setstate&uid=$USER&list=$1&state=$2"
}

function setLinkState {
    curl "http://$SERVER$API=setstate&uid=$USER&id=$1&state=$2"
}

function getListID {
    for cmd in $(echo -n $1 | tr ";" " " ) 
    do  
        eval $cmd
    done
    echo $LIST
}

cd /media/Bananas/Video/OTR


# get list from URL using curl
# remove DOS line breaks
# read line-wise
#
# Example:
#
#INTERVAL=60;NUMBER_OF_LINKS=1;LIST=2;LINKCOUNT=1;HHSTART=0;HHEND=8;
#http://81.95.11.39/download/2069180/1/12214227/d70ca628178a09308493fe3f16372c41/de/Aktenzeichen_XY____ungeloest_16.06.08_20-15_zdf_90_TVOON_DE.mpg.HD.cut.mp4;14358165;
#
curl -s "http://$SERVER$API=getlinks&uid=$USER" | tr -d "\r" | while read line
do
    if [ -z "$listID" ]
    then
        listID=$(getListID $line)
        setListState $listID processing
        continue
    fi
    
    url=${line%%\;*}
    id=${line##*;}

    curl -O $line
    
    setLinkState $id finished
done
