## Deployment Recipe 📝

##### Deploying new TSB docker server 📟

* Install docker (or use DigitalOcean marketplace)
* Clone the project
* Change directory `cd TheSearchBase`
* Setup the .env file for server and client
* Run `docker-compose up -d --no-deps --build`
* Update global variables in `docker/init-letsencrypt` add the new domain for SSL
* Run `./docker/init-letsencrypt.sh`



##### Explaining Docker Compose services ⚙️
* web: Builds react and move it to static + Install python libraries and run it on production
* mysql: Use Mysql in development only
* ngnix: Reverse proxy
