#! /bin/bash

# This is a script used to test the circleci config file without sending a
# build to github. You need to set your circle api token, the revision and the
# branch. This is explained in the following youtube video.
# https://www.youtube.com/watch?v=HB5DehCufG0

curl --user ${CIRCLE_TOKEN}: \
  --request POST \
  --form revision=a423da1a9dc3cb80bb82daaf7096ffddfe2a7ecd \
  --form config=@config.yml \
  --form notify=false \
  https://circleci.com/api/v1.1/project/github/PESD/akbash/tree/circleci-2.0-migration
