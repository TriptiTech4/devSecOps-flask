pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = tool 'sonar-scanner'
        IMAGE_NAME = "devsecops-flask:latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=devsecops-flask \
                    -Dsonar.projectName=devsecops-flask \
                    -Dsonar.sources=.
                    """
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t devsecops-flask .
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                trivy image --exit-code 0 --severity HIGH,CRITICAL devsecops-flask
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f flask-app || true
                docker run -d --name flask-app -p 7000:7000 devsecops-flask
                '''
            }
        }
    }

    post {
        success {
            echo "✅ PIPELINE COMPLETED SUCCESSFULLY"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
