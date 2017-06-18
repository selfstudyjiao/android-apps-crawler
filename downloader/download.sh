if [ $# -ge 4 ]
then
    echo "Usage: $0 <"databse IP:PORT"> <"databsename:docname"> [output directory]"
    exit 2
fi

if [ $# -eq 0 ]; then
    ./downloader.py "127.0.0.1:27017" "GPLAY:Apps" "../repo/apps"
elif [ $# -eq 1 ]; then
    ./downloader.py $1 "GPLAY:Apps" "../repo/apps"
elif [ $# -eq 2 ]; then
    ./downloader.py $1 $2 "../repo/apps"
else
    ./downloader.py $1 $2 $3
fi
