#!/bin/sh

UPSTREAM_REPO=/home/mark/Projects/core-integration-zimi
UPSTREAM_BRANCH=zimi-integration

echo Updating upstream repo
(cd ${UPSTREAM_REPO}; git pull origin ${UPSTREAM_BRANCH}; git checkout ${UPSTREAM_BRANCH})

echo Importing zimi contents
cp ${UPSTREAM_REPO}/homeassistant/components/zimi/*.py custom_components/zimi

echo Checking git status
git status

