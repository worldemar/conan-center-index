from os import environ, path
import sys
import json
import subprocess
from environment import  prepare_environment
from conan_tools import ConanfileTxt
import hashlib


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

def print_section(message):
    print("=" * 80)
    print("   " + message)
    print("=" * 80)

def collect_dependencies(branch_name):
    subprocess.check_call(["git", "checkout", environ.get("GITHUB_HEAD_REF")])
    conanfile_txt = ConanfileTxt(conan, environ["CONAN_TXT"])
    print("Collected %d packages:" % len(conanfile_txt.packages))
    for _, package in conanfile_txt.packages.items():
        print(package)
    return conanfile_txt

def detect_updated_packages(master_txt, branch_txt):
    """
        Raise error if following requirement is not satisfied:
        "updating conanfile.py must always be done with package version bump"
    """
    for name, package in branch_txt.packages:
        if name not in master_txt.packages.keys():
            print("CONAN_TXT: package added %s" % package)
            continue
        if master_txt.packages[name].conanfile != package.conanfile:
            md5_master = hashlib.md5()
            md5_master.update(master_txt.packages[name].conanfile)
            md5_branch = hashlib.md5()
            md5_branch.update(branch_txt.packages[name].conanfile)
            print("CONAN_TXT: package recipe updated %s:\nmd5(master)=%s\nmd5(branch)=%s" % (
                master_txt.packages[name].conanfile_path,
                md5_master.hexdigest(),
                md5_branch.hexdigest()
                ))
            if master_txt.packages[name].version == package.version:
                print("CONAN_TXT: package recipe updated but version did not: %s-%s" % (
                    package.name,
                    package.version
                    ))
                raise RuntimeError("package recipe updated but version did not")
            print("CONAN_TXT: package version updated: %s-%s => %s-%s" % (
                master_txt.packages[name].name,
                master_txt.packages[name].version,
                package.name,
                package.version
                ))



if __name__ == "__main__":
    conan, upload_remote = prepare_environment()

    print_section("Collect packages info from branch 'master'")

    # subprocess.check_call(["git", "checkout", "master"])
    # conanfile_txt_master = collect_dependencies("master")
    # print("Collected %d packages:" % len(conanfile_txt_master.packages))
    # for name, package in conanfile_txt_master.packages.iteritems():
    #     print(package)

    conanfile_txt_master = ConanfileTxt(conan, environ["CONAN_TXT"] + "-master")
    conanfile_txt_head = collect_dependencies(environ.get("GITHUB_HEAD_REF"))

    detect_updated_packages(conanfile_txt_master, conanfile_txt_head)

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
