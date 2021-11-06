import subprocess
from os import path
from shutil import copyfile

from flask import Blueprint, abort, current_app, g, json, request
from git import InvalidGitRepositoryError
from git.repo import Repo

from .utils import is_valid_signature, request_from_github

deploy = Blueprint("deploy", __name__)


@deploy.route("/deploy", methods=["GET", "POST"])
@request_from_github()
def deploy_from_github():
    """Deploy the GitHub request to the test platform."""
    abort_code = 418
    config = current_app.config

    event = request.headers.get("X-GitHub-Event")
    if event == "ping":
        g.log.info("deploy endpoint pinged!")
        return json.dumps({"msg": "Hi!"})
    if event != "push":
        g.log.info("deploy endpoint received unaccepted push request!")
        return json.dumps({"msg": "Wrong event type"})

    x_hub_signature = request.headers.get("X-Hub-Signature")
    # web hook content type should be application/json for request.data to have the payload
    # request.data is empty in case of x-www-form-urlencoded
    if not is_valid_signature(x_hub_signature, request.data, g.github["deploy_key"]):
        g.log.warning(f"Deploy signature failed: {x_hub_signature}")
        abort(abort_code)

    payload = request.get_json()
    if payload is None:
        g.log.warning(f"Deploy payload is empty: {payload}")
        abort(abort_code)

    if payload["ref"] != "refs/heads/master":
        return json.dumps({"msg": "Not master; ignoring"})

    try:
        repo = Repo(config["INSTALL_FOLDER"])
    except InvalidGitRepositoryError:
        return json.dumps({"msg": "Folder is not a valid git directory"})

    try:
        origin = repo.remote("origin")
    except ValueError:
        return json.dumps({"msg": "Remote origin does not exist"})

    fetch_info = origin.fetch()
    if len(fetch_info) == 0:
        return json.dumps({"msg": "Didn't fetch any information from remote!"})

    pull_info = origin.pull()

    if len(pull_info) == 0:
        return json.dumps({"msg": "Didn't pull any information from remote!"})

    if pull_info[0].flags > 128:
        return json.dumps({"msg": "Didn't pull any information from remote!"})

    commit_hash = pull_info[0].commit.hexsha
    build_commit = f'build_commit = "{commit_hash}"'
    with open("build_commit.py", "w") as f:
        f.write(build_commit)

    run_ci_repo = path.join(
        config["INSTALL_FOLDER"], "install", "ci-vm", "ci-linux", "ci", "runCI"
    )
    run_ci_nfs = path.join(
        config["SAMPLE_REPOSITORY"],
        "vm_data",
        config["KVM_LINUX_NAME"],
        "runCI",
    )
    copyfile(run_ci_repo, run_ci_nfs)

    g.log.info(f"Platform upgraded to commit {commit_hash}")
    subprocess.Popen(["sudo", "service", "platform", "reload"])
    g.log.info("Sample platform synced with GitHub!")
    return json.dumps({"msg": f"Platform upgraded to commit {commit_hash}"})
