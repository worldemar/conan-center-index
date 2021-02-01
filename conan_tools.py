#!/usr/bin/env python

from os import path

class PackageReference(object):
    def _possible_conanfile_locations(self, name, version):
        return [
            path.join("recipes", name, version, "conanfile.py"),
            path.join("recipes", name, "all", "conanfile.py"),
        ]

    def __init__(self, conan, strref):
        self.conan = conan
        if "/" not in strref:
            raise RuntimeError("package reference '%s' does not contain slash" % strref)
        self.name, self.version = strref.split("/")
        self.conanfile_path = None
        for loc in self._possible_conanfile_locations(self.name, self.version):
            if path.isfile(loc):
                self.conanfile_path = loc
        if not self.conanfile_path:
            print("conanfile.py not found at %s" % self._possible_conanfile_locations)
            raise RuntimeError("Recipe for package %s could not be found" % (self.name + "/" + self.version))
        self.conanfile = open(self.conanfile_path, "rb").read()

    def export(self):
        self.conan.export([self.conanfile_path, self.name + "/" + self.version + "@_/_"])

    def __str__(self):
        return "%s-%s :: %s" % (
            self.name,
            self.version,
            self.conanfile_path
        )

class ConanfileTxt(object):
    def __init__(self, conan, filename):
        self.conan = conan
        self.packages = []
        if path.isfile(filename):
            for line in open(filename, "rb").read().splitlines():
                strline = line.decode("ascii")
                if not self._is_package_reference(strline):
                    continue
                self.packages.append(PackageReference(conan, strline))

    def _is_package_reference(self, line):
        if line.startswith("#"):
            return False
        if "# disable GHA" in line:
            return False
        if "/sdk120" in line:
            return False
        if "/sdkARM" in line:
            return False
        if "/system" in line:
            return False
        if "@" in line:
            return False
        if "/" not in line:
            return False
        return True

    def export(self):
        for package in self.packages:
            package.export()

def list_installed_packages(conan):
    installed_packages = []
    conan.search(["--json", "installed.json", "*"])
    installed = json.load(open("installed.json","r"))
    if installed["results"]:
        for p in installed["results"][0]["items"]:
            installed_packages.append(p["recipe"]["id"])
    return installed_packages
