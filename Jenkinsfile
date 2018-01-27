pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            echo 'Building..'
          }
        }
        stage('Directory') {
          steps {
            bat(script: 'test.bat', returnStatus: true, returnStdout: true)
          }
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
}