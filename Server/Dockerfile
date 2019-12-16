# Run python in production
FROM python:3.7

# Copy Pipfile and paste it in Server - To be cached -
COPY Pipfile .
COPY Pipfile.lock .

#COPY Server/Pipfile.lock .
# Install pipenv to install dependecies
RUN pip install pipenv
#RUN pipenv lock # no need
RUN pipenv install --system --deploy --ignore-pipfile

# Copy (host) Server and paste in (container) Server directory
ADD . .

# Run the production server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--no-sendfile", "--timeout", "90", "thesearchbase:app"]
