<<<<<<< HEAD

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
=======
pipeline {
    agent any
    
    parameters {
        choice(name: 'TARGET_ENVIRONMENT', choices: ['GREEN', 'BLUE'], description: 'Environment to deploy to')
        string(name: 'VERSION', defaultValue: '2.0.0', description: 'Version to deploy')
        booleanParam(name: 'AUTO_SWITCH_TRAFFIC', defaultValue: false, description: 'Automatically switch traffic after successful deployment')
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
                echo "✅ Checked out code from ${env.GITHUB_URL}"
            }
        }
        
        stage('Preparation') {
            steps {
                echo "🚀 Starting Blue-Green Deployment Pipeline"
                echo "Target Environment: ${params.TARGET_ENVIRONMENT}"
                echo "Version: ${params.VERSION}"
                
                script {
                    env.TARGET_PORT = params.TARGET_ENVIRONMENT == 'GREEN' ? env.GREEN_PORT : env.BLUE_PORT
                    env.INACTIVE_ENV = params.TARGET_ENVIRONMENT == 'GREEN' ? 'BLUE' : 'GREEN'
                    env.INACTIVE_PORT = params.TARGET_ENVIRONMENT == 'GREEN' ? env.BLUE_PORT : env.GREEN_PORT
                }
                
                echo "Target Port: ${env.TARGET_PORT}"
                echo "Inactive Environment: ${env.INACTIVE_ENV}"
                
                // Get current active environment before deployment
                script {
                    try {
                        def statusResponse = bat(script: "curl -s ${env.CONTROLLER_URL}/status", returnStdout: true).trim()
                        def statusJson = readJSON text: statusResponse
                        env.PREVIOUS_ENV = statusJson.active_environment
                        echo "Previous active environment: ${env.PREVIOUS_ENV}"
                    } catch (Exception e) {
                        echo "⚠️ Could not determine previous environment: ${e.getMessage()}"
                        env.PREVIOUS_ENV = 'UNKNOWN'
                    }
                }
            }
        }
        
        stage('Deploy to Target Environment') {
            steps {
                echo "📦 Deploying to ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        // Run deployment script
                        bat """
                            python scripts\\deploy.py ${params.TARGET_ENVIRONMENT} ${params.VERSION} ${env.TARGET_PORT}
                        """
                        
                        echo "✅ Deployment to ${params.TARGET_ENVIRONMENT} completed"
                    } catch (Exception e) {
                        echo "❌ Deployment failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Deployment failed")
                    }
                }
            }
        }
        
        stage('Start Application') {
            steps {
                echo "▶️ Starting application in ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        // Start the application in background
                        bat """
                            cd ${params.TARGET_ENVIRONMENT.toLowerCase()}_environment
                            start /B python start.py > app.log 2>&1
                        """
                        
                        // Wait for the application to start
                        sleep(time: 10, unit: 'SECONDS')
                        
                        echo "✅ Application started in ${params.TARGET_ENVIRONMENT} environment"
                    } catch (Exception e) {
                        echo "❌ Failed to start application: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Application start failed")
                    }
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo "🩺 Performing health check on ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        def healthCheckResult = bat(
                            script: "python scripts\\health_check.py http://localhost:${env.TARGET_PORT}",
                            returnStatus: true
                        )
                        
                        if (healthCheckResult == 0) {
                            echo "✅ Health check passed for ${params.TARGET_ENVIRONMENT} environment"
                        } else {
                            echo "❌ Health check failed for ${params.TARGET_ENVIRONMENT} environment"
                            currentBuild.result = 'FAILURE'
                            error("Health check failed")
                        }
                    } catch (Exception e) {
                        echo "❌ Health check error: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Health check failed")
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                echo "🧪 Running integration tests on ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        // Simulate integration tests
                        bat """
                            echo "Running API tests..."
                            curl -f http://localhost:${env.TARGET_PORT}/health
                            curl -f http://localhost:${env.TARGET_PORT}/api/version
                            echo "All tests passed!"
                        """
                        
                        echo "✅ Integration tests passed"
                    } catch (Exception e) {
                        echo "❌ Integration tests failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Integration tests failed")
                    }
                }
            }
        }
        
        stage('Traffic Switch Decision') {
            when {
                expression { params.AUTO_SWITCH_TRAFFIC == true }
            }
            steps {
                echo "🔄 Auto-switching traffic to ${params.TARGET_ENVIRONMENT} environment..."
                
                script {
                    try {
                        def switchResult = bat(
                            script: "python scripts\\switch_traffic.py ${env.CONTROLLER_URL} ${params.TARGET_ENVIRONMENT}",
                            returnStatus: true
                        )
                        
                        if (switchResult == 0) {
                            echo "✅ Traffic successfully switched to ${params.TARGET_ENVIRONMENT}"
                            env.TRAFFIC_SWITCHED = 'true'
                        } else {
                            echo "❌ Failed to switch traffic"
                            currentBuild.result = 'FAILURE'
                            error("Traffic switch failed")
                        }
                    } catch (Exception e) {
                        echo "❌ Traffic switch error: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Traffic switch failed")
                    }
                }
            }
        }
        
        stage('Manual Traffic Switch Approval') {
            when {
                expression { params.AUTO_SWITCH_TRAFFIC == false }
            }
            steps {
                script {
                    echo "⏸️ Deployment completed successfully!"
                    echo "🌐 New version is running on: http://localhost:${env.TARGET_PORT}"
                    echo "🎯 Ready for manual traffic switch to ${params.TARGET_ENVIRONMENT}"
                    
                    def userInput = input(
                        id: 'SwitchTraffic',
                        message: "Switch traffic to ${params.TARGET_ENVIRONMENT} environment?",
                        parameters: [
                            choice(name: 'ACTION', choices: ['SWITCH', 'SKIP'], description: 'Choose action')
                        ]
                    )
                    
                    if (userInput == 'SWITCH') {
                        echo "🔄 Switching traffic to ${params.TARGET_ENVIRONMENT}..."
                        def switchResult = bat(
                            script: "python scripts\\switch_traffic.py ${env.CONTROLLER_URL} ${params.TARGET_ENVIRONMENT}",
                            returnStatus: true
                        )
                        
                        if (switchResult == 0) {
                            echo "✅ Traffic successfully switched to ${params.TARGET_ENVIRONMENT}"
                            env.TRAFFIC_SWITCHED = 'true'
                        } else {
                            echo "❌ Failed to switch traffic"
                            currentBuild.result = 'UNSTABLE'
                        }
                    } else {
                        echo "⏭️ Traffic switch skipped by user"
                        env.TRAFFIC_SWITCHED = 'false'
                    }
                }
            }
        }
        
        stage('Post-Switch Verification') {
            when {
                expression { env.TRAFFIC_SWITCHED == 'true' }
            }
            steps {
                echo "🔍 Verifying traffic switch..."
                
                script {
                    try {
                        // Wait for traffic to stabilize
                        sleep(time: 5, unit: 'SECONDS')
                        
                        // Verify traffic controller status
                        bat """
                            curl -f ${env.CONTROLLER_URL}/status
                            echo "Traffic switch verification completed"
                        """
                        
                        // Display traffic flag content
                        echo "📄 Content of traffic_flag.txt:"
                        bat "type traffic_controller\\traffic_flag.txt"
                        
                        echo "✅ Post-switch verification passed"
                    } catch (Exception e) {
                        echo "⚠️ Post-switch verification failed: ${e.getMessage()}"
                        echo "Consider manual rollback if issues persist"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "🏁 Pipeline execution completed"
            
            script {
                def status = currentBuild.result ?: 'SUCCESS'
                echo "Final Status: ${status}"
                
                if (env.TRAFFIC_SWITCHED == 'true') {
                    echo "🌐 Live Traffic: ${env.CONTROLLER_URL}"
                    echo "🔵 Blue Environment: http://localhost:${env.BLUE_PORT}"
                    echo "🟢 Green Environment: http://localhost:${env.GREEN_PORT}"
                }
                
                // Always show traffic flag content
                echo "📄 Current traffic_flag.txt content:"
                bat "type traffic_controller\\traffic_flag.txt"
            }
        }
        
        success {
            echo "🎉 Blue-Green Deployment Pipeline completed successfully!"
            
            script {
                if (env.TRAFFIC_SWITCHED == 'true') {
                    echo "✅ New version ${params.VERSION} is now live on ${params.TARGET_ENVIRONMENT}"
                } else {
                    echo "✅ New version ${params.VERSION} is ready on ${params.TARGET_ENVIRONMENT}"
                    echo "💡 Manual traffic switch available at: ${env.CONTROLLER_URL}/admin"
                }
            }
        }
        
        failure {
            echo "❌ Blue-Green Deployment Pipeline failed!"
            echo "🔧 Attempting rollback to previous environment..."
            
            script {
                // Attempt rollback if we know the previous environment
                if (env.PREVIOUS_ENV != 'UNKNOWN' && env.PREVIOUS_ENV != params.TARGET_ENVIRONMENT) {
                    try {
                        echo "🔄 Rolling back to ${env.PREVIOUS_ENV} environment..."
                        def rollbackResult = bat(
                            script: "python scripts\\switch_traffic.py ${env.CONTROLLER_URL} ${env.PREVIOUS_ENV}",
                            returnStatus: true
                        )
                        
                        if (rollbackResult == 0) {
                            echo "✅ Rollback to ${env.PREVIOUS_ENV} completed successfully"
                        } else {
                            echo "❌ Rollback failed"
                        }
                    } catch (Exception e) {
                        echo "❌ Rollback error: ${e.getMessage()}"
                    }
                } else {
                    echo "⚠️ Cannot perform automatic rollback - previous environment unknown"
                }
                
                // Attempt cleanup of failed deployment
                try {
                    bat """
                        if exist ${params.TARGET_ENVIRONMENT.toLowerCase()}_environment\\app.pid (
                            for /f %%i in (${params.TARGET_ENVIRONMENT.toLowerCase()}_environment\\app.pid) do taskkill /F /PID %%i
                            del ${params.TARGET_ENVIRONMENT.toLowerCase()}_environment\\app.pid
                        )
                    """
                    echo "🧹 Cleanup completed"
                } catch (Exception e) {
                    echo "⚠️ Cleanup failed: ${e.getMessage()}"
                }
            }
        }
        
        unstable {
            echo "⚠️ Blue-Green Deployment completed with warnings"
            echo "🔍 Review the logs and consider manual intervention"
            
            script {
                // Offer manual rollback option
                if (env.TRAFFIC_SWITCHED == 'true') {
                    try {
                        def userInput = input(
                            id: 'ManualRollback',
                            message: "Deployment completed with warnings. Rollback to ${env.PREVIOUS_ENV}?",
                            parameters: [
                                choice(name: 'ROLLBACK_ACTION', choices: ['ROLLBACK', 'KEEP'], description: 'Choose action')
                            ]
                        )
                        
                        if (userInput == 'ROLLBACK') {
                            echo "🔄 Performing manual rollback to ${env.PREVIOUS_ENV}..."
                            def rollbackResult = bat(
                                script: "python scripts\\switch_traffic.py ${env.CONTROLLER_URL} ${env.PREVIOUS_ENV}",
                                returnStatus: true
                            )
                            
                            if (rollbackResult == 0) {
                                echo "✅ Manual rollback to ${env.PREVIOUS_ENV} completed"
                            } else {
                                echo "❌ Manual rollback failed"
                            }
                        }
                    } catch (Exception e) {
                        echo "⚠️ Manual rollback input error: ${e.getMessage()}"
                    }
                }
            }
        }
    }
}
>>>>>>> ea867fb861e2e807795c6ea85272ba6c3e769945
