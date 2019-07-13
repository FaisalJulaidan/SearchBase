# ----------------------------------------------------------------------------
# Build Chatbot Dist
FROM node:9.6.1 as chatbot_builder

# Change directory to Client
WORKDIR /Chatbot

# Copy package.json file - To be cache -
COPY Chatbot/package.json .

# Install npm dependecies
RUN npm install --silent

# Copy chatbot project from (host) to (container)
ADD Chatbot .

# Run the build script it will move it self from
RUN npm run build

# ----------------------------------------------------------------------------
# Build React Dist
FROM node:9.6.1 as client_builder

# Change directory to client
WORKDIR /Client

# Copy package.json file - To be cache -
COPY Client/package.json .

# Install npm dependecies
RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent

# Copy react project
ADD Client .

# Run the build script it will move it self from
RUN npm run build

# ----------------------------------------------------------------------------
# Run python in production
FROM python:3

# Change/Create directory to server
WORKDIR /Server

# Copy Pipfile and paste it in Server - To be cached -
COPY Server/Pipfile .
COPY Server/Pipfile.lock .

# Install pipenv to install dependecies
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Copy (host) Server and paste in (container) Server directory
ADD Server .

# Copy static/widgets directory from chatbot_builder, which includes the new build version of chatbot
COPY --from=chatbot_builder Chatbot/build static/widgets

# Copy static/react_app directory from client_builder, which includes the new build version of react_app
COPY --from=client_builder Client/build static/react_app

# Wait for mysql to run
COPY docker/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Run the production server
CMD ["/wait-for-it.sh", "mysql:3306", "--", \
     "gunicorn", "--bind",\
     "0.0.0.0:5000" ,"thesearchbase:app"]
