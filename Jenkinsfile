pipeline {
    environment {
        registry = "cookie_server"
        registryCredential = 'registry.cn-shanghai.aliyuncs.com/crawler_test'
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
        stage('Deploy Image') {
            steps{
                script {
                        docker.withRegistry( '', registryCredential ) {
                            dockerImage.push()
                        }
                }
            }
         }
         stage('Remove Unused docker image') {
             steps{
                 sh "docker rmi $registry:$BUILD_NUMBER"
             }
         }
    }
}