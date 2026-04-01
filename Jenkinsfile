pipeline {
    agent any

    environment {
        IMAGE_NAME = "inventory-api"
        CONTAINER_NAME = "inventory-api-container"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Aaron5044/inventory-api.git', branch: 'main'
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
                bat 'newman run tests/tests.json'
            }
        }

        stage('Generate README') {
            steps {
                bat '''
                echo Inventory Management API > README.txt
                echo ======================== >> README.txt
                echo GET  /getSingleProduct?product_id=int >> README.txt
                echo GET  /getAll >> README.txt
                echo POST /addNew >> README.txt
                echo DELETE /deleteOne?product_id=int >> README.txt
                echo GET  /startsWith?letter=str >> README.txt
                echo GET  /paginate?start_id=int&end_id=int >> README.txt
                echo GET  /convert?product_id=int >> README.txt
                echo FastAPI docs: https://fastapi.tiangolo.com/ >> README.txt
                '''
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
                bat 'powershell Compress-Archive -Path . -DestinationPath complete-%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%-%TIME:~0,2%%TIME:~3,2%.zip -Force'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
    }
}
```

---

## Step 2 — Create tests folder
In VS Code create a new **folder** called `tests` inside your project. Inside that folder create a file called `tests.json` — leave it empty for now, we'll fill it after Postman.

Your folder should look like:
```
inventory-api/
├── tests/
│   └── tests.json
├── Jenkinsfile
├── main.py
├── csv_to_mongo.py
├── Dockerfile
├── requirements.txt
├── .env
└── .gitignore
```

---

## Step 3 — Push to GitHub
Open GitHub Desktop:
1. You'll see `Jenkinsfile` and `tests/tests.json` listed as new files
2. Commit message:
```
Add Jenkinsfile and tests folder