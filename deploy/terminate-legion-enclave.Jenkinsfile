pipeline {
    agent any

    environment {
        //Input parameters
        param_git_branch = "${params.GitBranch}"
        param_profile = "${params.Profile}"
        param_legion_version = "${params.LegionVersion}"
        aram_enclave_name = "${params.EnclaveName}"
        param_docker_repo = "${params.DockerRepo}"
        param_debug_run = "${params.DebugRun}"
        //Job parameters
        sharedLibPath = "deploy/legionPipeline.groovy"
        ansibleHome =  "/opt/legion/deploy/ansible"
        ansibleVerbose = '-v'
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
                script {
                    legion = load "${env.sharedLibPath}"
                    legion.buildDescription()
                }
            }
        }
        
        stage('Terminate Legion Enclave') {
            steps {
                script {
                    legion.ansibleDebugRunCheck(env.param_debug_run)
                    legion.terminateLegionEnclave()
                }
            }
        }
    }
    
    post {
        always {
            script {
                legion = load "${sharedLibPath}"
                legion.notifyBuild(currentBuild.currentResult)
            }
            deleteDir()
        }
    }
}