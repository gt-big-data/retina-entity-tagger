cd /home/bdc/retina-entity-tagger
echo $(date) >> entityRuns.log
python 1-extractEntities.py && echo $(date) >> entitySuccess.log