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
            when {
              branch 'master'
            }
            steps {
                  withCredentials([usernamePassword(credentialsId: 'aliyundocker', passwordVariable: 'aliyundockerPassword', usernameVariable: 'aliyundockerUser')]) {
                      sh "docker login -u ${env.aliyundockerUser} -p ${env.aliyundockerPassword}"
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