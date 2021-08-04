# INSTALLING

The following instructions target Ubuntu 20.04 LTS but should also apply to any
system that uses `systemd` to install and manage services. Python 3.8 or newer
is required and the system must already have a working installation available.

This document provides instructions on how to serve the application through
[Gunicorn](https://gunicorn.org) and use [NGINX](https://nginx.org/) as a
front-end HTTP server. Other options are available for serving up FastAPI
applications, but those options will not be covered here.

## Installing the Application

Clone a copy of this repository to a location of your choosing by running:

```bash
git clone https://github.com/questionlp/api.wwdt.me_fastapi.git
```

Within the new local copy of the repository, create a new virtual environment
and install the required packages by running the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

Next, make a copy of the `.env.dist` file and name it `.env`. Edit the `.env`
file and fill in the required database connection information and any other
settings that are specific to your environment.

To validate the installation, start up `uvicorn` using the following command
while in the application root directory and with the virtual environment
activated:

```bash
uvicorn app.main:app --reload
```

Once started, open a browser and go to http://127.0.0.1:8000/docs. This should
bring up the Swagger UI interface. Use the interface to test the various
endpoints provided.

## Configuring Gunicorn

Gunicorn can take configuration options either as command line arguments or it
can load configuration options from a `gunicorn.conf.py` file located in the
same directory that Gunicorn is launched from.

A template configuration file is included in the repository called
`gunicorn.conf.dist.py`. A copy of that file should be made and named
`gunicorn.conf.py` and the configuration options reviewed. The following
options may need to be changed depending on the environment in which the
application is being deployed:

* `bind`: The template defaults to using a UNIX socket file at
`/tmp/gunicorn-wwdtmapi.sock` as the listener. If TCP socket is preferred,
change the value to `IP:PORT` (replacing `IP` and `PORT` with the
appropriate IP address of the interface and TCP port to listen to)
* `workers`: The number of processes that are created to handle requests.
* `accesslog`: The file that will be used to write access log entries to.
Change the value from a string to `None` to disable access logging if that'll
be handled by NGINX or a front-end HTTP server.
* `errorlog`: The file that will be used to write error log entries to.
Change the value from a string to `None` to disable error logging (not
recommended).

For more information on the above configuration options and other configuration
options avaiable, check out the [Gunicorn documentation site](https://docs.gunicorn.org/en/stable/settings.html).

## Setting up a Gunicorn systemd Service

A template `systemd` service file is included in the repository named 
`gunicorn-wwdtmapi.dist.service`. That service file provides the commands and
arguments used to start a Gunicorn instance to serve up the application. A copy
of that template file can be modified and installed under `/etc/systemd/system`.

For this document, the service file will be installed as `gunicorn-wwdtmapi.service`
and the service name will be `gunicorn-wwdtmapi`. The service file name, thus the
service name, can be changed to meet your needs and requirements.

You will need to modify the following items in the new service file:

* `User`: The user which the service will run under
* `Group`: The group which the service will run under
* `WorkingDirectory`: Provide the full path to the application root directory.
**Do not** include the `app` directory in the path
* `Environment`: Add the full path to the `venv/bin` directory
* `ExecStart`: Include the full path to the `venv/bin` directory and insert
that between `ExecStart=` and `gunicorn`

Save the file and run the following commands to enable and start the new service:

```bash
sudo systemctl enable wwdtmapi_fastapi
sudo systemctl start wwdtmapi_fastapi
```

Verify that the service started by running the following command:

```bash
sudo systemctl status wwdtmapi_fastapi
```

## Serving the Application Through NGINX

Once the service is up and running, NGINX can be configured to proxy requests
to Gunicorn. NGINX can also be set up to cache responses and provide additional
access controls that may not be feasible with Gunicorn.

The following NGINX configuration snippet provides a starting point for serving
up the application.

```nginx
upstream wwdtmapi_fastapi {
    server unix:/tmp/wwdtmapi_fastapi.sock fail_timeout=0;
}

server {
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header Host $http_host;
		proxy_redirect off;
		proxy_pass http://wwdtmapi_fastapi;
    }
}
```
