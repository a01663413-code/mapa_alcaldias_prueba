#!/bin/bash
# Force LFS to use HTTPS instead of SSH
git config --global lfs.url "https://github.com/plpcollado/mapa_alcaldias_v1.git/info/lfs"
git config --global url."https://github.com/".insteadOf git@github.com:
git lfs install
git lfs pull
