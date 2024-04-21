#!/usr/bin/bash
source C:/Users/doant/anaconda3/etc/profile.d/conda.sh
conda activate C:/Users/doant/anaconda3/envs/deepface
# gunicorn -w 1 -b 0.0.0.0:8888 main:app --reload --timeout 300
waitress-serve --listen=127.0.0.1:8888 main:app