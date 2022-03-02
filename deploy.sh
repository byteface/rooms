#!/bin/bash

ROOT='/home/ubuntu/Desktop/rooms'

echo 'Updating files on server:'
scp -F ~/.ssh/config ./server.py eventual:$ROOT
scp -F ~/.ssh/config ./multi.py eventual:$ROOT
scp -F ~/.ssh/config -r ./static/ eventual:$ROOT'/static/'

echo 'Resarting service:'
ssh eventual 'sudo service rooms restart'

echo 'DONE'
