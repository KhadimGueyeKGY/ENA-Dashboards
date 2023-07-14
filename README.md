# ENA Dashboards
 * ENA-Datahub-Dashboard (default)
 * ENA-Cohort-Dashboard

## Usage: 
```
git clone https://github.com/KhadimGueyeKGY/ENA-Dashboards.git
cd ENA-Dashboards
pip install --no-cache-dir -r requirements.txt
pip install --upgrade pip
```
You can either modify the ```authentication.yaml``` file by adding your username and password, or the running application will prompt you for your username and password.

```
python manage.py runserver

```

## Docker commands 

```
docker build -t ena-dashboards .
docker run --rm -it -p 8000:8000  ena-dashboards

```

## Docker image


  * https://hub.docker.com/r/khadimgueyekgy/ena-dashboards 


## view (ENA Dashboards)

  * http://127.0.0.1:8000/ena-datahub-dashboard/ 
  * http://127.0.0.1:8000/ena-cohort-dashboard/ 

