pipeline {
    agent any

    tools {
        jdk 'jdk11'
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
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=devsecops-flask \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonarqube:9000
                    '''
                }
            }
        }
    }
}
