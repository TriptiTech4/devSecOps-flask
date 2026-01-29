pipeline {
    agent any

    tools {
        jdk 'jdk11'
        python 'python3'
    }

    environment {
        SONARQUBE_ENV = 'sonarqube'
        IMAGE_NAME = 'devsecops-flask'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/TriptiTech4/devsecops-flask.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=devsecops-flask \
                      -Dsonar.projectName=devsecops-flask \
                      -Dsonar.sources=. \
                      -Dsonar.language=py \
                      -Dsonar.python.version=3
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                waitForQualityGate abortPipeline: true
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                trivy image --exit-code 0 --severity LOW,MEDIUM ${IMAGE_NAME}:latest
                trivy image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
