# GithubActionsEKSPipelines
A sample of Github Actions deploying an application in EKS

## Local Development

Run the unit test with
```
python3 -m unittest
```

Run the following commands to build and run the app in your local kubernetes cluster
```
GIT_COMMIT_SHA=$(git rev-parse HEAD)
docker build -f deploy/Dockerfile -t application:${GIT_COMMIT_SHA} .
helm upgrade --install application ./deploy/helm --set image.tag=${GIT_COMMIT_SHA} --wait
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

## Deploy on EKS

### Create the infrastructure (EKS and ECR)
Run the following command to create a mini EKS cluster and an ECR repo. This is a one time action and currently not hooked up in the CD pipeline. So, needs to be done manually.

```
aws cloudformation create-stack \
  --stack-name my-eks-stack \
  --template-body file://deploy/cloudformation.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue=vpc-xxxxxxxx \
    ParameterKey=SubnetIds,ParameterValue=subnet-xxxxxxxx\\,subnet-yyyyyyyy \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

### Deploy the app on EKS
Run the following commands to build and deploy the python app on EKS.

```
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
GIT_COMMIT_SHA=$(git rev-parse HEAD)
python3 -m unittest
docker build -f deploy/Dockerfile -t application:${GIT_COMMIT_SHA} .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com
docker tag application:${GIT_COMMIT_SHA} ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-application-ecr-repo:${GIT_COMMIT_SHA}
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-application-ecr-repo:${GIT_COMMIT_SHA}
aws eks update-kubeconfig --region us-east-1 --name eks-cluster-for-very-small-app
helm upgrade --install application ./deploy/helm --set image.repository=${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-application-ecr-repo --set image.tag=${GIT_COMMIT_SHA} --wait
```

### Check the logs
```
kubectl logs -l app=application -f
```