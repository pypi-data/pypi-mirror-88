###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import os
from os.path import join
import shlex

from pkg_resources import get_distribution, DistributionNotFound
import click
from LbAPCommon import render_yaml, parse_yaml, validate_yaml

from .log_parsing import show_log_advice
from .testing import enter_debugging, prepare_reproduce, prepare_test
from .utils import (
    available_productions,
    check_production,
    inside_ap_datapkg,
    logging_subprocess_run,
    validate_environment,
)


class NaturalOrderGroup(click.Group):
    """Group for showing subcommands in the correct order"""

    def list_commands(self, ctx):
        return self.commands.keys()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    for package in ["LbAPLocal", "LbAPCommon", "LbEnv", "LbDiracWrappers"]:
        try:
            version = get_distribution(package).version
        except DistributionNotFound:
            click.secho(f"{package} is not installed", fg="red")
        else:
            click.echo(f"{package} version: {version}")
    ctx.exit()


@click.group(cls=NaturalOrderGroup)
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
def main():
    """Command line tool for the LHCb AnalysisProductions"""
    pass


@main.command()
@click.argument("production_name", type=str, default="", nargs=1)
def list(production_name):
    """List the available production folders by running lb-ap list
    List the available productions for a specific production by running lb-ap list YOUR_PRODUCTION"""
    inside_ap_datapkg()

    if production_name:
        # Check if production exists
        check_production(production_name)
        click.echo(f"The available jobs for {production_name} are: ")

        # Get rendered yaml and find all the production names
        with open(os.path.join(production_name, "info.yaml"), "rt") as fp:
            raw_yaml = fp.read()
        job_names = parse_yaml(render_yaml(raw_yaml))
        for line in job_names:
            click.echo(f"* {line}")
    else:
        click.echo("The available productions are: ")
        for folder in available_productions():
            click.echo(f"* {folder}")


@main.command()
@click.argument("production_name", type=str, nargs=1)
def render(production_name):
    """Render the info.yaml for a given production"""
    inside_ap_datapkg()

    # Check if production exists
    check_production(production_name)

    # Get rendered yaml and print
    click.secho(f"Rendering info.yaml for {production_name}", fg="green")
    with open(os.path.join(production_name, "info.yaml"), "rt") as fp:
        raw_yaml = fp.read()
    render = render_yaml(raw_yaml)
    click.echo(render)
    try:
        job_data = parse_yaml(render)
        validate_yaml(job_data, ".", production_name)
    except Exception:
        click.secho("Rendered YAML has errors!", fg="red")
        click.secho(f'See "lb-ap validate {production_name}" for details', fg="red")
        raise click.ClickException("Failed to parse and valate YAML")
    else:
        click.secho("YAML parsed and validated successfully", fg="green")


@main.command()
@click.argument("production_name", type=str, nargs=1)
def validate(production_name):
    """Validate the configuration for a given production"""
    inside_ap_datapkg()

    # Check if production exists
    check_production(production_name)

    # Get rendered yaml and print
    click.secho(f"Rendering info.yaml for {production_name}", fg="green")
    with open(os.path.join(production_name, "info.yaml"), "rt") as fp:
        raw_yaml = fp.read()
    render = render_yaml(raw_yaml)

    try:
        job_data = parse_yaml(render)
    except Exception as e:
        click.secho("Error parsing YAML!", fg="red")
        raise click.ClickException(str(e))
    else:
        click.secho("YAML parsed successfully", fg="green")

    try:
        validate_yaml(job_data, ".", production_name)
    except Exception as e:
        click.secho("Error validating YAML!", fg="red")
        raise click.ClickException(str(e))
    else:
        click.secho("YAML validated successfully", fg="green")


@main.command()
@click.argument("production_name", type=str, nargs=1)
@click.argument("job_name", type=str, nargs=1)
def test(production_name, job_name):
    """Execute a job locally"""
    validate_environment()
    inside_ap_datapkg()

    out_dir, env_cmd, gaudi_cmd = prepare_test(production_name, job_name)
    cmd = env_cmd + gaudi_cmd
    click.secho(f"Starting lb-run with: {shlex.join(cmd)}", fg="green")
    result = logging_subprocess_run(cmd, cwd=out_dir)

    with open(join(out_dir, "stdout.log"), "wb") as fp:
        fp.write(result.stdout)

    with open(join(out_dir, "stderr.log"), "wb") as fp:
        fp.write(result.stderr)

    click.secho("Summary of log messages:", fg="green")
    show_log_advice(result.stdout.decode() + "\n" + result.stderr.decode())

    if result.returncode != 0:
        raise click.ClickException("Execution failed, see above for details")

    click.secho(f"Success! Output can be found in {out_dir}", fg="green")


@main.command()
@click.argument("production_name", type=str, nargs=1)
@click.argument("job_name", type=str, nargs=1)
def debug(production_name, job_name):
    """Start an interactive session inside the job's environment"""
    validate_environment()
    inside_ap_datapkg()

    enter_debugging(*prepare_test(production_name, job_name))


@main.command()
@click.argument("pipeline_id", type=int, nargs=1)
@click.argument("production_name", type=str, nargs=1)
@click.argument("job_name", type=str, nargs=1)
@click.argument("test_id", type=str, nargs=1, default="latest")
def reproduce(pipeline_id, production_name, job_name, test_id):
    """Reproduce an existing online test locally"""
    validate_environment()
    enter_debugging(*prepare_reproduce(pipeline_id, production_name, job_name, test_id))


@main.command()
@click.argument("log_fn", type=click.Path(exists=True))
@click.option(
    "--suppress",
    type=int,
    default=5,
    show_default=True,
    help="Minimum number of instances required to show ERROR and WARNING messages",
)
def parse_log(log_fn, suppress):
    """Read a Gaudi log file and extract information"""
    with open(log_fn, "rt") as fp:
        log_text = fp.read()

    click.echo(f"Summary of log messages in: {log_fn}")
    show_log_advice(log_text, suppress)
