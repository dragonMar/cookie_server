pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                dockerfile {
                    label 'cookie_server'
                    additionalBuildArgs '--build-arg version=$BUILD_NUMBER'
                    registryUrl 'https://localhost:5000'
                    registryCredentialsId 'cookie_server'
                }
            }
            steps {
                echo 'finish'
            }
        }
    }
}