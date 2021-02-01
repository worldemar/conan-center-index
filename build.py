from os import environ, path
import sys
import json
import subprocess
from environment import  prepare_environment
from conan_tools import ConanfileTxt


def verify_packages(conan, installed, expected):
    missing_packages = []
    for package in installed:
        if not is_package_reference(package):
            continue
        if package in expected:
            conan.search([package + "@_/_"])
        else:
            missing_packages.append(package)
    if missing_packages:
        print("Some packages were installed (possibly as dependencies) but has no fixed versions in %s:" % environ["CONAN_TXT"])
        print(missing_packages)
        raise RuntimeError("Not all requirements have specified versions in %s" % environ["CONAN_TXT"])



def diff_to_master():
    changed_files = []
    diff = subprocess.check_output("git diff master")
    for line in diff.decode("utf-8").splitlines():
        if line.startswith("diff --git a/"):
            two_files = line[len("diff --git a/"):]
            changed_files.append(two_files.split(" b/")[0])
    return changed_files

def collect_dependencies(branch_name):
    subprocess.check_call(["git", "checkout", branch_name])
    return ConanfileTxt(conan, environ["CONAN_TXT"])

def print_section(message):
    print("=" * 80)
    print("   " + message)
    print("=" * 80)

if __name__ == "__main__":
    conan, upload_remote = prepare_environment()

    print_section("Collect packages info from branch 'master'")

    subprocess.check_call(["git", "checkout", "master"])
    conanfile_txt_master = collect_dependencies("master")
    print("Collected %d packages:" % len(conanfile_txt_master.packages))
    for p in conanfile_txt_master.packages:
        print(p)

    print_section("Collect packages info from branch '%s'" % environ.get("GITHUB_HEAD_REF"))

    subprocess.check_call(["git", "checkout", environ.get("GITHUB_HEAD_REF")])
    conanfile_txt_head = collect_dependencies(environ.get("GITHUB_HEAD_REF"))
    print("Collected %d packages:" % len(conanfile_txt_head.packages))
    for p in conanfile_txt_head.packages:
        print(p)

    sys.exit(0)

    expected_packages = packages_from_conanfile_txt(conan)
    for p in expected_packages:
        p.export()

    conan.install([environ["CONAN_TXT"],
                    "-if", "install_dir",
                    "-pr", environ["CONAN_PROFILE"],
                    "-s", "build_type=Release",
                    "--build", "missing"])

    installed = list_installed_packages(conan)
    verify_packages(conan, installed, expected_packages)

    if installed:
        conan.upload(["--confirm", "--force", "--all", "-r", upload_remote, "*"])
