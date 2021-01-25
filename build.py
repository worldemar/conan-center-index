from os import environ, path
# from cpt.packager import ConanMultiPackager
# from cpt.tools import get_bool_from_env
from conans.client.conan_api import Conan
from conans.client.command import Command

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

def export_referenced_recipes(conan):
    for line in open(environ["CONAN_TXT"], "rb").read().splitlines():
        strline = line.decode("ascii")
        if not is_package_reference(strline):
            continue

        package, version = strline.split("/")

        conanfile_location = locate_conanfile_for_package(package, version)
        if not conanfile_location:
            raise RuntimeError("Could not find recipe for package ref %s" % strline)

        conan.export([conanfile_location])

if __name__ == "__main__":
    # these interfere with conan commands
    if "CONAN_USERNAME" in environ:
        del environ["CONAN_USERNAME"]
    if "CONAN_CHANNEL" in environ:
        del environ["CONAN_CHANNEL"]

    conan = Command(Conan())
    conan.config(["install", "https://github.com/trassir/conan-config.git"])
    conan.remote(["remove", "bintray-trassir"])
    conan.remote(["add", "trassir-staging", "https://api.bintray.com/conan/trassir/conan-staging", "True"])
    conan.remote(["add", "trassir-public", "https://api.bintray.com/conan/trassir/conan-public", "True"])
    conan.remote(["add", "conan-center", "https://conan.bintray.com", "True"])

    if environ.get("GITHUB_HEAD_REF", "master") == "master":
        upload_remote = "trassir-public"
    else:
        upload_remote = "trassir-staging"

    export_referenced_recipes(conan)

    conan.install([environ["CONAN_TXT"],
                    "-if", "install_dir",
                    "-pr", environ["CONAN_PROFILE"],
                    "-s", "build_type=Release",
                    "--build", "missing"])
    conan.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "trassir-ci-bot"])
    conan.upload(["--confirm", "--force", "--all", "-r", upload_remote, "*"])
