#Copyright STACKEO - INRIA 2020
# pylint: disable=redefined-builtin,broad-except

from __future__ import print_function

import json
import os
import sys
import shutil
import tempfile
import zipfile
from io import BytesIO

import click
import requests

from jinja2 import Environment, FileSystemLoader
from jsonschema import ValidationError
from prettytable import PrettyTable
from yaml.scanner import ScannerError

from Stkml.Diagram.Map.RegionNotFound import RegionNotFound
from Stkml.Drawio import DrawIO
from Stkml.Stkml import Stkml, StkmlSyntaxicErrorList, ModelException
from Stkml.Diagram import  StkmlDiagram
from Stkml import MODULE_DIR, __version__, STACKIHUB_URL, STKML_PACKAGES
from Stkml.Stkml.PackageZip import PackageZip
from Stkml.Stkml.StkmlPackage import StkmlPackage

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


CONTEXT_SETTINGS = {'help_option_names':['-h', '--help']}
ICONS = os.path.join(MODULE_DIR, 'templates/diagram/resources/')
@click.group()
@click.version_option(__version__)
def cli():
    latest_version = get_stkml_latest_version()
    if latest_version:
        if __version__ != latest_version:
            click.secho(f"""[WARN] deprecated stkml@{__version__}: stkml@<{latest_version}\
 is no longer maintained. Upgrade to stkml@^{latest_version} using\
"pip install --upgrade stkml" """,
                        fg='yellow')

@click.command('check', help='check a Stkml project', context_settings=CONTEXT_SETTINGS)
@click.argument('stkmlfolder')
@click.option('--disable-syntax-verification', '-d', help='ignore syntax verification', is_flag=True)
def check(stkmlfolder: str, disable_syntax_verification: bool) -> None:
    stkml, _ = create_stkml(stkmlfolder)
    try:
        check_stkml(stkml, disable_syntax_verification)
    except click.ClickException as error:
        click.secho(f"[ERROR] {error}", fg='red')
        sys.exit(1)
    else:
        click.secho("[SUCCESS] Project checked successfully", fg='green')


@click.group('compile', help='compile a Stkml project using a specific backend',
             context_settings=CONTEXT_SETTINGS)
@click.argument('stkmlproject')
@click.option('--disable-syntax-verification', '-d', help='ignore syntax verification', is_flag=True)
@click.pass_context
def compile(ctx: click.Context, stkmlproject: str, disable_syntax_verification: bool) -> None:
    if stkmlproject:
        stkml, working_dir = create_stkml(stkmlproject)
        try:
            check_stkml(stkml, disable_syntax_verification)
        except click.ClickException as error:
            click.secho(f"[ERROR] {error}", fg='red')
            sys.exit(1)
        try:
            warns = stkml.create_architecture()
        except ModelException as error:
            click.secho(f"[ERROR] {error} ", fg='red')
            sys.exit(1)
        else:
            for warn in warns:
                click.secho(f"[WARN] File Not Found on  {warn} ", fg='yellow')
        ctx.ensure_object(dict)
        ctx.obj['Stkml'] = stkml
        ctx.obj['working_dir'] = working_dir

@click.command('diagram', short_help='compile a Stkml project for diagram', context_settings=CONTEXT_SETTINGS)
@click.option('--type', '-t', 'type', help='the diagram type {Architecture ,Topology or Map}',
              required=True, type=click.Choice(['1', '2', '3']))
@click.option('--output', '-o', 'outputfile', required=True, help='the output file')
@click.pass_context
def diagram(ctx: click.Context, type: str, outputfile: str) -> None:
    """
    compile Stkml file for diagram

    Example:
    \b
        Stkml compile stkml_project diagram -t 1 -o img
    """
    if which('dot'):
        stkml = ctx.obj['Stkml']
        working_dir = ctx.obj['working_dir']
        outputfile = os.path.join(working_dir, outputfile)
        diagram_ = StkmlDiagram()
        try:
            result = diagram_.diagram_from_stkml(type_=int(type),
                                                   stkml=stkml, output=outputfile)
        except FileNotFoundError as error:
            click.secho(f"[ERROR] {error} ", fg='red')
        except RegionNotFound as error:
            click.secho(f"[ERROR] {error} ", fg='red')
        else:
            if result:
                click.secho(result.rstrip().replace('Warning:', '[WARN]'), fg='yellow')
            click.secho("[SUCCESS] Compilation completed successfully", fg='green')
    else:
        click.secho("""[WARN] failed to execute 'dot',
                    make sure the Graphviz 'https://www.graphviz.org/' executables are on your systems' PATH""",
                    fg='yellow')


@click.command('drawio', short_help='compile a Stkml project for Drawio', context_settings=CONTEXT_SETTINGS)
@click.option('--level', '-l', 'level', help='the diagram view level {System View or Layer View}', required=True,
              type=click.Choice(['1', '2']))
@click.option('--icons', '-i', 'icons', default=ICONS, help='the icon folder {it contains [Node_Id].png files}')
@click.option('--output', '-o', 'outputfile', required=True, help='the output file')
@click.pass_context
def drawio(ctx: click.Context, level: str, icons: str, outputfile: str) -> None:
    """
    compile Stkml file for Drawio

    Example:
    \b
        Stkml compile stkml_project Drawio -l 1 -o Drawio
    """

    stkml = ctx.obj['Stkml']
    working_dir = ctx.obj['working_dir']
    outputfile = os.path.join(working_dir, outputfile)
    template_dir = os.path.join(MODULE_DIR, 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    drawio_ = DrawIO(default_icons=ICONS, icons=icons)
    erreur = drawio_.from_stkml(stkml)
    if erreur:
        click.secho(f"[Error] {erreur} ", fg='red')
        sys.exit(1)
    warnings = drawio_.generate_drawio_diagram(output=outputfile, env=env, level=int(level))
    if len(warnings) > 0:
        for warn in warnings:
            click.secho(f"[WARN] {warn} ", fg='yellow')

    click.secho("[SUCCESS] Compilation completed successfully", fg='green')



@click.command('init', help='initialize a Stkml project', context_settings=CONTEXT_SETTINGS)
@click.argument('stkmldir')
def init(stkmldir: str) -> None:
    working_dir = os.path.realpath(os.getcwd())
    project_dir = check_folder_empty(working_dir, stkmldir)
    if project_dir:
        template_dir = os.path.join(MODULE_DIR, 'templates')
        stkml = Stkml()
        stkml.topology.name = click.prompt('Enter the system Name', type=str)
        stkml.topology.usecase = click.prompt('Enter the system use case', type=str)
        env = Environment(loader=FileSystemLoader(template_dir))
        output = stkml.generate_files(environment=env)
        outputfile = os.path.join(project_dir, 'main.stkml.yaml')
        with open(outputfile, 'w') as stkml_file:
            stkml_file.write(output)
        click.secho("[SUCCESS] Stkml project initialized successfully", fg='green')
    else:
        click.secho(f"[ERROR] can not create stkml project on {stkmldir}")


def check_stkml(stkml, disable_syntax_verification):
    try:
        stkml.check_stkml_project()
    except ScannerError as error:
        raise click.ClickException(f'YAML is not valid, {stkml.stkmlfile} {error}')
    except FileNotFoundError as error:
        raise click.ClickException(error.__str__())
    click.secho("[INFO] YAML is valid", fg='blue')
    if disable_syntax_verification:
        click.secho("[INFO] Ignore syntax verification", fg='blue')
    else:
        try:
            stkml.validate_stkml_project()
        except FileNotFoundError as error:
            raise click.ClickException(f'{error} not found')
        except StkmlSyntaxicErrorList as error_list:
            raise click.ClickException(f'Schema validation No\n {error_list}')
        except Exception as error:
            raise click.ClickException(error)
        click.secho("[INFO] Schema validation Ok", fg='blue')

def _check_package(stkml, disable_syntax_verification=False, check_metadata=False):
    try:
        stkml.check_stkml_package(check_metadata)
    except ScannerError as error:
        raise click.ClickException(f'YAML is not valid, {error}')
    except ValidationError as error:
        raise click.ClickException(f'The stkml metadata file is not valid, {error}')
    except FileNotFoundError as error:
        raise click.ClickException(f'{error}')
    click.secho("[INFO] YAML is valid", fg='blue')
    if disable_syntax_verification:
        click.secho("[INFO] Ignore syntax verification", fg='blue')
    else:
        try:
            result = stkml.validate_stkml_package()
        except FileNotFoundError as error:
            raise click.ClickException(f'{error} not found')
        except StkmlSyntaxicErrorList as error_list:
            raise click.ClickException(f'Schema validation No\n {error_list}')
        except Exception as error:
            raise click.ClickException(error)
        else:
            if result is True:
                click.secho("[INFO] Schema validation Ok", fg='blue')
            else:
                click.secho("[ERROR] Cant not find icon(s) :", fg='yellow')
                print_icon_not_found(result)
                sys.exit(1)


def print_icon_not_found(result):
    for key, values in result.items():
        click.secho(f"\t\t{key} : ", fg='yellow')
        for value in values:
            click.secho(f"\t\t\t{value}", fg='yellow')


def create_stkml(stkml_folder, ignore_main=False):
    working_dir = os.path.realpath(os.getcwd())
    stkml_folder = os.path.join(working_dir, stkml_folder)
    if not ignore_main:
        if not os.path.isdir(stkml_folder):
            raise click.BadParameter(message=f'{stkml_folder} doesn\'t exist',
                                     param=stkml_folder, param_hint='--input')
        if not os.path.isfile(os.path.join(stkml_folder, 'main.stkml.yaml')):
            raise click.BadParameter(message=f'{os.path.join(stkml_folder,"main.stkml.yaml") } doesn\'t exist',
                                     param=stkml_folder, param_hint='--input')
    stkml = Stkml(stkml_folder)
    return stkml, working_dir

def check_folder_empty(working_dir, outputdir):
    output_dir = os.path.join(working_dir, outputdir)
    if os.path.isdir(output_dir):
        if len(os.listdir(outputdir)) != 0:
            click.secho(f"[WARN] {output_dir} is not empty", fg='yellow')
            if click.confirm('Do you want to delete its content', abort=False):
                shutil.rmtree(output_dir)
                os.makedirs(output_dir)
                return output_dir
            return None
        return output_dir
    if click.confirm(f'{output_dir} Does not existe, do you want to create it', abort=False):
        os.makedirs(output_dir)
        return output_dir
    return None


def which(program):
    return shutil.which(program)

def get_stkml_latest_version() -> str or None:
    try:
        request = requests.get('https://pypi.org/pypi/stkml/json')
    except requests.exceptions.ConnectionError :
        pass
    else:
        version = None
        if request.status_code == 200:
            stkml_pypi = json.loads(request.content.decode("utf-8"))
            version = list(stkml_pypi['releases'].keys())[-1]
        request.close()
        return version

@click.command('check:package', help='check a Stkml package', context_settings=CONTEXT_SETTINGS)
@click.argument('package_path')
@click.option('--disable-syntax-verification', '-d', help='ignore syntax verification', is_flag=True)
@click.option('--check-metadata', '-m', help='check the package metadata', is_flag=True)
def check_package(package_path: str, disable_syntax_verification: bool, check_metadata: bool) -> None:
    stkml, _ = create_stkml(package_path, ignore_main=True)
    try:
        _check_package(stkml, disable_syntax_verification, check_metadata)
    except Exception as error:
        click.secho(f'[ERROR] {error.__str__()}', fg='red')
        sys.exit(1)
    click.secho("[SUCCESS] Package checked successfully", fg='green')

@click.command('install', help='install a Stkml package from stackhub'
               , context_settings=CONTEXT_SETTINGS)
@click.argument('name')
@click.option('--version', '-v', 'version', help='the version of the package',
              default='latest')
def install(name: str, version: str) -> None:
    packages_dir = create_stkml_packages_folder()
    url = f'{STACKIHUB_URL}files/{name}/{version}'
    try:
        zip = requests.get(url, stream=True)
    except requests.exceptions.ConnectionError as error:
        click.secho(f'[ERROR] can not connect to the {url} {error}', fg='red')
    else:
        if zip.status_code == 200:
            package_path = os.path.join(packages_dir, name)
            create_package_folder(package_path)
            file_bytes = BytesIO(zip.content)
            with PackageZip(file_bytes) as zip_package:
                zip_package.extract_all(package_path)
                click.secho(f'[SUCCESS] {name} has been installed successfully', fg='green')
        else:
            click.secho(f'[ERROR] {name} can not be installed : {zip.reason}', fg='red')

def create_package_folder(package_path):
    if os.path.isdir(package_path):
        shutil.rmtree(package_path)
    os.makedirs(package_path)


def create_stkml_packages_folder() -> str:
    try:
        packages_dir = StkmlPackage.get_packages_dir(os.getcwd())
    except RecursionError:
        packages_dir = os.path.join(os.getcwd(), STKML_PACKAGES)
        os.makedirs(packages_dir)
    return packages_dir





@click.command('search', help='search for a Stkml package on stackhub'
               , context_settings=CONTEXT_SETTINGS)
@click.argument('package')
def search(package):
    url = f'{STACKIHUB_URL}/search?package={package}'
    packages = requests.get(url)
    if packages.status_code == 200:
        packages = packages.json()
        nb_package = len(packages)
        if nb_package > 0:
            click.secho(f'[INFO] {nb_package} package(s) founded', fg='green')
            results_table = PrettyTable(list(packages[0].keys()))
            for pack in packages:
                results_table.add_row(list(pack.values()))
            print(results_table)
        else:
            click.secho(f'[WARN] There are no package similar to {package}', fg='yellow')
    else:
        click.secho(f'[ERROR] can not search for {package} : {packages.reason}')

@click.command('create:package', help='create a stkml package'
               , context_settings=CONTEXT_SETTINGS)
@click.argument('package')
def create_package(package: str):
    working_dir = os.path.realpath(os.getcwd())
    package_dir = check_folder_empty(working_dir, package)
    if package_dir:
        template_dir = os.path.join(MODULE_DIR, 'templates')
        package = StkmlPackage(package_dir)
        package.name = click.prompt('Enter the package''s Name', type=str, default=package.name)
        package.version = click.prompt('Enter the package''s version', type=str, default='1.0.0')
        package.author = click.prompt('Enter the package''s author', type=str, default='anonymous')
        env = Environment(loader=FileSystemLoader(template_dir))
        package.generate_metadata(env)
        click.secho(f"[SUCCESS] {package.name} has been initialized successfully", fg='green')
    else:
        click.secho(f"[ERROR] can not create stkml package on {package}")

@click.command('publish', help='publish a Stkml package to stackhub'
               , context_settings=CONTEXT_SETTINGS)
@click.argument('package')
def publish_package(package: str):
    working_dir = os.path.realpath(os.getcwd())
    package_dir = os.path.join(working_dir, os.path.realpath(package))
    if os.path.isdir(package_dir):
        stkml, _ = create_stkml(package, ignore_main=True)
        try:
            _check_package(stkml, check_metadata=True)
        except Exception as error:
            click.secho(f'[ERROR] {error.__str__()}', fg='red')
            click.secho(f'[ERROR] {package} can not be published because it is invalid', fg='red')
            sys.exit(1)
        click.secho("[INFO] Package checked successfully", fg='blue')
        with tempfile.TemporaryDirectory() as tmpdirname:
            package_zip_name = f'{tmpdirname}/{os.path.basename(package_dir)}.zip'
            with PackageZip(package_zip_name, 'w') as package_zip:
                package_zip.zip(package_dir)
                with open(package_zip_name, 'rb') as zif_file_pointer:
                    url = f'{STACKIHUB_URL}upload/'
                    req = requests.post(url, files={"file": zif_file_pointer})
                    if req.status_code == 200:
                        click.secho(f'[SUCCESS] {package} has been published successfully', fg='green')
                    else:
                        click.secho(f'[ERROR] {package} can not be published because : {req.reason}')
    else:
        click.secho(f"[ERROR] {package} is not package directory", fg='red')



cli.add_command(check)
cli.add_command(compile)
cli.add_command(init)
cli.add_command(check_package)
cli.add_command(install)
cli.add_command(search)
cli.add_command(create_package)
cli.add_command(publish_package)
compile.add_command(diagram)
compile.add_command(drawio)

if __name__ == '__main__':
    cli()
