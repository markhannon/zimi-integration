#!/bin/sh
# Parallel Development Workflow
#
# 1.Upstream development is done in a seperately checked out repo $UPSTREAM_REPO and $UPSTREAM_BRANCH
# 2.Downstream merge is done in this repo by running this script to copy latest  

MERGE_BRANCH=upstream
UPSTREAM_REPO=../core-zimi
UPSTREAM_BRANCH=zimi

echo Updating upstream repo
(cd ${UPSTREAM_REPO}; git pull origin ${UPSTREAM_BRANCH}; git checkout ${UPSTREAM_BRANCH})


echo Importing zimi contents into $MERGE_BRANCH branch
git checkout -b $MERGE_BRANCH
cp ${UPSTREAM_REPO}/homeassistant/components/zimi/*.py custom_components/zimi
git add custome_components/zimi/*
git commit -m 'Merge of latest upstream'

echo Checking git status
git status

echo Perform manual merge from $MERGE_BRANCH as required
