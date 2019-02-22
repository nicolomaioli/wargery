import os
import glob
import re
import sys
import argparse
from subprocess import Popen, PIPE
from datetime import date


def parse_options():
    parser = argparse.ArgumentParser(
        description="Create a sensibly named war artifact from a Grails project"
    )

    parser.add_argument(
        "-d",
        "--name-after-date",
        dest="name_after_date",
        default=False,
        action="store_true",
        help="Name artifact after current date"
    )

    parser.add_argument(
        "-b",
        "--build-nr",
        dest="build_nr",
        default=None,
        help="Specify build number (only valid with '-d')",
        type=int
    )

    return parser.parse_args()


def parse_application_properties():
    """
    Parse the application.properties file
    """

    skip_comment = re.compile('^#')
    application_properties = {}

    if not (glob.glob('application.properties')):
        print("No 'application.properties' file found.")
        sys.exit(1)

    with open('application.properties', 'r') as file:
        for line in file:

            if (skip_comment.match(line)):
                pass
            else:
                line = line.rstrip('\n')
                split = line.split('=')
                application_properties[split[0]] = split[1]

    return application_properties


def get_source_name():
    """
    Create a file name from the application metadata
    """

    application_properties = parse_application_properties()

    return "{}-{}".format(
        application_properties['app.name'],
        application_properties['app.version']
    )


def get_target_name(name_after_date, build_nr=None):
    """
    Create a file name in the form:
    'project'-'date'-'n'
    """

    path = os.getcwd()
    project_name = os.path.basename(path)

    if name_after_date:
        artifact_name = name_with_date(project_name, build_nr)
    else:
        artifact_name = name_with_commit(project_name)

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
    returncode = Popen(
        cmd,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).wait()

    return True if returncode == 0 else False


def name_with_commit(project_name):
    """
    Create a file name in the form:
    'project'-'commit hash'-'n'
    """
    is_git_repository = check_git()

    if is_git_repository:
        proc = Popen(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            encoding='utf-8'
        )

        stdout, stderr = proc.communicate()
        commit = stdout.rstrip()
        print("Current commit: {}".format(commit))
        return "{}-{}".format(project_name, commit)
    else:
        print("The current directory is not a git repository")
        sys.exit(1)


def exec_grails_clean():
    """
    Run 'grails clean'
    """

    try:
        return Popen(["grails", "clean"]).wait()
    except FileNotFoundError:
        print("Grails is not installed.")
        sys.exit(1)


def exec_grails_war():
    """
    Run 'grails war'
    """

    try:
        return Popen(["grails", "war"]).wait()
    except FileNotFoundError:
        print("Grails is not installed.")
        sys.exit(1)
