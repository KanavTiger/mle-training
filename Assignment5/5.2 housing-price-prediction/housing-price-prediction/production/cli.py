import os
import os.path as op
from functools import partial
import mlflow

import click

from ta_lib.core.api import (
    create_context,
    job_planner,
    job_runner,
    list_jobs,
    load_job_processors
)
from training import train_model
HERE = op.dirname(op.abspath(__file__))


@click.group()
@click.option("-c", "--cfg", required=False)
@click.pass_context
def cli(cli_ctx, cfg):
    if cfg is None:
        cfg = os.environ.get("TA_LIB_APP_CONFIG_PATH")
        if cfg is None:
            cfg = os.path.join(HERE, "conf", "config.yml")

    cli_ctx.ensure_object(dict)
    proj_ctxt = create_context(cfg)
    cli_ctx.obj["project_context"] = proj_ctxt


@cli.group()
@click.pass_context
def job(cli_ctx):
    pass


@job.command("list")
@click.pass_context
def _list_jobs(cli_ctx):
    header = "Available jobs"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    for key in list_jobs():
        print(key)


@job.command("run")
@click.option(
    "-j", "--job-id", default="all", help="Id of the job to run",
)
@click.option(
    "-n", "--num-workers", default=1, help="Number of worker processes",
)
@click.option(
    "-t",
    "--num-threads-per-worker",
    default=-1,
    help="Number of threads per each worker process",
)
@click.pass_context
def _run_job(cli_ctx, job_id, num_workers, num_threads_per_worker):
    proj_ctxt = cli_ctx.obj["project_context"]
    job_catalog = proj_ctxt.job_catalog

    init_fn = None
    if num_workers != 1:
        init_fn = partial(load_job_processors, op.dirname(op.abspath(__file__)))

    _completed = False
    for job_spec in job_catalog["jobs"]:
        spec_job_id = job_spec["name"]
        if (job_id != "all") and (spec_job_id != job_id):
            continue

        if spec_job_id == "model-gen":
            for stage in job_spec["stages"]:
                for task in stage["tasks"]:
                    if task["name"] == "train-model":
                        train_model(proj_ctxt, task["params"])
                        _completed = True
                        break
                if _completed:
                    break
            continue

        planner = job_planner.create_job_plan
        job_runner.main(
            proj_ctxt,
            planner,
            job_spec,
            init_fn=init_fn,
            n_workers=num_workers,
            n_threads_per_worker=num_threads_per_worker,
        )
        _completed = True

    if not _completed:
        print(
            f"Invalid job-id : {job_id}. \n\n"
            "Use list sub-command to see available tasks."
        )
        if not _completed:
            print(
                f"Invalid job-id : {job_id}. \n\n"
                "Use list sub-command to see available tasks."
            )


def main():
    mlflow.set_tracking_uri("http://localhost:5000")
    load_job_processors(op.dirname(op.abspath(__file__)))
    cli()


if __name__ == "__main__":
    main()
