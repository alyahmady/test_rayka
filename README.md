# RaykaTest Back-End

----

## Main notes:

- Tables will be created automatically in DDB.
- `.env` file is not in the repo, but there is a `.env.example` file.
- I didn't have permission to deploy on AWS with Zappa
```
An error occurred (ValidationException) when calling the PutRule operation: Provided role 'arn:aws:iam::675174937919:role/testrayka-dev-ZappaLambdaExecutionRole' cannot be assumed by principal 'events.amazonaws.com'
```

----
## Deploy on AWS with Zappa

- Requirements:
  - [AWS account](https://aws.amazon.com/)
  - [AWS CLI](https://aws.amazon.com/cli/)
  - [Python](https://www.python.org/downloads/) >=3.11
  - [pip](https://pip.pypa.io/en/stable/cli/pip_install/)

1- Make a copy of `.env.example` and rename it to `.env`
```shell
cp ./.env.example ./.env
```

2- Update values in `.env` file (especially `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` and `AWS_REGION_NAME`)

3- Activate a virtual environment
```shell
python -m venv .venv
source ./.venv/bin/activate
```

4- Install dependencies
```shell
pip install -r ./requirements.txt
```

5- If it's the first time of deploying, run this command to initialize Zappa
```shell
zappa init
```

6- Make sure AWS credentials are set correctly
```shell
aws configure
```

7- Deploy
```shell
zappa deploy dev
```

----

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
pip install -r ./requirements.txt
```

4- Run server
```shell
python manage.py runserver 0.0.0.0:8000
```

App is accessible now, on [http://localhost:8000](http://localhost:8000)

---

These 2 APIs are also available:



---

### Other notes:

1- We could make `serial` field, auto-incremental in SQL (achievable with SQLAlchemy):
```sql
CREATE SEQUENCE rayka_test_device_serial_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 999999999
    CACHE 1;

CREATE OR REPLACE FUNCTION rayka_test_generate_serial()
RETURNS TRIGGER AS $$
BEGIN
    NEW.serial = 'A' || lpad(nextval('rayka_test_device_serial_seq')::TEXT, 9, '0');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER rayka_test_devices_generate_serial
BEFORE INSERT ON rayka_test_devices
FOR EACH ROW
EXECUTE FUNCTION rayka_test_generate_serial();
```
but it's an antipattern in DDB because of its distributed nature (difficulties in sharding and partitioning)

2- I didn't add API versioning.

3- I didn't add any authentication.

4- I didn't add `created_at` and `updated_at` fields to models.

5- I didn't add any local or global indexes on tables.

6- I would recommend using one table for both `Device` and `DeviceModel` table in a project like this.
```json
{
  "id": 1,
  "serial": "A000000001",
  "model": {
    "name": "model1"
  },
  "note": "note1",
  "name": "name1"
}
```
But based on your payload schema, I separated them.

7- I didn't manage logging and error handling that well (because of time limitation).

8- I didn't add `drf_spectacular` for API documentation (because of time limitation).
Instead, I added a Postman collection file.
