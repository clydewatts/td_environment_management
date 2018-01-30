pipeline {
  agent any
  stages {
    stage('Initialise') {
      steps {
        catchError() {
          dir(path: 'jenkins') {
            bat 'python test1.py'
          }
          
        }
        
        pwd(tmp: true)
      }
    }
    stage('Test') {
      steps {
        echo 'Testing..'
        bat(script: 'robot "%WORKSPACE%"/robot/test.robot', returnStatus: true)
        archiveArtifacts 'output.xml'
        archiveArtifacts 'log.html'
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
        mail(subject: 'Test1 Jenkins Test 1', body: 'Hey Dood', from: 'cw171001@teradata.com', to: 'cw171001@teradata.com', replyTo: 'cw171001@teradata.com')
      }
    }
  }
  environment {
    INSTANCE = 'D01'
  }
}