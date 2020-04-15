import click
import yaml
import re
from kubernetes import client
from os import path
from utils import hiss, util
import settings

def terminate_rca():
    name = settings.RCA_NAME
    domain = settings.RCA_ORG

    # Terminate stateful set
    return settings.k8s.delete_stateful(name=name, namespace=domain, delete_pvc=True) 


def delete_rca():
    name = settings.RCA_NAME
    domain = settings.RCA_ORG

    # Delete stateful set
    return settings.k8s.delete_stateful(name=name, namespace=domain)


def setup_rca():
    domain = settings.RCA_ORG

    # Create temp folder & namespace
    settings.k8s.prereqs(domain)

    dict_env = {
        'ORG': domain,
        'RCA_NAME': settings.RCA_NAME,
        'FABRIC_ORGS': settings.ORGS,
        'EFS_SERVER': settings.EFS_SERVER,
        'EFS_PATH': settings.EFS_PATH,
        'EFS_EXTEND': settings.EFS_EXTEND
    }

    k8s_template_file = '%s/rca/fabric-deployment-rca.yaml' % util.get_k8s_template_path()
    settings.k8s.apply_yaml_from_template(
        namespace=domain, k8s_template_file=k8s_template_file, dict_env=dict_env)

    if settings.EXTERNAL_RCA_ADDRESSES != '':
        # Deploy nlb
        k8s_nlb_template_file = '%s/rca/fabric-deployment-rca-nlb.yaml' % util.get_k8s_template_path()
        settings.k8s.apply_yaml_from_template(
        namespace=domain, k8s_template_file=k8s_nlb_template_file, dict_env=dict_env)



@click.group()
def rca():
    """Root Certificate Authority"""
    pass


@rca.command('setup', short_help="Setup Root CA")
def setup():
    hiss.rattle('Setup Root CA Server')
    setup_rca()

@rca.command('delete', short_help="Delete Root CA")
def delete():
    hiss.rattle('Delete Root CA Server')
    delete_rca()

@rca.command('terminate', short_help="Terminate Root CA")
def terminate():
    hiss.rattle('Terminate Root CA Server')
    terminate_rca()