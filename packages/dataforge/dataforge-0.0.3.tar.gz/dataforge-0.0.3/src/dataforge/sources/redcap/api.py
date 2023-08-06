"""CLI access to REDCap projects through API

Note: We use Requests instead of PycURL because it is easier to install and
is less restrictive about the certificate chain (e.g.,
https://redcap.uchicago.edu/ currently has a certificate chain containing an
expired certificate). Any performance degredation should be minor in most cases.
"""

import click
import click_config_file
import keyring
import requests
import datetime, os, sys
from urllib.parse import urlparse
from ... import config

PROJECT_XML = {
    'content': 'project_xml',
    'format': 'xml',
    'returnMetadataOnly': 'true',
    'exportFiles': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

PROJECT_DATA = {
    'content': 'record',
    'format': 'csv',
    'type': 'flat',
    'rawOrLabel': 'label',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'true',
    'returnFormat': 'json'
}

def export_to_file(post_fields, url, token, outfile):
    """Make call to REDCap API and write result to file"""
    post_fields.update({'token':token})
    response = requests.post(url, data=post_fields)
    
    with open(outfile, mode='wb') as f:
        f.write(response.content)

def config_provider(file_path, cmd_name):
    """Returns options found in configuration file(s)"""
    settings = config['sources.redcap.api'].get()
    if not settings:
        settings = {}
    return settings

@click.command()
@click.argument('url', envvar='REDCAP_URL')
@click.option('--token', '-t', help='REDCap API token')
@click.option('--project_name', '-p', envvar='REDCAP_PROJECT',
              help='REDCap project name abbreviation (no spaces)')
@click.option('--outdir', '-o', envvar='REDCAP_OUTDIR', default='tmp/redcap',
              show_default=True)
@click_config_file.configuration_option(provider=config_provider)
def export(url, token, project_name, outdir):
    """Export data and metadata from REDCap project"""
    
    if token is None:
        token = keyring.get_password(urlparse(url).hostname, project_name)
        if token is None:
            sys.exit('Token not found in system keyring')
    
    if project_name is None:
        project_name = ''
    elif project_name != '':
        project_name = project_name + '_'
    
    os.makedirs(outdir, exist_ok=True)
    ts = '{:%Y-%m-%d_%H%M}'.format(datetime.datetime.now())
    
    fname = '{}{}.REDCap.xml'.format(project_name, ts)
    export_to_file(PROJECT_XML, url, token, os.path.join(outdir,fname))
    
    fname = '{}DATA_LABELS_{}.csv'.format(project_name, ts)
    export_to_file(PROJECT_DATA, url, token, os.path.join(outdir,fname))
