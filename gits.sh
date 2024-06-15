#!/bin/bash

# this script adds, commits, pulls, and pushes to git with the message passed from the command line
message=${1:-"syncing"}

echo "Adding, committing, pulling, and pushing to git with message: $message"

# Local git operations
git add --all
git commit -m "$message"
git pull
git push

# Remote git operations on the Raspberry Pi using sshpass to provide the password
sshpass -p 'raspberry' ssh pi@raspberrypi.local << 'ENDSSH'
cd RubiksCubeRobot
touch gits_worked.txt
ENDSSH
