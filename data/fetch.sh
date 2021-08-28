#!/bin/bash

# https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "${SCRIPT_DIR}"

wget https://lab.cs.tsinghua.edu.cn/physics-data/terrain/dataset.tar.gz -O - | tar -xzf -
sha256sum -c checksums.sha256

if [[ $? != 0 ]]; then
  echo "Checksum failed. Please run this script again."
fi
