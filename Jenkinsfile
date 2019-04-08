pipeline {
    environment {
        registry = "cookie_server"
        dockerImage = ''
    }
    agent none
    stages {
        stage('Build') {
            steps{
                script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }
        stage('Publish') {
            agent any
            when {
              branch 'master'
            }
            steps {
                sh "docker push localhost:5000/$$registry:$BUILD_NUMBER"
            }
          }
        stage('Remove Unused docker image') {
            steps{
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }
    }
}