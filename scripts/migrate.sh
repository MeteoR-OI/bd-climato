#!/bin/bash

cd ..
for f in $(cat scripts/db.txt)
do
    python manage.py svc run migrate $f
done
cd scripts
