pipeline {
    agent {
        label "jenkins-python"
    }
    environment {
      ORG               = 'mirr254'
      APP_NAME          = 'bright-events'
      CHARTMUSEUM_CREDS = credentials('jenkins-x-chartmuseum')
      APP_MAIL_PASSWORD = credentials('APP_MAIL_PASSWORD') 
      APP_MAIL_USERNAME = credentials('APP_MAIL_USERNAME') 
      APP_SETTINGS = 'development'
      SECRET_KEY = credentials('SECRET_KEY')
      SECURITY_PASSWORD_RESET_SALT = credentials('SECURITY_PASSWORD_RESET_SALT')
      SECURITY_PASSWORD_SALT = credentials('SECURITY_PASSWORD_SALT')
      DATABASE_URL = 'postgresql://postgres:postgres@localhost:5433/bright-events'
    }
    stages {
      stage('CI Build and push snapshot') {
        when {
          branch 'PR-*'
        }
        environment {
          PREVIEW_VERSION = "0.0.0-SNAPSHOT-$BRANCH_NAME-$BUILD_NUMBER"
          PREVIEW_NAMESPACE = "$APP_NAME-$BRANCH_NAME".toLowerCase()
          HELM_RELEASE = "$PREVIEW_NAMESPACE".toLowerCase()
        }
        steps {
          container('python') {
            sh "apt-get update"
            sh "apt-get -y install gcc"
            sh "pip install -r requirements.txt"
            sh "nosetests --with-coverage --cover-package=app"

            sh 'export VERSION=$PREVIEW_VERSION && skaffold build -f skaffold.yaml'


            sh "jx step post build --image $DOCKER_REGISTRY/$ORG/$APP_NAME:$PREVIEW_VERSION"
          }

          dir ('./charts/preview') {
           container('python') {
             sh "make preview"
             sh "jx preview --app $APP_NAME --dir ../.."
           }
          }
        }
      }
      stage('Build Release') {
        when {
          branch 'master'
        }
        steps {
          container('python') {
            // ensure we're not on a detached head
            sh "git checkout master"
            sh "git config --global credential.helper store"

            sh "jx step git credentials"
            // so we can retrieve the version in later steps
            sh "echo \$(jx-release-version) > VERSION"
          }
          dir ('./charts/bright-events') {
            container('python') {
              sh "make tag"
            }
          }
          container('python') {
            sh "apt-get update"
            sh "apt-get -y install gcc"
            
            sh "pip install -r requirements.txt"
            sh "python -m unittest"

            sh 'export VERSION=`cat VERSION` && skaffold build -f skaffold.yaml'

            sh "jx step post build --image $DOCKER_REGISTRY/$ORG/$APP_NAME:\$(cat VERSION)"
          }
        }
      }
      stage('Promote to Environments') {
        when {
          branch 'master'
        }
        steps {
          dir ('./charts/bright-events') {
            container('python') {
              sh 'jx step changelog --version v\$(cat ../../VERSION)'

              // release the helm chart
              sh 'jx step helm release'

              // promote through all 'Auto' promotion Environments
              sh 'jx promote -b --all-auto --timeout 1h --version \$(cat ../../VERSION)'
            }
          }
        }
      }
    }
    post {
        always {
            cleanWs()
        }
    }
  }
