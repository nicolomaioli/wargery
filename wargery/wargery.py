import os
import glob
import sys
from wargery.utils import (
    parse_options,
    get_source_name,
    get_target_name,
    exec_grails_clean,
    exec_grails_war
)


def create_war_artifact(
    name_after_date=False,
    build_nr=None
):
    """
    Wargery's main entry point
    It creates a war artifact from a Grails project and names it something
    sensible.
    """
    print("You have summoned the Wargery")

    source = get_source_name()
    opt = parse_options()
    name_after_date = opt.name_after_date
    build_nr = opt.build_nr
    target = get_target_name(name_after_date, build_nr)

    print("Creating war artifact {}.war".format(target))

    name_after_commit = True

    if opt.name_after_date:
        name_after_commit = False

    if name_after_commit:
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

    returncode = exec_grails_clean()

    if (returncode == 0):
        print("Application cleaned, ready to create war artifact")
    else:
        print("Clean failed, returncode: {}".format(returncode))
        sys.exit(returncode)

    returncode = exec_grails_war()

    if (returncode == 0):
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
        print("Build failed, returncode: {}".format(returncode))
        sys.exit(returncode)

    # Return artifact name
    return "{}.war".format(target)
