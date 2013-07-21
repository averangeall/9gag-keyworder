if [[ "$#" != "2" ]]
then
    echo 'usage:'
    echo '    bash download.sh gag_id image_url'
    exit 1
fi

gag_id=$1
image_url=$2

rm -f images/$gag_id.*
okay=false
while [[ "$okay" == "false" ]]
do
    if [ -e images/$gag_id.jpg ]
    then
        break
    fi
    wget -q -O "images/$gag_id" "$image_url"
    desc=`file images/$gag_id`
    if [[ "$desc" =~ "GIF" ]]
    then
        convert images/$gag_id[0] images/$gag_id.jpg
        rm -f images/$gag_id
        okay=true
    elif [[ "$desc" =~ "JPEG" ]]
    then
        mv images/$gag_id images/$gag_id.jpg
        okay=true
    fi
    sleep 1
done

exit 0

