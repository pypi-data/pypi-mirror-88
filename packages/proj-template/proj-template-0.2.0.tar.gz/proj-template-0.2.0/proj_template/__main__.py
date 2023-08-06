"""CLI entry point for proj-template."""

import os
import sys
import yaml

from pkg_resources import resource_filename

from proj_template.proj_template import create_project


def usage():
    """Display program usage."""
    exe = os.path.basename(sys.argv[0])
    print("usage: %s [-h] [-R] project_cfg" % exe)
    print("\nCreates the basic structure for a Python project.")
    print("\nArguments:")
    print("    project_cfg    project description file")
    print("\nOptions:")
    print("    -h, --help     display this help message")
    print("    -R, --no-root  don't create root directory, use current one.")


def recursive_update(obj, new):
    """Merge a dictionary or a list, recursively."""
    if isinstance(obj, dict):
        for k, v in new.items():
            obj[k] = recursive_update(obj.get(k, None), v)
    elif isinstance(obj, list):
        new = [new] if not (isinstance(new, list)) else new
        obj.extend(new)
    else:
        return new
    return obj


def main():
    """Program entry point."""
    config_file = 0
    create_root = True
    for opt in sys.argv[1:]:
        if opt in ["-h", "--help"]:
            usage()
            sys.exit(0)
        elif opt in ["-R", "--no-root"]:
            create_root = False
        else:
            if bool(config_file):
                print("EROR: Can only create one project.")
                usage()
                sys.exit(1)
            config_file = opt
    project_data = dict(
        __create_root=create_root,
        requires=dict(dev=[], test=[], install=[]),
        style=dict(line_length=80),
        project=dict(version="0.0.1"),
        template_dir=resource_filename("proj_template", "templates")
    )
    with open(config_file, "r") as yaml_file:
        cfg_data = yaml.safe_load(yaml_file)
    create_project(recursive_update(project_data, cfg_data))


if __name__ == "__main__":
    main()
