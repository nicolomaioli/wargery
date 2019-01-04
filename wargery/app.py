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
        help="Specify build number",
        type=int
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


def get_target_name(build_nr=None):
    """
    Create a file name in the form:
    'project'-'date'-'n'
    """

    path = os.getcwd()
    project_name = os.path.basename(path)
    today = date.today().__str__()
    artifact_name = "{}-{}".format(project_name, today)

    # If a war artifact with the same name already exists, append -n
    glob_list = glob.glob("target/{}*.war".format(artifact_name))

    # -n can also be specified as a parameter
    n = build_nr if build_nr else len(glob_list)

    if (n):
        artifact_name = "{}-{}".format(artifact_name, n)

    return artifact_name


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


def run():
    """
    The function exposed by the public API
    """
    source = get_source_name()
    opt = parse_options()
    target = get_target_name(opt.build_nr)

    cleaned = clean_application()

    if (cleaned.returncode == 0):
        print("Application cleaned, ready to create war artifact")
    else:
        print("Clean failed, returncode: {}".format(cleaned.returncode))
        sys.exit(cleaned.returncode)

    completed = create_war_artifact()

    if (completed.returncode == 0):
        print("War artifact created")
        os.rename("target/{}.war".format(source), "target/{}.war".format(target))
        print("Moved target/{} to target/{}.war".format(source, target))

    else:
        print("Build failed, returncode: {}".format(completed.returncode))
        sys.exit(completed.returncode)

    # Return the path to the war artifact
    return "target/{}.war".format(target)


if __name__ == '__main__':
    run()
