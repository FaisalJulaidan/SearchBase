# ----------------------------------------------------------------------------
# Run python in production
FROM python:3


# Copy Pipfile and paste it in Server - To be cached -
COPY Pipfile .
COPY Pipfile.lock .

# Install pipenv to install dependecies
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Copy (host) Server and paste in (container) Server directory
ADD . .

# Wait for mysql to run
COPY scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Run the production server
CMD ["/wait-for-it.sh", "mysql:3306", "--", \
     "gunicorn", "--bind",\
     "0.0.0.0:5000" ,"thesearchbase:app"]
