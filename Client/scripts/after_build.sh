#!/bin/bash

# THIS WORKS ONLY WITH DOCKER
rm -rf static/react_app
mkdir static/react_app
mv build/* static/react_app
rm -rf build
