pipeline {
  agent any
  stages {
    stage('Initialise') {
      steps {
        echo 'Init Started'
        catchError() {
          sh 'Jenkins/test1.py'
          bat(script: 'test', returnStatus: true, returnStdout: true)
        }
        
      }
    }
    stage('Test') {
      steps {
        echo 'Testing..'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying....'
      }
    }
    stage('Cook') {
      steps {
        echo 'Cook....'
      }
    }
    stage('Supper') {
      steps {
        sleep 10
      }
    }
  }
  environment {
    INSTANCE = 'D01'
  }
}