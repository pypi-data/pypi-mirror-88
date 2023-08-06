from cli.config import ConfigParser
import pytest
import click
import os
from cli.templates import DeployerRepositoryTemplate
from cli.templates import InitializeDeployerTemplate
from cli.templates import CoreDeployerTemplate
from subprocess import call



def test_name(deployer):
    assert DeployerRepositoryTemplate.name(deployer) == "test-deployer-repository-stack"

def test_aws(deployer, config, configfile):
    template = DeployerRepositoryTemplate.aws(deployer, config)
    ref_template = InitializeDeployerTemplate.aws(deployer, config)
    core_template = CoreDeployerTemplate.aws(deployer, config)

    assert len(template) == 1
    assert template[0]['aws']['account-id'] == configfile['aws'].get('account')
    assert template[0]['aws']['region'] == configfile['aws'].get('region')
    assert template[0]['aws']['deployment-role'] == configfile['aws'].get('deployment-role', '')
    assert os.path.isfile(template[0]['location'])
    assert template[0]['template']['name'] == DeployerRepositoryTemplate.name(deployer)
    assert template[0]['template']['parameters']['artifact-bucket'] == ref_template[0]['template']['parameters']['artifact-bucket']
    assert template[0]['template']['parameters']['deployment-workflow'] == core_template[0]['template']['parameters']['deployment-workflow']

def test_aws_template(deployer, config, configfile):
    template = DeployerRepositoryTemplate.aws(deployer, config)
    assert 0 == call(f"cfn-lint {template[0]['location']}", shell=True)