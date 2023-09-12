# Before start

It is required to specify `.env` variables

```
POSTGRES_USER=exerciser
POSTGRES_PASSWORD=exerciser
POSTGRES_DATABASE=exerciser
POSTGRES_HOST=db
POSTGRES_PORT=5432
SLACK_TOKEN= # Slack API token
SIGNING_SECRET= # Slack sign in secret. Not required for now
VERIFICATION_TOKEN= # Slack verification token
SECRET_KEY= # Django secret
```

# Start locally

```
docker-compose build
docker-compose up
```

# Deployment with docker

`deploy/docker-compose.prod.yml` adds nginx container

```
docker-compose build -f docker-compose.yml -f deploy/docker-compose.prod.yml
docker-compose up -d
```

# With Kubernetes

```
kubectl create secret generic exerciser-secret --from-env-file=.env
# Postgres database setup
kubectl apply -f deploy/kubernetes/persistent-volume-claim.yml
kubectl apply -f deploy/kubernetes/deployment-db.yml
kubectl apply -f deploy/kubernetes/service-db.yml
# Django application setup
kubectl apply -f deploy/kubernetes/deployment-web.yml
kubectl apply -f deploy/kubernetes/service-web.yml
# Add ingres
kubctl apply -f deploy/kubernetes/ingres.yml
```