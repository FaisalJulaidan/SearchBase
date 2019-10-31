# ----------------------------------------------------------------------------
# Build React Dist
FROM node:9.6.1

# Copy package.json file - To be cache -
COPY package.json .

# Install npm dependecies
RUN npm install --silent
RUN npm install react-scripts@1.1.1 serve -g --silent

# Copy react project
ADD . .

# Run the build script it will move it self from
RUN npm run build
RUN rm -rf node_modules

CMD ["serve", "-l", "3001", "-s", "build"]
