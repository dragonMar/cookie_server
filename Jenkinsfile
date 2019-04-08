pipeline {
    environment {
        registry = "localhost:5000/cookie_server"
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
                sh "docker push $registry:$BUILD_NUMBER"
            }
          }
        stage('Remove Unused docker image') {
            agent any
            steps{
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }
    }
}