if [[ "$#" != "2" ]]
then
    echo 'usage:'
    echo '    bash download.sh gag_id image_url'
    exit
fi

gag_id=$1
image_url=$2

rm -f images/$gag_id.*
wget -q -O images/$gag_id $image_url 2>&1 > /dev/null
desc=`file images/$gag_id`
if [[ "$desc" =~ "GIF" ]]
then
    convert images/$gag_id[0] images/$gag_id.jpg
    rm -f images/$gag_id
elif [[ "$desc" =~ "JPEG" ]]
then
    mv images/$gag_id images/$gag_id.jpg
fi

