pipeline {
    agent any

    environment {
        IMAGE_NAME = "devsecops-flask"
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
                  --network devsecops-net \
                  -v $(pwd):/usr/src \
                  sonarsource/sonar-scanner-cli \
                  -Dsonar.projectKey=devsecops-flask \
                  -Dsonar.projectName=devsecops-flask \
                  -Dsonar.sources=. \
                  -Dsonar.host.url=http://sonarqube:9000 \
                  -Dsonar.login=$SONAR_TOKEN
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME} .
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
                  --failOnCVSS 11 || true
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                trivy image \
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
                allowEmptyArchive: true
        }
        success {
            echo "✅ DEVSECOPS PIPELINE COMPLETED SUCCESSFULLY"
        }
        failure {
            echo "❌ PIPELINE FAILED — CHECK SECURITY STAGES"
        }
    }
}
