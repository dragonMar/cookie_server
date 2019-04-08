pipeline {
    environment {
        registry = "registry.cn-shanghai.aliyuncs.com/crawler_test/cookie_server"
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
                  withCredentials([usernamePassword(credentialsId: 'aliyundocker', passwordVariable: 'aliyundockerPassword', usernameVariable: 'aliyundockerUser')]) {
                      sh "docker login -u ${env.aliyundockerUser} -p ${env.aliyundockerPassword} registry.cn-shanghai.aliyuncs.com"
                      sh 'docker push $registry:$BUILD_NUMBER'
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