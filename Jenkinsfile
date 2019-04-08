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
                withDockerRegistry([ credentialsId: "aliyundocker", url: "" ]) {
                    dockerImage.push()
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