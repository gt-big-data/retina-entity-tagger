#!/bin/bash
cd /home/entity/retina-entity-tagger
echo $(date) >> entityRuns.log
python -m name_entity_extraction && echo $(date) >> entitySuccess.log
