pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "finalproject-backend"
        FRONTEND_IMAGE = "finalproject-frontend"
        MLSERVICE_IMAGE = "finalproject-ml-service"
        VAULT_SECRET_PATH = "secret/ansible"
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:${env.PATH}"
    }

    triggers {
        githubPush()
    }

    options {
        skipDefaultCheckout()
        timestamps()
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-ssh',
                    url: 'git@github.com:aashishvaswani/MLOps---Support-ticket-routing.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker build -t $BACKEND_IMAGE ./backend'
                    sh 'docker build -t $FRONTEND_IMAGE ./frontend'
                    sh 'docker build -t $MLSERVICE_IMAGE ./ml_service'
                }
            }
        }

        stage('Run Backend Tests Inside Container') {
            steps {
                script {
                    sh '''
                        docker network create test-net || true
                        docker run -d --rm --name ml-service --network test-net -p 6000:6000 $MLSERVICE_IMAGE
                        docker run --rm --name backend-test --network test-net $BACKEND_IMAGE pytest tests/test_app.py || EXIT_CODE=$?
                        docker stop ml-service || true
                        exit $EXIT_CODE
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    docker tag finalproject-backend aashishvaswani/finalproject-backend:latest
                    docker tag finalproject-frontend aashishvaswani/finalproject-frontend:latest
                    docker tag finalproject-ml-service aashishvaswani/finalproject-ml-service:latest
    
                    docker push aashishvaswani/finalproject-backend:latest
                    docker push aashishvaswani/finalproject-frontend:latest
                    docker push aashishvaswani/finalproject-ml-service:latest
                '''
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    // Get password from Vault
                    def password = sh(
                        script: "VAULT_ADDR=http://127.0.0.1:8200 vault kv get -field=sudo_password ${VAULT_SECRET_PATH}",
                        returnStdout: true
                    ).trim()
        
                    writeFile file: 'extra-vars.yml', text: "ansible_sudo_pass: '${password}'\n"
                    sh "chmod 600 extra-vars.yml"
        
                    sh """
                        ANSIBLE_FORCE_COLOR=1 \
                        ansible-playbook -i ansible/inventory.ini ansible/playbook.yaml \
                        --extra-vars '@extra-vars.yml'
                    """

        
                    sh "rm -f extra-vars.yml"
                }
            }
        }




        stage('Verify Log Forwarding (Debug)') {
            steps {
                script {
                    sh 'sleep 30'
                    sh 'docker exec logstash tail -n 10 /usr/share/logstash/logs/app.log || echo "Log file not found"'
                }
            }
        }
    }

    post {
        success {
            mail to: 'VaswaniAashish.Raju@iiitb.ac.in',
                 subject: "SUCCESS: Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The build, test, and deployment was successful!"
        }
        failure {
            mail to: 'VaswaniAashish.Raju@iiitb.ac.in',
                 subject: "FAILURE: Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The build or deployment failed. Please check the Jenkins logs."
        }
        always {
            cleanWs()
        }
    }
}
