from os import environ, path
import sys
import subprocess
from environment import  prepare_environment
from conan_tools import ConanfileTxt, list_installed_packages


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
    subprocess.check_call(["git", "checkout", branch_name])
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
    for name, package in branch_txt.packages.items():
        if name not in master_txt.packages.keys():
            print("CONAN_TXT: package added %s" % package)
            continue
        if master_txt.packages[name].md5sum != package.md5sum:
            print("CONAN_TXT: recipe update detected\npackage(master): %s\npackage(branch): %s" % (
                master_txt.packages[name], package))
            if master_txt.packages[name].version == package.version:
                raise RuntimeError("package recipe updated but version did not")
        else:
            if master_txt.packages[name].version == package.version:
                print("CONAN_TXT: package did not change: %s-%s" % (
                    package.name, package.version ))
            else:
                print("CONAN_TXT: package updated with no recipe changes: %s-%s => %s-%s" % (
                    master_txt.packages[name].name, master_txt.packages[name].version,
                    package.name, package.version))


if __name__ == "__main__":
    conan, upload_remote = prepare_environment()

    print_section("Collect packages info from branches")
    conanfile_txt_master = collect_dependencies("master")
    conanfile_txt_head = collect_dependencies(environ.get("GITHUB_HEAD_REF"))

    print_section("Ensure recipe changes accompanied with version bump")
    detect_updated_packages(conanfile_txt_master, conanfile_txt_head)

    print_section("Exporting all package recipes referenced in %s" % environ["CONAN_TXT"])
    for _, package in conanfile_txt_head.packages.items():
        package.export()

    print_section("Building packages")
    conan.install([environ["CONAN_TXT"],
                    "-if", "install_dir",
                    "-pr", environ["CONAN_PROFILE"],
                    "-s", "build_type=Release",
                    "--build", "missing"])

    print_section("Enumerating installed packages")
    installed = list_installed_packages(conan)

    print_section("Ensure all packages have mention in %s" % environ["CONAN_TXT"])
    for pi in installed:
        name, version = pi.split("/")
        if name not in conanfile_txt_head.packages:
            raise RuntimeError("Package %s is not mentioned in %s" % (name, environ["CONAN_TXT"]))
        if version != conanfile_txt_head.packages[name].version:
            raise RuntimeError("Package %s-%s mentioned in %s with different version %s-%s" % (
                name, version, environ["CONAN_TXT"], name, conanfile_txt_head.packages[name].version))
        package_txt = conanfile_txt_head.packages[name]
        print("Package %s is confirmed by %s as %s-%s" % (
            name, environ["CONAN_TXT"], name, version
            ))

    print_section("Enumerating installed packages")
    conan.upload(["--confirm", "--force", "--all", "-r", upload_remote, "*"])
