import requests
import os
import logging
import argparse
import re

rootURL = "http://hpc.uni-due.de/lnc/cpp/"


def download_file(url: str, file: str) -> bool:
    downloaded = requests.get(url + file)
    if downloaded:
        open(os.path.join(os.getcwd(), file), "wb").write(downloaded.content)
        logging.info("Downloaded " + file)
        return True
    else:
        logging.warning("Could not download " + file)
        return False


def get_file_lines(name: str) -> list:
    filename = os.path.join(os.path.curdir, name)
    if not os.path.exists(filename):
        return []
    file = open(os.path.join(os.path.curdir, name), "r")
    return file.readlines()


def get_makefile_deps() -> list:
    lines = get_file_lines("makefile")
    regex = re.compile("SRC = (.*)\\s")
    for line in lines:
        match = regex.match(line)
        if match:
            deps = match.group(1).split(sep=" ")
            logging.info("Found the following makefile deps: " + str(deps))
            return deps


def get_cpp_deps(cpp_name: str) -> list:
    deps = []
    lines = get_file_lines(cpp_name)
    regex = re.compile("#include\\s+\"(.*)\"\\s")
    regex_glsl = re.compile("\"(\\w*\\.glsl)\"")
    for line in lines:
        match = regex.match(line)
        if match:
            include = match.group(1).strip()
            logging.info("Remembering header dependency " + include)
            deps.append(include)
        match = regex_glsl.findall(line)
        if match:
            logging.info("Remembering GSLS files " + str(match))
            deps.extend(match)

    return deps


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(description="Download Late Night Coding files to current directory")
    parser.add_argument("projectName", type=str, nargs=1, help="Project name like OpenGL", default="OpenGL")
    args = parser.parse_args()

    projectUrl = rootURL + args.projectName[0] + "/"

    if not (download_file(projectUrl, "makefile")):
        logging.error("Could not download makefile. Giving up")
        exit(-1)

    header_deps = set()
    for dep in get_makefile_deps():
        if download_file(projectUrl, dep):
            headers = get_cpp_deps(dep)
            header_deps.update(headers)

    for header in header_deps:
        download_file(projectUrl, str(header))
