#!/bin/bash
cd /home/entity/retina-entity-tagger
echo $(date) >> entityRuns.log
python -m 1-nameEntityExtraction && echo $(date) >> entitySuccess.log
