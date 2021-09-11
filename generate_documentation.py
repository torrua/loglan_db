# -*- coding: utf-8 -*-
"""
Generate HTML docs
"""

import os
import shutil

import pdoc

from loglan_db import run_with_context

DEFAULT_OUTPUT_DIRECTORY = "docs"
DEFAULT_PACKAGE_DIRECTORY = "loglan_db"


def ignore_files(directory, files):
    return [file for file in files if os.path.isfile(os.path.join(directory, file))]


def create_structure(
        src: str = DEFAULT_PACKAGE_DIRECTORY,
        dst: str = DEFAULT_OUTPUT_DIRECTORY):
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=ignore_files)


def recursive_html(mod):
    yield mod.name, mod.html(show_source_code=False)
    for sub_mod in mod.submodules():
        yield from recursive_html(sub_mod)


def generate_html(module_name, html, dst: str = DEFAULT_OUTPUT_DIRECTORY):
    line = "\\"
    path = os.path.join(dst, line.join(str(module_name).split('.')[1:]))
    if os.path.exists(path) and os.path.isdir(path):
        path = os.path.join(path, "index")
    with open(f"{path}.html", "w+", encoding='utf-8') as file:
        file.write(html)


def get_package_modules(src: str = DEFAULT_PACKAGE_DIRECTORY) -> list:
    # Public submodules are auto-imported
    context = pdoc.Context()
    modules = [pdoc.Module(mod, context=context)
               for mod in [src, ]]
    pdoc.link_inheritance(context)
    return modules


@run_with_context
def run(
        src: str = DEFAULT_PACKAGE_DIRECTORY,
        dst: str = DEFAULT_OUTPUT_DIRECTORY):

    modules = get_package_modules(src)
    create_structure(src, dst)

    for mod in modules:
        for module_name, html in recursive_html(mod):
            generate_html(module_name, html, dst)


if __name__ == "__main__":
    run()
