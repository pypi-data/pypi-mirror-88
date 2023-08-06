import click
from glob import glob
import os

from .__about__ import __version__
from grvlms.commands import config as config_cli
from grvlms import config as grvlms_config
from grvlms import env
from grvlms import interactive
HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "MYSQL_DATABASE": "ecommerce",
        "MYSQL_USERNAME": "ecommerce",
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_KEY": "ecommerce",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "API_KEY": "{{ 20|random_string }}",
        "PAYMENT_PROCESSORS": {
            "cybersource": {
                "merchant_id": "SET-ME-PLEASE",
                "profile_id": "SET-ME-PLEASE",
                "access_key": "SET-ME-PLEASE",
                "secret_key": "SET-ME-PLEASE",
                "transaction_key": "SET-ME-PLEASE",
                "payment_page_url": "https://testsecureacceptance.cybersource.com/pay",
                "receipt_page_url": "/checkout/receipt/",
                "cancel_checkout_path": "/checkout/cancel-checkout/",
                "soap_api_url": "https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.140.wsdl",
                "send_level_2_3_details": True,
                "sop_profile_id": "SET-ME-PLEASE",
                "sop_access_key": "SET-ME-PLEASE",
                "sop_secret_key": "SET-ME-PLEASE",
                "sop_payment_page_url": "https://testsecureacceptance.cybersource.com/silent/pay",
            },
            "paypal": {
                "mode": "sandbox",
                "client_id": "SET-ME-PLEASE",
                "client_secret": "SET-ME-PLEASE",
                "receipt_url": "/checkout/receipt/",
                "cancel_checkout_path": "/checkout/cancel-checkout/",
                "error_url": "/checkout/error/",
            },
        },
        "ENABLED_PAYMENT_PROCESSORS": ["cybersource", "paypal"],
        "ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS": ["cybersource"],
        "EXTRA_PAYMENT_PROCESSOR_CLASSES": [],
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "groovetech/openedx-ecommerce:{{ ECOMMERCE_VERSION }}",
        "WORKER_DOCKER_IMAGE": "groovetech/openedx-ecommerce-worker:{{ ECOMMERCE_VERSION }}",
        "HOST": "ecommerce.{{ WILDCARD_DOMAIN }}",
        "API_TIMEOUT": 5,
        "WORKER_JWT_ISSUER": "ecommerce-worker",
        "EXTRA_PIP_REQUIREMENTS": [],
    },
}

hooks = {
    "build-image": {
        "ecommerce": "{{ ECOMMERCE_DOCKER_IMAGE }}",
        "ecommerce-worker": "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
    },
    "remote-image": {
        "ecommerce": "{{ ECOMMERCE_DOCKER_IMAGE }}",
        "ecommerce-worker": "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
    },
    "init": ["mysql", "lms", "ecommerce"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
    
@click.group(help="Extra Command for E-Commerce")
def command():
    pass

@click.command(help="Print E-Commerce version", name="version")
def print_version():
    click.secho("The version is: {}".format(__version__), fg="blue")

def ask_questions_ecommerce(config, defaults):
    interactive.ask(
        "MYSQL Database:",
        "ECOMMERCE_MYSQL_DATABASE",
        config,
        {"ECOMMERCE_MYSQL_DATABASE": ""}
    )
    interactive.ask(
        "MYSQL Username:",
        "ECOMMERCE_MYSQL_USERNAME",
        config,
        {"ECOMMERCE_MYSQL_USERNAME": ""}
    )
    interactive.ask(
        "MYSQL Passwork:",
        "ECOMMERCE_MYSQL_PASSWORD",
        config,
        {"ECOMMERCE_MYSQL_PASSWORD": ""}
    )
    interactive.ask(
        "Secret Key:",
        "ECOMMERCE_SECRET_KEY",
        config,
        {"ECOMMERCE_SECRET_KEY": ""}
    )
    interactive.ask(
        "Oauth2 Key:",
        "ECOMMERCE_OAUTH2_KEY",
        config,
        {"ECOMMERCE_OAUTH2_KEY": ""}
    )
    interactive.ask(
        "Oauth2 Secret:",
        "ECOMMERCE_OAUTH2_SECRET",
        config,
        {"ECOMMERCE_OAUTH2_SECRET": ""}
    )
    interactive.ask(
        "API Key:",
        "ECOMMERCE_API_KEY",
        config,
        {"ECOMMERCE_API_KEY": ""}
    )

def load_config_ecommerce(root, interactive=True):
    defaults = grvlms_config.load_defaults()
    config = grvlms_config.load_current(root, defaults)
    if interactive:
        ask_questions_ecommerce(config, defaults)
    return config, defaults

@click.command(help="E-Commerce variables configuration", name="config")
@click.option("-i", "--interactive", is_flag=True, help="Run interactively")
@click.option("-s", "--set", "set_",
    type=config_cli.YamlParamType(),
    multiple=True,
    metavar="KEY=VAL", 
    help="Set a configuration value")
@click.pass_obj
def config_ecommerce(context, interactive, set_):
    config, defaults = load_config_ecommerce(
        context.root, interactive=interactive
    )
    if set_:
        grvlms_config.merge(config, dict(set_), force=True)
    grvlms_config.save_config_file(context.root, config)
    grvlms_config.merge(config, defaults)
    env.save(context.root, config)

command.add_command(print_version)
command.add_command(config_ecommerce)
