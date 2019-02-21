import os
import glob
import subprocess
import re
import sys
import argparse
from datetime import date


def parse_options():
    parser = argparse.ArgumentParser(
        description="Create a sensibly named war artifact from a Grails project"
    )

    parser.add_argument(
        "--build-nr",
        dest="build_nr",
        nargs=1,
        help="Specify build number",
        type=int
    )

    parser.add_argument(
        "--name-after-commit",
        "-c",
        dest="name_after_commit",
        default=False,
        action="store_true",
        help="Name artifact after current commit (short) hash"
    )

    return parser.parse_args()


def parse_application_properties():
    """
    Parse the application.properties file
    """

    p = re.compile('^#')
    d = {}

    if not (glob.glob('application.properties')):
        print("No 'application.properties' file found.")
        sys.exit(1)

    with open('application.properties', 'r') as file:
        for line in file:

            if (p.match(line)):
                pass
            else:
                line = line.rstrip('\n')
                split = line.split('=')
                d[split[0]] = split[1]

    return d


def get_source_name():
    """
    Create a file name from the application metadata
    """

    d = parse_application_properties()

    return "{}-{}".format(d['app.name'], d['app.version'])


def get_target_name(name_after_commit, build_nr=None):
    """
    Create a file name in the form:
    'project'-'date'-'n'
    """

    path = os.getcwd()
    project_name = os.path.basename(path)

    if name_after_commit:
        artifact_name = name_with_commit(project_name)
    else:
        artifact_name = name_with_date(project_name, build_nr)

    return artifact_name


def name_with_date(project_name, build_nr=None):
    """
    Create a file name in the form:
    'project'-'date'-'n'
    """
    today = date.today().__str__()
    artifact_name = "{}-{}".format(project_name, today)

    # If a war artifact with the same name already exists, append -n
    glob_list = glob.glob(
        os.path.join(
            "target",
            "{}*.war".format(artifact_name)
        )
    )

    # -n can also be specified as a parameter
    n = build_nr if build_nr else len(glob_list)

    if (n):
        artifact_name = "{}-{}".format(artifact_name, n)

    return artifact_name


def check_git():
    """
    Check if the current directory is a git repository
    """
    cmd = ["git", "rev-parse", "--git-dir"]
    completed = subprocess.run(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return True if completed.returncode == 0 else False


def name_with_commit(project_name):
    """
    Create a file name in the form:
    'project'-'commit hash'-'n'
    """
    is_git_repository = check_git()

    if is_git_repository:
        completed = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8')

        commit = completed.stdout.rstrip()
        return "{}-{}".format(project_name, commit)
    else:
        print("The current directory is not a git repository")
        sys.exit(1)


def clean_application():
    """
    Run 'grails clean'
    """

    try:
        return subprocess.run(["grails", "clean"])
    except FileNotFoundError:
        print("Grails is not installed.")
        sys.exit(1)


def create_war_artifact():
    """
    Run 'grails war'
    """

    try:
        return subprocess.run(["grails", "war"])
    except FileNotFoundError:
        print("Grails is not installed.")
        sys.exit(1)


def run(config=None):
    """
    The function exposed by the public API
    It takes an optional config object that overrides the parser
    """
    source = get_source_name()

    if config:
        opt = config
    else:
        opt = parse_options()

    target = get_target_name(opt.name_after_commit, opt.build_nr)

    if opt.name_after_commit:
        glob_list = glob.glob(
            os.path.join(
                "target",
                "{}.war".format(target)
            )
        )

        if len(glob_list) > 0:
            print("A war artifact from the current commit already exists")
            print("Skipping war artifact creation and exiting now.")
            return "{}.war".format(target)

    cleaned = clean_application()

    if (cleaned.returncode == 0):
        print("Application cleaned, ready to create war artifact")
    else:
        print("Clean failed, returncode: {}".format(cleaned.returncode))
        sys.exit(cleaned.returncode)

    completed = create_war_artifact()

    if (completed.returncode == 0):
        print("War artifact created")
        os.rename(
            os.path.join(
                "target",
                "{}.war".format(source)
            ),
            os.path.join(
                "target",
                "{}.war".format(target)
            )
        )
        print("Moved target/{} to target/{}.war".format(source, target))

    else:
        print("Build failed, returncode: {}".format(completed.returncode))
        sys.exit(completed.returncode)

    # Return artifact name
    return "{}.war".format(target)


if __name__ == '__main__':
    run()
