from os import environ, path
import json
from conans.client.conan_api import Conan
from conans.client.command import Command
from conans.errors import NotFoundException

def locate_conanfile_for_package(name, version):
    possible_conanfile_locations = [
        path.join("recipes", name, version, "conanfile.py"),
        path.join("recipes", name, "all", "conanfile.py"),
    ]
    for loc in possible_conanfile_locations:
        if path.isfile(loc):
            return loc
    return None

def is_package_reference(line):
    if line.startswith("#"):
        return False
    if "# disable GHA" in line:
        return False
    if "sdk120" in line:
        return False
    if "sdkARM" in line:
        return False
    if "/" not in line:
        return False
    return True

def packages_from_conanfile_txt():
    packages = []
    for line in open(environ["CONAN_TXT"], "rb").read().splitlines():
        strline = line.decode("ascii")
        if not is_package_reference(strline):
            continue

        if "@" in strline:
            package_ref = strline.split("@")[0]
        else:
            package_ref = strline
        packages.append(package_ref)
    return packages

def export_referenced_conanfiles(conan, packages):
    for package_ref in packages:
        package, version = package_ref.split("/")

        conanfile_location = locate_conanfile_for_package(package, version)
        if not conanfile_location:
            raise RuntimeError("Could not find recipe for package line %s" % package_ref)

        conan.export([conanfile_location, package + "/" + version + "@_/_"])

def list_installed_packages(conan):
    installed_packages = []
    conan.search(["--json", "installed.json", "*"])
    installed = json.load(open("installed.json","r"))
    if installed["results"]:
        for p in installed["results"][0]["items"]:
            installed_packages.append(p["recipe"]["id"])
    return installed_packages

def verify_packages(conan, installed, expected):
    missing_packages = []
    for package in installed:
        if package not in expected:
            missing_packages.append(package)
        else:
            print("Ready for upload %s" % package)
            # conan.info([package + "@_/_"])
    if missing_packages:
        print("Some packages were installed (possibly as dependencies) but has no fixed versions in %s:" % environ["CONAN_TXT"])
        print(missing_packages)
        raise RuntimeError("Not all requirements have specified versions in %s" % environ["CONAN_TXT"])

def prepare_conan():
    # these interfere with conan commands
    if "CONAN_USERNAME" in environ:
        del environ["CONAN_USERNAME"]
    if "CONAN_CHANNEL" in environ:
        del environ["CONAN_CHANNEL"]

    conan = Command(Conan())

    conan.config(["install", "https://github.com/trassir/conan-config.git"])

    # TODO: delete this after https://github.com/trassir/conan-config/pull/11
    conan.remote(["remove", "bintray-trassir"])

    conan.remote(["add", "trassir-staging", "https://api.bintray.com/conan/trassir/conan-staging", "True"])
    conan.remote(["add", "trassir-public", "https://api.bintray.com/conan/trassir/conan-public", "True"])
    # conan.remote(["add", "conan-center", "https://conan.bintray.com", "True"])

    if environ.get("GITHUB_HEAD_REF", "master") == "master":
        upload_remote = "trassir-public"
    else:
        upload_remote = "trassir-staging"

    if "CONAN_PASSWORD" in environ:
        conan.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "trassir-ci-bot"])
    return conan, upload_remote


if __name__ == "__main__":
    conan, upload_remote = prepare_conan()

    expected_packages = packages_from_conanfile_txt()
    export_referenced_conanfiles(conan, expected_packages)

    conan.install([environ["CONAN_TXT"],
                    "-if", "install_dir",
                    "-pr", environ["CONAN_PROFILE"],
                    "-s", "build_type=Release",
                    "--build", "missing"])

    installed = list_installed_packages(conan)
    verify_packages(conan, installed, expected_packages)

    if installed:
        conan.upload(["--confirm", "--force", "--all", "-r", upload_remote, "*"])
