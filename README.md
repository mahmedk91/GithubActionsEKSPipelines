# GithubActionsEKSPipelines
A sample of Github Actions deploying an application in EKS

Run the unit test with
```
python3 -m unittest
```

Run the following commands to build and run the app in your local kubernetes cluster
```
docker build -f deploy/Dockerfile -t application:$(git rev-parse HEAD) .
helm upgrade --install application ./deploy/helm --set image.tag=$(git rev-parse HEAD) --wait
```

Check the running app locally
```
kubectl logs -l app=application -f
```

Run this to cleanup
```
helm uninstall application
docker rmi $(docker images -a | grep application | awk '{print $3}') -f
```