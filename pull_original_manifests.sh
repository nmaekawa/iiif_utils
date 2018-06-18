#!/usr/bin/env bash


input_file=$1
echo "processing file ${input_file}"

for uri in $(cat ${input_file})
do
    source=$(basename ${uri} | cut -d ':' -f 1)
    manifest_id=$(basename ${uri} | cut -d ':' -f 2)

    echo "got source(${source}) and id(${manifest_id})"

    if [ ${source} == 'huam' ]
    then
        echo "pulling from museums(${manifest_id})"
        curl https://iiif.harvardartmuseums.org/manifests/object/${manifest_id} > original_source/huam/${manifest_id}.json
    elif [ ${source} == 'drs' ]
    then
        echo "pulling from libraries(${manifest_id})"
        curl https://iiif.lib.harvard.edu/manifests/drs:${manifest_id} > original_source/drs/${manifest_id}.json
    else
        echo "unknown source (${source})"
    fi
done

echo "DONE!"
