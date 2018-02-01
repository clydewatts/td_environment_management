pipeline {
  agent any
  stages {
    stage('Initialise') {
      steps {
        catchError() {
          dir(path: 'jenkins') {
            bat 'python test1.py  --INSTANCE=%INSTANCE%'
          }
          
        }
        
        pwd(tmp: true)
      }
    }
stage('Validate') {
       steps {
         echo 'Validate..'
         bat returnStatus: true, script:  'robot -x xunit "%WORKSPACE%"/robot/test.robot'
         step([$class: 'XUnitBuilder',
                 thresholds: [[$class: 'FailedThreshold', unstableThreshold: '1']],
                 tools: [[$class: 'JUnitType', pattern: 'xunit.*']]])




          step([$class: 'RobotPublisher',
             disableArchiveOutput: false,
             logFileName: 'log.html',
             otherFiles: '',
             outputFileName: 'output.xml',
             outputPath: '.',
             passThreshold: 100,
             reportFileName: 'report.html',
             unstableThreshold: 0]);


       }
     }

    stage('Deploy') {
      steps {
        echo 'Deploying....'
      }
    }
    stage('Test') {
      steps {
        echo 'Test.......'
      }
    }
     stage('Approve') {
            input {
                message "Should we continue?"
                ok "Yes, we should."
                submitter "cw171001"
                parameters {
                    string(name: 'PERSON', defaultValue: 'Mr Jenkins', description: 'Who should I say hello to?')
                }
            }
            steps {
                echo "Hello, ${PERSON}, nice to meet you."
            }
        }
    stage('Production') {
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