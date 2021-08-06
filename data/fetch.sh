#!/bin/bash

BN=$(dirname $(readlink -f $0 || python3 -c "import sys,os;print(os.path.realpath(sys.argv[1]))" $0))
cd $BN

wget https://lab.cs.tsinghua.edu.cn/physics-data/terrain/dataset.tar.gz -O - | tar -xzf - .
sha256sum -c checksums.sha256

if [[ $? != 0 ]]; then
  echo "Checksum failed. Please run this script again."
fi
