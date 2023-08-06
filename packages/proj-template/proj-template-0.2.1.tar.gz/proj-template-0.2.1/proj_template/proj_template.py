"""Create a setup.cfg file from a template."""

import os
from urllib.request import urlopen
from datetime import datetime
import yaml


def create_project(config):
    """Create project."""
    config["year"] = datetime.now().strftime("%Y")
    config.setdefault("extra", {"line-length": 80, "max-complexity": 12})
    tgt_dir = config["project"]["name"]
    create_root = config.get("__create_root", True)
    root_dir = tgt_dir if create_root else "."
    pkg_dir = os.path.join(root_dir, tgt_dir)

    create_project_dirs(root_dir, tgt_dir)

    config["license_classifier"] = build_copying(root_dir, config)

    code_templates = [
        ("_main.py.in", "{pkg_dir}/__main__.py"),
        ("_init.py.in", "{pkg_dir}/__init__.py"),
        ("_setup.py.in", "{root_dir}/setup.py"),
        ("_setup.cfg.in", "{root_dir}/setup.cfg"),
        ("_gitignore.in", "{root_dir}/.gitignore"),
    ]

    # fix list formating of requires setup.cfg items.
    # NOTE: This is a very dirty hack, it should be reimplemented as plugins.
    defaults = {
        "dev": ["pre-commit, black"],
        "test": ["behave", "pytest", "coverage"],
        "lint": ["pydocstyle", "flake8", "pylint"],
    }
    reqs = config.setdefault("requires", {})
    for req in ["install", "dev", "test", "lint"]:
        opts = reqs.get(req, defaults.get(req, []))
        if "%defaults" in opts:
            opts.remove("%defaults")
            opts.extend(defaults.get(req, []))
        reqs[req] = "\n\t".join(set(opts))

    for src, dst in code_templates:
        with open(os.path.join(config["template_dir"], src), "rt") as srcfile:
            dst = dst.format(pkg_dir=pkg_dir, root_dir=root_dir)
            with open(dst, "wt") as outfile:
                data = srcfile.read()
                print(data.format(**config), end="", file=outfile)


def create_project_dirs(root_dir, target_dir):
    """Create project directories in the target_dir."""
    os.makedirs(os.path.join(root_dir, target_dir), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "tests"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "features/steps"), exist_ok=True)


def build_copying(root_dir, config):
    """Generateproper  COPYING file on target_dir."""

    licenses_path = os.path.join(config["template_dir"], "licenses")

    with open(
        os.path.join(licenses_path, "licenses.yml"), "rt"
    ) as license_file:
        licenses = yaml.safe_load(license_file.read())

    license = licenses.get(config["project"].get("license", "GPLv3"))
    classifier = license["classifier"]
    text = license["location"]

    if text.startswith("https:"):
        text = urlopen(text).read()
        if isinstance(text, bytes):
            text = text.decode("utf-8")
    elif text.startswith("template:"):
        fname = text.split(":", 1)[1]
        with open(os.path.join(licenses_path, fname), "rt") as input_file:
            text = input_file.read()
    with open(os.path.join(root_dir, "COPYING"), "wt") as license_file:
        print(text.format(**config), file=license_file)
    return classifier
