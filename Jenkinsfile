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
        bat returnStatus: true, script:  'robot -x xunit "%WORKSPACE%"/robot/test.robot'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying....'
      }
    }
    stage('Cook') {
      steps {
        echo 'Cook.......'
      }
    }
    stage('Supper') {
      steps {
        sleep 10
        mail(subject: 'Test1 Jenkins Test 1', body: 'Hey Dood', from: 'cw171001@teradata.com', to: 'cw171001@teradata.com', replyTo: 'cw171001@teradata.com')
      }
    }
  }
post {
        always {
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        success {
            echo 'I succeeeded!'
        }
        unstable {
            echo 'I am unstable :/'
        }
  failure {
        mail to: 'cw171001@teradata.com',
             subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
             body: "Something is wrong with ${env.BUILD_URL}"
    }
        changed {
            echo 'Things were different before.....'
        }
    }

}