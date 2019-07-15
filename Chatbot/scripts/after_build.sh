#!/bin/bash

# THIS WORKS ONLY WITH DOCKER
rm -rf static/widgets
mkdir static/widgets
mv dist/* static/widgets
rm -rf dist
