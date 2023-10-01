#!/bin/bash

echo 'Updating latest core-integration-zimi content to HACS repo'

UPSTREAM_BRANCH='upstream'
UPSTREAM_FILES='../home-assistant/core-integration-zimi/homeassistant/components/zimi'
CUSTOM_FILES='custom_components/zimi'

git checkout -b ${UPSTREAM_BRANCH}

echo Existing HACS version is: 
grep version ${CUSTOM_FILES}/manifest.json

cp ${UPSTREAM_FILES}/*.py ${CUSTOM_FILES}
cp ${UPSTREAM_FILES}/manifest.json ${CUSTOM_FILES}
cp ${UPSTREAM_FILES}/strings.json ${CUSTOM_FILES}
cp ${UPSTREAM_FILES}/translations/*.json ${CUSTOM_FILES}/translations

git status




