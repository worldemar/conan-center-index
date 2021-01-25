from os import environ, path
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
    if not "/" in line:
        return False
    return True

def export_referenced_recipes(conan):
    have_packages = False
    for line in open(environ["CONAN_TXT"], "rb").read().splitlines():
        strline = line.decode("ascii")
        if not is_package_reference(strline):
            continue

        package, version = strline.split("/")

        conanfile_location = locate_conanfile_for_package(package, version)
        if not conanfile_location:
            raise RuntimeError("Could not find recipe for package ref %s" % strline)

        conan.export([conanfile_location, package + "/" + version + "@_/_"])
        have_packages = True
    return have_packages


if __name__ == "__main__":
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
    conan.remote(["add", "conan-center", "https://conan.bintray.com", "True"])

    if environ.get("GITHUB_HEAD_REF", "master") == "master":
        upload_remote = "trassir-public"
    else:
        upload_remote = "trassir-staging"

    expect_packages = export_referenced_recipes(conan)

    conan.install([environ["CONAN_TXT"],
                    "-if", "install_dir",
                    "-pr", environ["CONAN_PROFILE"],
                    "-s", "build_type=Release",
                    "--build", "missing"])
    conan.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "trassir-ci-bot"])
    conan.search(["*"])
    try:
        conan.upload(["--confirm", "--force", "--all", "-r", upload_remote, "*"])
    except NotFoundException:
        if expect_packages:
            raise
