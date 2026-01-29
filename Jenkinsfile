pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'sonarqube'     // Name exactly as in Jenkins > Manage Jenkins > System
        IMAGE_NAME = 'devsecops-flask'
        IMAGE_TAG = 'latest'
    }

    stages {

        stage('Checkout SCM') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/TriptiTech4/devSecOps-flask.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=devsecops-flask \
                    -Dsonar.projectName=devsecops-flask \
                    -Dsonar.sources=. \
                    -Dsonar.language=py \
                    -Dsonar.python.version=3 \
                    -Dsonar.sourceEncoding=UTF-8
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
