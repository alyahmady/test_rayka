# RaykaTest Back-End

---

## Run (build) on local

- Requirements:
  - [Python](https://www.python.org/downloads/) >=3.11
  - [pip](https://pip.pypa.io/en/stable/cli/pip_install/)

1- Make a copy of `.env.example` and rename it to `.env`
```shell
cp ./.env.example ./.env
```

2- Update values in `.env` file

2- Activate a virtual environment
```shell
python -m venv .venv
source ./.venv/bin/activate
```

3- Install dependencies
```shell
pip install -r ./deploy/requirements/base.txt
```

4- Run server
```shell
python manage.py runserver 0.0.0.0:8000
```

App is accessible now, on [http://localhost:8000](http://localhost:8000)

---

## Run (build) with Docker Build

- Requirements:
  - [Docker Engine](https://docs.docker.com/engine/install/)

1- Make a copy of `.env.example` and rename it to `.env`
```shell
cp ./.env.example ./.env
```

2- Update values in `.env` file

3- Build docker image
```shell
docker build -f ./deploy/dockerfiles/backend.dockerfile -t raykatest-backend:1.0.0 ./
```

4- Run docker container
```shell
docker run -it -p 8000:8000 raykatest-backend:1.0.0
```

5- Push docker image to docker hub
```shell
docker tag raykatest-backend:1.0.0 <DOCKER-HUB-USERNAME>/raykatest-backend:1.0.0
docker push <DOCKER-HUB-USERNAME>/raykatest-backend:1.0.0
```

---

## Run (build) with Docker Compose

- Requirements:
  - [Docker Engine](https://docs.docker.com/engine/install/)
  - [Docker Compose Plugin](https://docs.docker.com/compose/install/)

1- Make a copy of `.env.example` and rename it to `.env`
```shell
cp ./.env.example ./.env
```

2- Update values in `.env` files

3- Run docker compose
```shell
docker compose -f ./docker-compose.yml up -d --build --force-recreate --remove-orphans
```

Now Back-End app (with Redis and PostgresSQL) are running in docker containers.

Back-End app is accessible now, on [http://localhost:80](http://localhost:80)

---
