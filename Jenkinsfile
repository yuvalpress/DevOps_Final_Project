pipeline {
    agent any
    stages {
        stage('Check Github for commit') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])
                }
                git 'https://github.com/yuvalpress/Devops_Project.git'
            }
        }
        stage('Run rest_app.py') {
            steps {
                script {
                    if (Boolean.valueOf(env.UNIX)) {
                        // for Daniel's check
                        bat 'rest_app.py'
                    } else {
                        bat 'rest_app.py'
                    }
                }
            }
        }
    }
}