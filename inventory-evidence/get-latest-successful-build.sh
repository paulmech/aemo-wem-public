#!/usr/bin/env bash


IDS=$(aws codebuild list-builds --query "[ids]" --output text)

BUILD_NUMBER=$(aws codebuild batch-get-builds --query "builds[?buildStatus=='SUCCEEDED']|[0].buildNumber" --ids $IDS)

echo $BUILD_NUMBER
