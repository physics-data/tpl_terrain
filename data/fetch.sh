#!/bin/bash

BN=$(dirname $(readlink -f $0))
cd $BN

rm *.tif
rm checksums.sha256

wget https://lab.cs.tsinghua.edu.cn/physics-data/terrain/dataset.tar.gz -O - | tar -xzf - .
sha256sum -c checksums.sha256

if [[ $? != 0 ]]; then
  echo "Checksum failed. Please run this script again."
fi
