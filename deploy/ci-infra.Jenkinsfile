def legionVersion = "latest"

node {
    stage('Checkout GIT'){
            checkout scm
    }
    def legion = load 'deploy/legionPipeline.groovy'
    try {
        stage('Build') {
            result = build job: params.BuildLegionJobName, propagate: true, wait: true, parameters: [
                    [$class: 'GitParameterValue', name: 'GitBranch', value: params.GitBranch],
                    string(name: 'PyPiRepository', value: params.PyPiRepository),
                    string(name: 'PyPiDistributionTargetName', value: params.PyPiDistributionTargetName),
                    string(name: 'DockerRegistry', value: params.DockerRegistry),
                    string(name: 'JenkinsPluginsRepository', value: params.JenkinsPluginsRepository),
                    string(name: 'JenkinsPluginsRepositoryStore', value: params.JenkinsPluginsRepositoryStore),
                    string(name: 'LocalDocumentationStorage', value: params.LocalDocumentationStorage),
                    booleanParam(name: 'EnableSlackNotifications', value: params.EnableSlackNotifications),
                    booleanParam(name: 'EnableDockerCache', value: true)
            ]

            buildNumber = result.getNumber()
            print 'Finished build id ' + buildNumber.toString()

            // Save logs
            logFile = result.getRawBuild().getLogFile()
            sh """
            cat "${logFile.getPath()}" | perl -pe 's/\\x1b\\[8m.*?\\x1b\\[0m//g;' > build-log.txt 2>&1
            """
            archiveArtifacts 'build-log.txt'

            // Copy artifacts
            copyArtifacts filter: '*', flatten: true, fingerprintArtifacts: true, projectName: 'Build_Legion_Artifacts', selector: specific(buildNumber.toString()), target: ''
            sh 'ls -lah'
            
            //sh 'cp pylint.log python-lint-log.txt'
            //archiveArtifacts 'python-lint-log.txt'

            // Load variables
            def map = [:]
            def envs = sh returnStdout: true, script: "cat file.env"

            envs.split("\n").each {
                kv = it.split('=', 2)
                print "Loaded ${kv[0]} = ${kv[1]}"
                map[kv[0]] = kv[1]
            }

            legionVersion = map["LEGION_VERSION"]

            print "Loaded version ${legionVersion}"
            // \ Load variables

            if (!legionVersion) {
                error 'Cannot get legion release version number'
            }
        }

        stage('Terminate Cluster if exists') {
            result = build job: params.TerminateClusterJobName, propagate: true, wait: true, parameters: [
                    [$class: 'GitParameterValue', name: 'GitBranch', value: params.GitBranch],
                    string(name: 'Profile', value: params.Profile),
                    string(name: 'LegionVersion', value: legionVersion),
                    string(name: 'DockerRepo', value: params.DockerRepo)
            ]
        }

        stage('Create Cluster') {
            result = build job: params.CreateClusterJobName, propagate: true, wait: true, parameters: [
                    [$class: 'GitParameterValue', name: 'GitBranch', value: params.GitBranch],
                    string(name: 'Profile', value: params.Profile),
                    booleanParam(name: 'Skip_kops', value: false),
                    string(name: 'LegionVersion', value: legionVersion),
                    string(name: 'DockerRepo', value: params.DockerRepo),
                    string(name: 'LegionInfraVersion', value: params.LegionInfraVersion),
                    string(name: 'LegionInfraRegistry', value: params.LegionInfraRegistry)
            ]
        }

        stage('Deploy Legion & run tests') {
            result = build job: params.DeployLegionJobName, propagate: true, wait: true, parameters: [
                    [$class: 'GitParameterValue', name: 'GitBranch', value: params.GitBranch],
                    string(name: 'Profile', value: params.Profile),
                    string(name: 'LegionVersion', value: legionVersion),
                    string(name: 'DockerRepo', value: params.DockerRepo),
                    string(name: 'TestsTags', value: "infra"),
                    booleanParam(name: 'DeployLegion', value: true),
                    booleanParam(name: 'CreateJenkinsTests', value: true),
                    booleanParam(name: 'UseRegressionTests', value: true),
            ]
        }

        stage('Deploy Legion Enclave') {
            result = build job: params.DeployLegionEnclaveJobName, propagate: true, wait: true, parameters: [
                    [$class: 'GitParameterValue', name: 'GitBranch', value: params.GitBranch],
                    string(name: 'Profile', value: params.Profile),
                    string(name: 'LegionVersion', value: legionVersion),
                    string(name: 'DockerRepo', value: params.DockerRepo),
                    string(name: 'EnclaveName', value: 'enclave-ci')
            ]
        }

        stage('Terminate Legion Enclave') {
            result = build job: params.TerminateLegionEnclaveJobName, propagate: true, wait: true, parameters: [
                    [$class: 'GitParameterValue', name: 'GitBranch', value: params.GitBranch],
                    string(name: 'Profile', value: params.Profile),
                    string(name: 'EnclaveName', value: 'enclave-ci'),
                    string(name: 'LegionVersion', value: legionVersion),
                    string(name: 'DockerRepo', value: params.DockerRepo)
            ]
        }
        stage('Test') {
            print("${env.BUILD_NUMBER}")
        }
    }
    catch (e) {
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
    }
    finally {
        stage('Terminate Cluster') {
            result = build job: params.TerminateClusterJobName, propagate: true, wait: true, parameters: [
                [$class: 'GitParameterValue', name: 'GitBranch', value: params.GitBranch],
                    string(name: 'Profile', value: params.Profile),
                    string(name: 'LegionVersion', value: legionVersion),
                    string(name: 'DockerRepo', value: params.DockerRepo)
            ]
        }
        legion.notifyBuild(currentBuild.result)
    }

}