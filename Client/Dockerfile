#Build Stage Start

#Specify a base image
FROM node:10 as builder

#Copy the dependencies file
COPY package.json .

#Install dependencies
RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent

#Copy remaining files
COPY . .

#Build the project for production
RUN npm run build
