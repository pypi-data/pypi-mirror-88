import os
import logging
import click
from mldock.api.push import \
    push_to_ecr
from mldock.config.config_manager import \
    SagifyConfigManager

click.disable_unicode_literals_warning = True
logger=logging.getLogger('mldock')

@click.group()
def cloud():
    """
    Commands for local operations: train and deploy
    """
    pass

@click.command()
@click.option('--dir', help='Set the working directory for your sagify container.', required=True)
@click.option('--build', help='Set the working directory for your sagify container.', is_flag=True)
@click.option('--provider', help='Set the cloud provider', required=True, default='aws')
@click.pass_obj
def push(obj, dir, build, provider):
    """
    Command to push docker container image to ECR using your default AWS sdk credentials.

    note: Override default AWS credentials by providing AWS_DEFAULT_PROFILE environment variable.
    """
    # sagify_manager = SagifyConfigManager(
    #     filepath=os.path.join(dir, ".sagify.json")
    # )
    # # get sagify_module_path name
    # sagify_config = sagify_manager.get_config()
    # image_name = sagify_config.get("image_name", None)
    # dockerfile_path = os.path.join(
    #     dir,
    #     sagify_config.get("sagify_module_dir", "src"),
    #     'container'
    # )
    helper_library_path=obj['helper_library_path']
    sagify_manager = SagifyConfigManager(
        filepath=os.path.join(dir, ".mldock.json")
    )
    # get sagify_module_path name
    sagify_config = sagify_manager.get_config()
    module_path = os.path.join(
                dir,
        sagify_config.get("sagify_module_dir", "src"),
    )
    image_name = sagify_config.get("image_name", None)
    platform = sagify_config.get("platform", None)
    container_dir = sagify_config.get("container_dir", None)
    helper_library_path = obj['helper_library_path']

    dockerfile_path = os.path.join(
        dir,
        sagify_config.get("sagify_module_dir", "src"),
        container_dir
    )


    if image_name is None:
        logger.info("\nimage_name cannot be None")
    elif image_name.endswith(":latest"):
        logger.info("\nImage version is not supported at this point. Please remove :latest versioning")
    else:
        if provider == 'aws':
            if build:
                push_to_ecr(
                    script_path=os.path.join(helper_library_path,'api', 'build_and_push.sh'),
                    base_path=dir,
                    image_name=image_name,
                    dockerfile_path=dockerfile_path,
                    module_path=sagify_config.get("sagify_module_dir", "src"),
                    target_dir_name=sagify_config.get("sagify_module_dir", "src"),
                    requirements_file_path=sagify_config.get("requirements.txt", "requirements.txt")
                )
            else:
                raise Exception("Only Build and Push is supported at current. Set --build=true.")
        else:
            raise Exception("{} is not supported. Only 'aws' available at current for --provider".format(provider))


cloud.add_command(push)
