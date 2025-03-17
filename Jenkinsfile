pipeline {
    agent any

    environment {
        AWS_ECR_REPO = 'flask-hello-world'  // Set your AWS ECR repository name
        ECS_CLUSTER = 'northstar-cluster'  // Set your ECS cluster name
        ECS_SERVICE = 'flask-app-service'  // Set your ECS service name
        ECS_TASK_DEFINITION = 'flask-app-task'  // Set your ECS task definition
        IMAGE_NAME = 'flask-hello-world'  // Docker image name
        DOCKERFILE_PATH = '.'  // Path to the Dockerfile (can be adjusted)
        GITHUB_REPO = 'https://github.com/swapsocial/flask-app.git'  // GitHub repo URL
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository from GitHub
                git branch: 'main', url: "${GITHUB_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${IMAGE_NAME} ${DOCKERFILE_PATH}"
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    // Tag the Docker image
                    def tag = "v2.0"  // You can also use dynamic tags, such as the commit hash
                    sh "docker tag ${IMAGE_NAME} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_REPO}:${tag}"
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    // Login to AWS ECR using AWS CLI
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    """
                }
            }
        }

        stage('Push Docker Image to AWS ECR') {
            steps {
                script {
                    // Push the Docker image to AWS ECR
                    def tag = "v2.0"  // Ensure you're using the correct tag
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_REPO}:${tag}"
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                script {
                    // Update ECS service to use the new Docker image
                    sh """
                        aws ecs update-service --cluster ${ECS_CLUSTER} --service ${ECS_SERVICE} --task-definition ${ECS_TASK_DEFINITION} --desired-count 1 --region ${AWS_REGION}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs for details."
        }
    }
}
