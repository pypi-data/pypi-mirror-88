from cli.cloud.aws.build import CodebuildHelper
import os

def test_is_codebuild():
    os.environ['CODEBUILD_SOURCE_REPO_URL'] = 'test'
    assert CodebuildHelper.is_codebuild() == True
    os.environ['CODEBUILD_SOURCE_REPO_URL'] = ''
    assert CodebuildHelper.is_codebuild() == False

def test_get_project():
    os.environ['CODEBUILD_SOURCE_REPO_URL'] = "https://git-codecommit.ap-southeast-1.amazonaws.com/v1/repos/de-testproj"
    assert CodebuildHelper.get_project() == "de-testproj"
    os.environ['CODEBUILD_SOURCE_REPO_URL'] = ''
    assert CodebuildHelper.get_project() == ""

def test_get_branch():
    CodebuildHelper.BRANCH_EXTRACT_SCRIPT += "echo master;"
    assert CodebuildHelper.get_branch().split("\n")[-1] == "master"