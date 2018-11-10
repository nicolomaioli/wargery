import os
import glob
import subprocess
import re
import sys

from datetime import date


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


def get_target_name():
    """
    Create a file name in the form:
    'project'-'date'-'nr'
    """

    path = os.getcwd()
    project_name = os.path.basename(path)
    today = date.today().__str__()
    artifact_name = "{}-{}".format(project_name, today)

    # If a war artifact with the same name already exists, append -n
    glob_list = glob.glob("target/{0}*.war".format(artifact_name))
    if (glob_list):
        artifact_name = "{0}-{1}".format(artifact_name, len(glob_list))

    return artifact_name


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
    source = get_source_name()
    target = get_target_name()
    completed = create_war_artifact()

    if (completed.returncode == 0):
        print("War artifact created")
        os.rename("target/{}.war".format(source), "target/{}.war".format(target))
        print("Moved target/{} to target/{}.war".format(source, target))
    else:
        sys.exit(completed.returncode)


if __name__ == '__main__':
    run()
