# Build Chatbot Dist
FROM node:9.6.1

# Copy package.json file - To be cache -
COPY package.json .

# Install npm dependecies
RUN npm install --silent
RUN npm install react-scripts@1.1.1 serve -g --silent

# Copy chatbot project from (host) to (container)
ADD . .

# Run the build script it will move it self from
RUN npm run build

# Serve the built files
CMD serve -l 9000 -s build
