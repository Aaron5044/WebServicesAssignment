pipeline {
    agent any

    environment {
        IMAGE_NAME = "inventory-api"
        CONTAINER_NAME = "inventory-api-container"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Aaron5044/WebServicesAssignment.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d --name %CONTAINER_NAME% -p 8000:8000 --env-file .env %IMAGE_NAME%'
                bat 'ping -n 6 127.0.0.1 > nul'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'C:\\Users\\aaron\\AppData\\Roaming\\npm\\newman.cmd run tests/tests.json'
    }
}
            }
        }

        stage('Generate README') {
            steps {
                bat 'echo Inventory Management API > README.txt'
                bat 'echo GET /getSingleProduct?product_id=int >> README.txt'
                bat 'echo GET /getAll >> README.txt'
                bat 'echo POST /addNew >> README.txt'
                bat 'echo DELETE /deleteOne?product_id=int >> README.txt'
                bat 'echo GET /startsWith?letter=str >> README.txt'
                bat 'echo GET /paginate?start_id=int&end_id=int >> README.txt'
                bat 'echo GET /convert?product_id=int >> README.txt'
                bat 'echo FastAPI docs: https://fastapi.tiangolo.com/ >> README.txt'
            }
        }

        stage('Stop Container') {
            steps {
                bat 'docker stop %CONTAINER_NAME%'
                bat 'docker rm %CONTAINER_NAME%'
            }
        }

        stage('Create Zip') {
            steps {
                bat 'powershell Compress-Archive -Path . -DestinationPath complete-%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%.zip -Force'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
    }
}


