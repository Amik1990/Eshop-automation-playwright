pipeline {
    agent any

    environment {
        // Nastavení cesty k Pythonu (pokud není v PATH, upravte)
        // Vytvoříme virtuální prostředí přímo v workspace
        VENV_NAME = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                // Stáhne kód z repozitáře (automaticky nastaveno Jenkinsem)
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Kontrola, zda venv existuje, pokud ne, vytvoříme ho
                    if (!fileExists("${VENV_NAME}")) {
                        echo "Creating virtual environment..."
                        bat "python -m venv ${VENV_NAME}"
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                // Instalace knihoven
                echo "Installing requirements..."
                bat "${VENV_NAME}\\Scripts\\pip install -r requirements.txt"
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                // Instalace prohlížečů pro Playwright
                echo "Installing Playwright browsers..."
                bat "${VENV_NAME}\\Scripts\\playwright install"
            }
        }

        stage('Run Tests') {
            steps {
                // Spuštění testů
                // --alluredir je důležitý pro generování reportu
                echo "Running Pytest..."
                // Používáme 'bat' pro Windows. Pokud testy selžou, chceme pokračovat k reportu, proto catchError (nebo try/catch)
                // V deklarativní pipeline se to řeší v sekci 'post', takže tady můžeme nechat test selhat.
                bat "${VENV_NAME}\\Scripts\\pytest"
            }
        }
    }

    post {
        always {
            // Tento blok se provede vždy, i když testy spadnou
            echo "Generating Allure Report..."

            // Vyžaduje nainstalovaný 'Allure Jenkins Plugin' v Jenkinsu
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
        success {
            echo "Tests passed successfully!"
        }
        failure {
            echo "Tests failed!"
        }
    }
}
