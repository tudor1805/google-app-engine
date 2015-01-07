#!/bin/bash

set -e

client_libs_dir="$(pwd)/client_libs"

echo "Generating Client libraries..."

which endpointscfg.py &> /dev/null
if [ "$?" -ne 0 ] ; then
	echo "Looks like you don't have the Google SDK added to your PATH"
	exit 1
fi

endpointscfg.py get_client_lib java api.server.ServerApi

echo "Done generating Client libraries..."

mkdir -p "$client_libs_dir"
mv *.zip "$client_libs_dir"

