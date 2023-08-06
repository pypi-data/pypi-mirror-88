"""CLI interface to kfputils."""
import click
from .pipeline import (
    upload_pipeline,
    _extract_pipeline_name,
    list_pipelines,
    delete_multi,
)
from .run import Runner, _display_run
from .utils import read_params
import json


@click.group()
def pipeline():
    """Pipeline helpers."""
    pass


@pipeline.command()
@click.pass_context
def delete_all(ctx):
    """Delete all current pipelines."""
    client = ctx.obj["client"]
    pipelines = list_pipelines(client)
    if len(pipelines):
        delete_multi(client, pipelines)
        print("[OK] successfully deleted all pipelines")
    else:
        print("[OK] no pipelines to delete")


@pipeline.command()
# @click.option("-p", "--pipeline-name", required=True, help="Name of the pipeline.")
@click.option(
    "-v", "--pipeline-version", help="Name of the pipeline version", default=""
)
@click.option(
    "-f",
    "--package-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the pipeline package file.",
)
@click.option(
    "-e", "--experiment-name", required=True, help="Experiment name of the run."
)
@click.option(
    "-s",
    "--params-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the pipeline yaml params file.",
)
@click.pass_context
def upload_run(
    ctx,
    # pipeline_name,
    package_file,
    experiment_name,
    params_file,
    # output,
    pipeline_version,
):
    """Upload and trigger a run of a KFP pipeline."""
    client = ctx.obj["client"]
    namespace = ctx.obj["namespace"]
    pipeline_name = _extract_pipeline_name(package_file)
    res, new_pipeline = upload_pipeline(
        client, pipeline_name, package_file, pipeline_version
    )
    if res is None:
        raise Exception("Upload failed")
        return
    runner = Runner(client)
    if params_file is not None:
        params = read_params(params_file)
    run = runner.run(res.id, experiment_name, params)
    print("Run {} is submitted".format(run.id))
    _display_run(client, namespace, run.id, True)
    print(f"[OK ] pipeline run successfully for pipeline: {pipeline_name}")
    # pprint("----------------------------")
    # pprint("pipeline run result")
    # pprint(res)


@pipeline.command()
# @click.option("-p", "--pipeline-name", required=True, help="Name of the pipeline.")
@click.option(
    "-v", "--pipeline-version", help="Name of the pipeline version", default=""
)
@click.option(
    "-f",
    "--package-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the pipeline package file.",
)
@click.option(
    "-o",
    "--output",
    help="output format",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
)
@click.pass_context
def upload(ctx, package_file, output, pipeline_version):
    """Upload a KFP pipeline."""
    client = ctx.obj["client"]
    pipeline_name = _extract_pipeline_name(package_file)
    res, new_pipeline = upload_pipeline(
        client, pipeline_name, package_file, pipeline_version
    )
    if output == json:
        json.dumps(res)
        return

    if new_pipeline:
        print(f"[OK] created first version of pipeline: {pipeline_name}")
    else:
        print(
            f"[OK] created updated version of pipeline: {pipeline_name}, version: {pipeline_version}"
        )

    # pprint("res")
    # pprint(res)
