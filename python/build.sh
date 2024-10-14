#!/bin/bash
rm -r dist
pyinstaller run.spec
mkdir dist/ratventure
mv dist/run dist/ratventure/ratventure
cp -r gamefiles dist/ratventure/gamefiles
cp -r fonts dist/ratventure/fonts
cp -r sounds dist/ratventure/sounds
cp -r surfaces dist/ratventure/surfaces
(cd dist && zip -r ratventure.zip ratventure)
