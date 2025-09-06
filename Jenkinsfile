
pipeline {
    agent any
    
    parameters {
        choice(name: 'TARGET_ENVIRONMENT', choices: ['GREEN', 'BLUE'], description: 'Environment to deploy to')
        string(name: 'VERSION', defaultValue: '2.0.0', description: 'Version to deploy')
        booleanParam(name: 'AUTO_SWITCH_TRAFFIC', defaultValue: true, description: 'Automatically switch traffic after successful deployment')
    }
    
    environment {
        BLUE_PORT = '5000'
        GREEN_PORT = '5001'
        CONTROLLER_URL = 'http://localhost:8000'
        GITHUB_URL = 'https://github.com/Samudini-Chamodya/blue-green-deployment-demo.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git url: env.GITHUB_URL, branch: 'main'
                echo "Checked out code from GitHub"
            }
        }
        
        stage('Preparation') {
            steps {
                echo "Starting Blue-Green Deployment Pipeline"
                echo "Target Environment: ${params.TARGET_ENVIRONMENT}"
                echo "Version: ${params.VERSION}"
                
                script {
                    env.TARGET_PORT = params.TARGET_ENVIRONMENT == 'GREEN' ? env.GREEN_PORT : env.BLUE_PORT
                    env.INACTIVE_ENV = params.TARGET_ENVIRONMENT == 'GREEN' ? 'BLUE' : 'GREEN'
                }
                
                echo "Target Port: ${env.TARGET_PORT}"
                echo "Inactive Environment: ${env.INACTIVE_ENV}"
            }
        }
        
        stage('Deploy to Target Environment') {
            steps {
                echo "Deploying to ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        bat "python scripts\\deploy.py ${params.TARGET_ENVIRONMENT} ${params.VERSION} ${env.TARGET_PORT}"
                        echo "Deployment to ${params.TARGET_ENVIRONMENT} completed"
                    } catch (Exception e) {
                        echo "Deployment failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Deployment failed")
                    }
                }
            }
        }
        
        stage('Start Application') {
            steps {
                echo "Starting application in ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        bat """
                            cd ${params.TARGET_ENVIRONMENT.toLowerCase()}_environment
                            start /B python start.py > app.log 2>&1
                        """
                        
                        sleep(time: 10, unit: 'SECONDS')
                        
                        echo "Application started in ${params.TARGET_ENVIRONMENT} environment"
                    } catch (Exception e) {
                        echo "Failed to start application: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Application start failed")
                    }
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo "Performing health check on ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        def healthCheckResult = bat(
                            script: "python scripts\\health_check.py http://localhost:${env.TARGET_PORT}",
                            returnStatus: true
                        )
                        
                        if (healthCheckResult == 0) {
                            echo "Health check passed for ${params.TARGET_ENVIRONMENT} environment"
                        } else {
                            echo "Health check failed for ${params.TARGET_ENVIRONMENT} environment"
                            currentBuild.result = 'FAILURE'
                            error("Health check failed")
                        }
                    } catch (Exception e) {
                        echo "Health check error: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Health check failed")
                    }
                }
            }
        }
        
        stage('Switch Traffic') {
            when {
                expression { params.AUTO_SWITCH_TRAFFIC == true }
            }
            steps {
                echo "Switching traffic to ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        def switchResult = bat(
                            script: "python scripts\\switch_traffic.py ${env.CONTROLLER_URL} ${params.TARGET_ENVIRONMENT}",
                            returnStatus: true
                        )
                        
                        if (switchResult == 0) {
                            echo "Traffic successfully switched to ${params.TARGET_ENVIRONMENT}"
                            env.TRAFFIC_SWITCHED = 'true'
                        } else {
                            echo "Failed to switch traffic"
                            currentBuild.result = 'FAILURE'
                            error("Traffic switch failed")
                        }
                    } catch (Exception e) {
                        echo "Traffic switch error: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Traffic switch failed")
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline execution completed"
            
            script {
                def status = currentBuild.result ?: 'SUCCESS'
                echo "Final Status: ${status}"
                
                // Try to show traffic flag content if it exists
                try {
                    bat "type traffic_controller\\traffic_flag.txt"
                } catch (Exception e) {
                    echo "Traffic flag file not found: ${e.getMessage()}"
                }
            }
        }
        
        success {
            echo "Pipeline completed successfully!"
            
            script {
                if (env.TRAFFIC_SWITCHED == 'true') {
                    echo "New version ${params.VERSION} is now live on ${params.TARGET_ENVIRONMENT}"
                } else {
                    echo "New version ${params.VERSION} is ready on ${params.TARGET_ENVIRONMENT}"
                    echo "Manual traffic switch available at: ${env.CONTROLLER_URL}/admin"
                }
            }
        }
        
        failure {
            echo "Pipeline failed!"
            echo "Attempting rollback to previous environment..."
            
            script {
                try {
                    echo "Rolling back to previous environment..."
                    def rollbackResult = bat(
                        script: "python scripts\\switch_traffic.py ${env.CONTROLLER_URL} ${params.TARGET_ENVIRONMENT == 'GREEN' ? 'BLUE' : 'GREEN'}",
                        returnStatus: true
                    )
                    
                    if (rollbackResult == 0) {
                        echo "Rollback completed successfully"
                    } else {
                        echo "Rollback failed"
                    }
                } catch (Exception e) {
                    echo "Rollback error: ${e.getMessage()}"
                }
                
                // Attempt cleanup of failed deployment
                try {
                    bat """
                        if exist ${params.TARGET_ENVIRONMENT.toLowerCase()}_environment\\app.pid (
                            for /f %%i in (${params.TARGET_ENVIRONMENT.toLowerCase()}_environment\\app.pid) do taskkill /F /PID %%i
                            del ${params.TARGET_ENVIRONMENT.toLowerCase()}_environment\\app.pid
                        )
                    """
                    echo "Cleanup completed"
                } catch (Exception e) {
                    echo "Cleanup failed: ${e.getMessage()}"
                }
            }
        }
    }
}
