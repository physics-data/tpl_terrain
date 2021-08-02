#!/bin/bash

BN=$(dirname $(readlink -f $0))
cd $BN

rm *.tif
rm checksums.sha256

wget https://lab.cs.tsinghua.edu.cn/physics-data/terrain/terrain.tif
wget https://lab.cs.tsinghua.edu.cn/physics-data/terrain/checksums.sha256

sha256sum -c checksums.sha256

if [[ $? != 0 ]]; then
  echo "Checksum failed. Please run this script again."
fi
