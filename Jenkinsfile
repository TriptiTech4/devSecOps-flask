pipeline {
    agent any

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
                sh 'docker build -t devsecops-flask:latest .'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                trivy image --exit-code 0 --severity LOW,MEDIUM devsecops-flask:latest
                trivy image --exit-code 1 --severity HIGH,CRITICAL devsecops-flask:latest
                '''
            }
        }
    }

    post {
        success {
            echo "PIPELINE SUCCESS"
        }
        failure {
            echo "PIPELINE FAILED"
        }
    }
}
