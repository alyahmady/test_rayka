# RaykaTest Back-End

----

## Main notes:

- Tables will be created automatically in DDB.
- `.env` file is not in the repo, but there is a `.env.example` file.
- Werkzeug >= 3 is not supported by serverless-wsgi yet, so I used Werkzeug >= 2.
----


## Run test cases

0- Enable testing mode by updating below variable in `.env` file:
```shell
TESTING_MODE=true
```

1- Run below command
```shell
python manage.py test
```

2- Consider that you don't need to update any environment variable. `TESTING` will be patched during tests.

3- After finishing tests, you can disable testing mode by updating below variable in `.env` file:
```shell
TESTING_MODE=false
```

----


## Run (build) on AWS (Serverless)

0- Create a S3 bucket for Serverless Framework (if you don't have one).

1- Make a copy of `.env.example` and rename it to `.env`
```shell
cp ./.env.example ./.env
```

2- Update values in `.env` file. Set S3 bucket name in `DEPLOYMENT_BUCKET` variable.

3- Make sure you have authenticated with AWS CLI
```shell
aws sts get-caller-identity
```
If you get an error (or didn't get your account ID), you need to authenticate with AWS CLI:
```shell
aws configure --profile <AWS_PROFILE_NAME>
```

4- Run the following command to start a Amazon Linux container:
```shell
docker run -it -v <PROJECT_DIR>:/root/src/ -v ~/.aws:/root/.aws/ amazonlinux:latest bash
```

5- Inside the container, run the following commands:
```shell
yum install sudo -y
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel wget tar gcc-c++ make
```

6- Install Node.js in container:
```shell
sudo yum install https://rpm.nodesource.com/pub_20.x/nodistro/repo/nodesource-release-nodistro-1.noarch.rpm -y
sudo yum install nodejs -y --setopt=nodesource-nodejs.module_hotfixes=1
```

7- Install Python 3.11 in container:
```shell
sudo dnf install python3.11 -y
alias python='python3.11'
python -m ensurepip --upgrade
alias pip='pip3.11'
pip install --upgrade pip setuptools
```

8- Install Serverless Framework in container:
```shell
npm install -g serverless
```

9- Move to project directory and install dependencies:
```shell
cd /root/src/
pip install -r requirements.txt
sudo rm -rf node_modules/
npm install
```

10- Make AWS credentials profile, accessible:
```shell
export AWS_PROFILE=<AWS_PROFILE_NAME>
```

11- Deploy the project (make sure about `STAGE` env variable in `.env.` file before):
```shell
npm run deploy
```

12- `Serverless` will create an IAM role for the project, and will attach the required policies to it.
We need to attach policies `AmazonDynamoDBFullAccess` to the role manually.
- Go to https://us-east-1.console.aws.amazon.com/iamv2/home?region=eu-north-1#/roles
- Find the role with this pattern -> `<SERVICE_NAME>-<STAGE>-<REGION>-lambdaRole`
- Click on it and under `Add Permissions`, click on `Create Inline Policy`
- Select `DynamoDB` service and `All DynamoDB actions`.
- Next to `table`, click on `Add ARN` and enter your DynamoDB Table ARN in the input.
- Click on `Next`
- Set a name for the policy and click on `Create Policy`

12- You should get the successful response and address.

13- If you got a `AWS provider credentials not found` error, run below commands to re-configure AWS credentials in container:
```shell
sudo yum remove awscli
cd ~
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws configure --profile <AWS_PROFILE_NAME>
export AWS_PROFILE=<AWS_PROFILE_NAME>
```

14- If you got this error: `Stack:arn:aws:cloudformation:<REGION>:<UID>:stack/<AWS_DEPLOY_STACK_NAME>/<UUID> is in ROLLBACK_COMPLETE state and can not be updated.`
```shell
aws cloudformation delete-stack --stack-name <AWS_DEPLOY_STACK_NAME>
```
Also make sure that you have set `AWS_DEPLOY_STACK_NAME` variable in `.env` file.

15- Then try to deploy again.
```shell
cd /root/src/
npm run deploy
```

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

2- I didn't add any authentication.

3- I didn't add `created_at` and `updated_at` fields to models.

4- I didn't add any local or global indexes on tables.

5- I didn't add `drf_spectacular` for API documentation (because of time limitation).
Instead, I added a Postman collection file.

6- I also didn't follow Git Flow branching and merging strategy (because of time limitation).
There is only two branches: `main` and `develop`.
