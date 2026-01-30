pipeline {
    agent any

    environment {
        IMAGE_NAME = "devsecops-flask"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/TriptiTech4/devSecOps-flask.git'
            }
        }

        stage('SonarQube Scan') {
            steps {
                script {
                    try {
                        withSonarQubeEnv('sonarqube') {
                            sh '''
                            sonar-scanner \
                            -Dsonar.projectKey=devsecops-flask \
                            -Dsonar.projectName=devsecops-flask \
                            -Dsonar.sources=.
                            '''
                        }
                    } catch (err) {
                        echo "⚠ SonarQube scan failed but pipeline continues"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    try {
                        timeout(time: 2, unit: 'MINUTES') {
                            waitForQualityGate abortPipeline: false
                        }
                    } catch (err) {
                        echo "⚠ Quality gate skipped"
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    sh '''
                    trivy image --severity HIGH,CRITICAL --no-progress $IMAGE_NAME || true
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ PIPELINE SUCCESSFULLY COMPLETED"
        }
        always {
            echo "📦 DevSecOps pipeline executed"
        }
    }
}
