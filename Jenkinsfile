pipeline {
    agent any
    stages {
        stage('Check Github for commit') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])
                    properties([buildDiscarder(logRotator(daysToKeepStr: '5', numToKeepStr: '20')),])
                }
                git 'https://github.com/yuvalpress/Devops_Project.git'
            }
        }
        stage('Run rest_app.py') {
            steps {
                script {
                    if (Boolean.valueOf(env.UNIX)) {
                        // for Daniel's check
                        sh 'nohup python rest_app.py &'
                    } else {
                        bat 'start/min python rest_app.py'
                    }
                }
            }
        }
        stage('Run web_app.py') {
            steps {
                script {
                    if (Boolean.valueOf(env.UNIX)) {
                        // for Daniel's check
                        sh 'nohup python web_app.py &'
                    } else {
                        bat 'start/min python web_app.py'
                    }
                }
            }
        }
        stage('Run backend_testing.py') {
            steps{
                script{
                    if (Boolean.valueOf(env.UNIX)) {
                        // for Daniel's check
                        sh 'nohup python backend_testing.py &'
                    } else {
                        bat 'start/min python backend_testing.py'
                    }
                }
            }
        }
        stage('Run frontend_testing.py') {
            steps{
                script{
                    if (Boolean.valueOf(env.UNIX)) {
                        // for Daniel's check
                        sh 'nohup python frontend_testing.py &'
                    } else {
                        bat 'start/min python backend_testing.py'
                    }
                }
            }
        }
        stage('Run combined_testing.py') {
            steps{
                script{
                    if (Boolean.valueOf(env.UNIX)) {
                        // for Daniel's check
                        sh 'nohup python combined_testing.py &'
                    } else {
                        bat 'start/min python combined_testing.py'
                    }
                }
            }
        }
        stage('Run clean_environment.py') {
            steps{
                script{
                    if (Boolean.valueOf(env.UNIX)) {
                        // for Daniel's check
                        sh 'nohup python clean_environment.py &'
                    } else {
                        bat 'start/min python clean_environment.py'
                    }
                }
            }
        }
    }
    post {
        failure {
            emailext body: 'Pipeline has failed.',
            recipientProviders: [[$class: 'DevelopersRecipientProvider'],
            [$class: 'RequesterRecipientProvider']], subject: 'Test'
        }
    }
}
