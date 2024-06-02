# nagp_kubernetes
This repository contains the flask API's for adding and viewing the details of employee along with Kubernetes deployment files.

# Table of Contents
* [Code Repository Link](#code-repository-link)
* [Docker Hub URL](#docker-hub-url)
* [Service API URL](#service-api-url)
* [Screen Recording Link](#screen-recording-link)
* [Deployment Steps](#deployment-steps)


## Code Repository Link
[Repository_link](https://github.com/Jaishreeagarwal48/nagp_kubernetes)

## Docker Hub URL
[Docker_Hub_URL](https://hub.docker.com/repository/docker/agarwaljaishree/nagp_flaskapp/general)

## Service API URL
It contains the endpoint details of flask application:

* Server Check Endpoint

    `http://nagp.flaskapp.com:80/v1`

    Type of request: `GET`

* GET Employee Details Endpoint

    `http://nagp.flaskapp.com:80/v1/employee`

    Type of request: `GET`

* Add Employee Details Endpoint

    `http://nagp.flaskapp.com:80/v1/add`

    Type of request: `POST`
    
    Request Payload:
    
    `{
    "name":"jaishree",
    "email":"jaishree@gmail.com",
    "salary":98000,
    "department":"IT"}`


## Screen Recording Link
[Recording Link](https://nagarro-my.sharepoint.com/:v:/p/jaishree_agarwal/Eeu7NxHtSjxHqd8IiSMcYn0B5s_CEvdO1S1LYv_GJmqXUQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=P0fN7e)

## Deployment Steps

* Create Kubernetes standard cluster with minimum 2 nodes having 4vCPU and 32GB memory.
* Once cluster is up and running, run `gcloud container clusters get-credentials <cluster name> --zone <cluster zone> --project <project ID>` command in cloudshell to connect the cluster.
* Upload all the yaml files in GCP present in repo kubernetes folder.
* Steps to deploy MySQL server Stateful set:
    * To create storage class, run `kubectl apply -f mysql-storageclass.yaml`
    * To create secrets, run `kubectl apply -f secrets.yaml`
    * To create persistent volume claim for DB, run `kubectl apply -f mysql-pvc.yaml`
    * To create MySQL database using Stateful sets, run `kubectl apply -f mysql-statefulset.yaml`
    * To create headless cluster IP service for accessing the DB within cluster, run `kubectl apply -f mysql-service.yaml`
    * Once MySQL pod is up and running, login to the MySQL pod to create the database for flask application using command: `kubectl exec --stdin --tty <mysql podname> -- /bin/bash`
    * Once login to the bash script, run command `mysql -p` to login into mysql server by passing password which is available in file `./kubernetes/secrets.yaml` file.
    * Run command `create database <db_name>` to create database in MySQL server and db_name is available in `./kubernetes/configmap.yaml` file.
    * Run command `exit` to come outside mysql and run command `exit` to come outside bash script.

* Steps to deploy Flask application:
    * To create the configmap, run `kubectl apply -f configmap.yaml`
    * To deploy the flask application, run `kubectl apply -f flask-deployment.yaml`
    * To create node port service for accessing the application outside of cluster, run `kubectl apply -f flask-nodeport-service.yaml`
    * To enable the firewall for nodeport service port, run `gcloud compute firewall-rules create <rule name> --allow tcp:31000 --project <project id>`
    * To apply the horizontal autoscaling of pods in API server, run `kubectl apply -f flask-autoscaling.yaml`

* Steps to deploy Ingress:
    * To create Ingress controller, run `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml`
    * To create Ingress which act as an entrypoint to the cluster, run `kubectl apply -f flask-ingress.yaml`
    * Once ingress is up and running, copy the external IP of ingress to create the mapping with the specified host `nagp.flaskapp.com` in `/etc/host` file
