#!/bin/bash
cd /home/entity/retina-entity-tagger
echo $(date) >> entityRuns.log
python -m retina-entity-tagger.1-nameEntityExtraction && echo $(date) >> entitySuccess.log
