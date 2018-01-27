pipeline {
  agent any
  stages {
    stage('Initialise') {
      steps {
        catchError() {
          bat(script: 'test.py', returnStatus: true, returnStdout: true)
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