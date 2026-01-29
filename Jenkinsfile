pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = tool 'sonar-scanner'
        DOCKER_IMAGE = "devsecops-flask:latest"
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

        stage('Quality Gate') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh 'trivy image --exit-code 0 --severity HIGH,CRITICAL $DOCKER_IMAGE'
            }
        }
    }

    post {
        success {
            echo "PIPELINE SUCCESSFUL"
        }
        failure {
            echo "PIPELINE FAILED"
        }
    }
}
