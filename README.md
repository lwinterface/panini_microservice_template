# Panini microservice template

### Abstract

This microservice is a template of how other microservices should look like:
- Files, the hierarchy of files
- Tests example
- Documentation example

### How to use

How to run the microservice:

`docker-compose up`

How to run project with connection to remote NATS server:

`docker-compose -f docker-compose.remote.yml up --build`

(required `.env.remote` file that shouldn't be included in repository)

How to install requirements locally(required for tests):

`pip3 install -r requirements.txt`

How to run tests with XML report:

`python3 -m pytest --junitxml=test-results/out.xml`

### NATS subjects

Sending:

`"some.publish.subject"` - to test for "some" data sending

Listening:

`"some.publish.subject"` - to test for "some" data recieving


### Recommendations how to deliver Panini microservice for `ms_general` project


The current structure of `ms_general` project is tied to the filesystem and might expect a specific hierarchy of directories and files.
Below are recommendations:

- Tests should work completely autonomously & independently from "ms_general". 
- Tests required XML reports for CI/CD pipeline
- Expected README.md file with description of how to run tests in readme. CI/CD system will run these tests after each commit to "develop" and "main" branch and deliver updated code to **stage** or **production** servers
- Microservice must have a global CONFIG_PATH variable, the absolute path of the config folder on the server. It is expected that configuration on a server will be in “config” directory [here](https://github.com/lwinterface/ms_general/tree/develop/config) . On the developer's computer, a configuration directory “config” is located where it is convenient for you.
- Configurations should be in a repository of the microservice if there are tests required for them.
- If your microservice required to use a new configuration file, it should be in ms_general/config; just create a pull request with a new config there(or update for old one).
- If the service requires custom .env files, use the following name “.env.” + unique name. For example .env.myuniquevars.
- Developer's shouldn't store sensitive configs or environments in the repository (including the ms_general repository). All “production” configs & environments are considered sensitive data, api keys are also considered sensitive data. After that, if the repository does not have enough configs and .env files, it’s might be sensitive. You or DevOps team need to add them manually then.
- Each PR to `main` branch required to tag with new version & update in `CHANGES.rst`. A first version is always v0.1.0


Following by this recommendation will significantly help us quickly integrate microservices into the system.

###### The finished microservice should include:

- Main code in directory `app`
- Pytest or uniittest tests in directory `tests`
- `Dockerfile` - a container that can be built and run
- `docker-compose.yml` - includes nats-server and everything you need to run the microservice independently
- `docker-compose.remote.yml` - to connect to an existing system, the nats_server host must be in the .env file
- `.env` files are similar with https://github.com/lwinterface/ms_general/tree/develop/environments
- `README.md` that describe:
    - microservices business logic description(required)
    - how to install/run/test microservice(required)
    - list of NATS subjects it subscribes/sends to(required)
    - usage recommendations(optional)
    - microservice limits expectations(optional)

