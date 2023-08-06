from cli.cloud.aws.stack import Stack
import logging
import json

class CfnCompiler():

    @classmethod
    def build_template(cls, deployer, templates, wait=True):

        for template in templates:
            logging.info(json.dumps(template, indent=4))
            stack = Stack(template, deployer)
            stack.read_template()
            stack.build_lambda_package()
            stack.render_template()
            stack.validate_rendered_template()
            stack.deploy(wait=wait)


    @classmethod
    def cleanup(cls, deployer, templates, wait=True):

        for template in templates:
            logging.info(json.dumps(template, indent=4))
            stack = Stack(template, deployer)
            stack.cleanup(wait)


    @classmethod
    def trigger_deployment(cls, deployer, templates, wait=True):
        for template in templates:
            logging.info(json.dumps(template, indent=4))
            stack = Stack(template, deployer)
            stack.read_template()
            stack.build_lambda_package()
            stack.render_template()
            stack.validate_rendered_template()
            stack.trigger_deployment()


    @classmethod
    def get_workflow_arn(cls, workflow_name, config):
        region = config.get("aws", "region", "ap-southeast-1")
        account = config.get("aws", "account", None)
        return f"arn:aws:states:{region}:{account}:stateMachine:{workflow_name}"