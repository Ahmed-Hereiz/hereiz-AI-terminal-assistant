#!/bin/bash

set -e
pip install -r requirements.txt

if [ -d "customAgents" ] || [ -d "tests" ]; then
    echo "Removing existing customAgents and tests..."
    rm -rf customAgents* tests*
fi

echo "Getting customAgents..."
git clone https://github.com/Ahmed-Hereiz/customAgents.git

cd customAgents/scripts
bash setup.sh
cd ../../

mv customAgents tmpcustomAgents
mv tmpcustomAgents/customAgents* .
mv tmpcustomAgents/tests .

rm -rf tmpcustomAgents

exit 0