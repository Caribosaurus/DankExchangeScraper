#!/usr/bin/env bash
cp *.py ./Lambda_package
echo installing dependencies
pip install  -r requirements.txt -t Lambda_package --no-cache-dir --compile -q
cd Lambda_package
echo zipping packages
zip -uq -r9 ~/package.zip .
#echo pushing to aws
aws lambda update-function-code --function-name dankExchangeScraper --zip-file fileb://~/package.zip
rm -rf ./*
#rm -rf ~/package.zip