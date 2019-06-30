# ----------------------------------------------------------------------------
# Build React Dist
FROM node:9.6.1 as client_builder

# Copy package.json file - To be cache -
COPY client/package.json /client/

# Change directory to client
WORKDIR /client

# Install npm dependecies
RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent

# Copy react project
ADD client /client
# Copy the static directory
ADD static /static

# Run the build script it will move it self from
RUN npm run build

# ----------------------------------------------------------------------------
# Run python in production
FROM python:3

# Change directory to server
WORKDIR /server

# Copy Pipfile - To be cached -
COPY Pipfile .
COPY Pipfile.lock .

# Install pipenv to install dependecies
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Copy the whole project
ADD . .

# Copy static directory from client_builder, which includes the new build version of react_app
COPY --from=client_builder static static

# Wait for mysql to run
COPY docker/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Run the production server
CMD ["/wait-for-it.sh", "mysql:3306", "--", \
     "gunicorn", "--bind",\
     "0.0.0.0:5000" ,"thesearchbase:app"]
