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
              withCredentials([usernamePassword(credentialsId: 'aliyundocker', passwordVariable: 'aliyundockerPassword', usernameVariable: 'aliyundockerUser')]) {
                sh "docker login -u ${env.aliyundockerUser} -p ${env.aliyundockerPassword}"
                sh 'docker push $registry.cn-shanghai.aliyuncs.com/crawler_test/$registry:latest$BUILD_NUMBER'
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