pipeline {
    agent any
    environment {
        registry = "yuvalpress/project_3"
        registryCredentials = "docker_hub"
        dockerImage = ""
    }
    stages {
        stage('Check Github for commit') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])
                    properties([buildDiscarder(logRotator(daysToKeepStr: '5', numToKeepStr: '20')),])
                }
                git "https://github.com/yuvalpress/Devops_Project_3.git"
            }
        }
        stage('Run rest_app.py') {
            steps {
                script {
                        bat "start/min python rest_app.py"
                }
            }
        }
        stage('Run backend_testing.py') {
            steps{
                script{
                        bat 'start/min python backend_testing.py'
                }
            }
        }
        stage('Run clean_environment.py') {
            steps{
                script{
                        bat 'start/min python clean_environment.py'
                }
            }
        }
    }
    post {
        always {
            bat "docker rmi $registry:$BUILD_NUMBER"
        }
    }
}
