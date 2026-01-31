pipeline {
    agent any

    environment {
        SONAR_HOST_URL = "http://localhost:9000"
        IMAGE_NAME = "devsecops-flask-app"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/TriptiTech4/DevSecOps-Flask.git'
            }
        }

        stage('SonarQube SAST Analysis') {
            environment {
                SONAR_TOKEN = credentials('sonar-token')
            }
            steps {
                sh '''
                docker run --rm \
                  -v $(pwd):/usr/src \
                  sonarsource/sonar-scanner-cli \
                  -Dsonar.projectKey=devsecops-flask \
                  -Dsonar.projectName=devsecops-flask \
                  -Dsonar.sources=. \
                  -Dsonar.host.url=${SONAR_HOST_URL} \
                  -Dsonar.login=$SONAR_TOKEN
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME} ./app
                '''
            }
        }

        stage('OWASP Dependency Check (SCA)') {
            steps {
                sh '''
                docker run --rm \
                  -v $(pwd):/src \
                  -v dependency-check-data:/usr/share/dependency-check/data \
                  owasp/dependency-check \
                  --scan /src \
                  --format HTML \
                  --out /src/dependency-check-report \
                  --disableAssembly \
                  --failOnCVSS 11 \
                  --noupdate || true
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                docker run --rm \
                  -v /var/run/docker.sock:/var/run/docker.sock \
                  aquasec/trivy:latest image \
                  --severity HIGH,CRITICAL \
                  --exit-code 0 \
                  ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dependency-check-report/*.html',
                fingerprint: true,
                allowEmptyArchive: true
        }

        success {
            echo "✅ DevSecOps Pipeline completed successfully!"
        }

        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
