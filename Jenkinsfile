pipeline {
    environment {
        registry = "cookie_server"
        registryHost = 'registry.cn-shanghai.aliyuncs.com/crawler_test'
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
                sh "docker push $registryHost/$registry:$BUILD_NUMBER"
            }
         }
         stage('Remove Unused docker image') {
             steps{
                 sh "docker rmi $registry:$BUILD_NUMBER"
             }
         }
    }
}