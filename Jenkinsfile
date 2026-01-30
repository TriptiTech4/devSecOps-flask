pipeline {
    agent any

    tools {
        sonarQubeScanner 'sonar-scanner'
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
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=devsecops-flask \
                    -Dsonar.projectName=devsecops-flask \
                    -Dsonar.sources=.
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t devsecops-flask .'
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
