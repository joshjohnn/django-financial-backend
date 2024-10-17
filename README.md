# Financial Backend Deployment

This README provides an overview of the steps required to set up, build, deploy, and manage a Django-based financial backend using AWS ECS (Elastic Container Service) with Fargate.

## Prerequisites

Before starting, ensure you have the following:

- **AWS CLI** installed and configured with access and secret keys.
- **Docker** installed for containerizing your application.
- An AWS account with permissions to create ECS clusters, task definitions, IAM roles, and other related resources.

## Setup Instructions

### 1. Clone the Repository

```sh
# Clone the project repository
$ git clone <repository-url>
$ cd financial_backend
```

### 2. Create the Docker Image

1. **Build Docker Image**:
   
   ```sh
   docker build -t financial-backend .
   ```

2. **Run the Docker Container Locally**:

   ```sh
   docker run -p 8000:8000 financial-backend
   ```

Ensure your Django application is working properly before deploying it to AWS.

### 3. Push Docker Image to AWS ECR

1. **Create an ECR Repository**:

   ```sh
   aws ecr create-repository --repository-name financial-backend
   ```

2. **Login to ECR**:

   ```sh
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com
   ```

3. **Tag and Push the Image**:

   ```sh
   docker tag financial-backend:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/financial-backend:latest
   docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/financial-backend:latest
   ```

### 4. Create AWS ECS Cluster and Task Definition

1. **Create a Cluster**:

   ```sh
   aws ecs create-cluster --cluster-name financial-backend-cluster
   ```

2. **Register Task Definition**:

   ```sh
   aws ecs register-task-definition \
     --family financial-backend-task \
     --network-mode awsvpc \
     --container-definitions '[{
       "name": "financial-backend-container",
       "image": "<account_id>.dkr.ecr.us-east-1.amazonaws.com/financial-backend:latest",
       "memory": 512,
       "cpu": 256,
       "essential": true,
       "portMappings": [{
         "containerPort": 8000,
         "hostPort": 8000,
         "protocol": "tcp"
       }]
     }]' \
     --requires-compatibilities FARGATE \
     --cpu "256" \
     --memory "512" \
     --execution-role-arn arn:aws:iam::<account_id>:role/ecsTaskExecutionRole
   ```

### 5. Run Task on ECS

1. **Run Task on Fargate**:

   ```sh
   aws ecs run-task \
     --cluster financial-backend-cluster \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-0b3939a85a514e5bb],securityGroups=[sg-00ec27f9299ae9948],assignPublicIp=ENABLED}" \
     --task-definition financial-backend-task
   ```

### 6. Verify Deployment

1. **Check Task Status**:

   Run the following command to verify if the task is running:

   ```sh
   aws ecs describe-tasks --cluster financial-backend-cluster --tasks <task_arn>
   ```

2. **Access the Application**:

   Once the status is **RUNNING**, get the public IP address of the container and visit it in your browser to verify that the deployment is successful.

## Cleanup

To remove all resources after testing:

1. **Stop and Deregister Task**:

   ```sh
   aws ecs stop-task --cluster financial-backend-cluster --task <task_arn>
   ```

2. **Delete Cluster**:

   ```sh
   aws ecs delete-cluster --cluster financial-backend-cluster
   ```

3. **Delete ECR Repository**:

   ```sh
   aws ecr delete-repository --repository-name financial-backend --force
   ```

## Notes

- Ensure the security groups have the appropriate inbound and outbound rules.
- Proper IAM permissions are required for all operations.

## Troubleshooting

- If the task fails to start, check the **stoppedReason** by describing the task:

  ```sh
  aws ecs describe-tasks --cluster financial-backend-cluster --tasks <task_arn>
  ```

- Make sure the Docker image was successfully pushed to ECR and that the task definition points to the correct image URI.

