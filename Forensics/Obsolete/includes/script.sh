res=""
while read -r line; do
    if [ ! -z "$(echo $line | grep TCP)" ]
    then
        res+='_'
    elif [ ! -z "$(echo $line | grep UDP)" ]
    then
        res+='.'
    else
        res+=' '
    fi
done <<< "$(tshark -r ./network.pcapng)"
echo $res
