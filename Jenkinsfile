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
        stage('run python') {
            steps {
                script {
                    if (Boolean.valueOf(env.UNIX)) {
                        sh 'python 1.py'
                    } else {
                        bat 'python 1.py'
                    }
                }
            }
        }
    }
}