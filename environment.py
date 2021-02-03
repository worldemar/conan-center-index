#!/usr/bin/env python

from os import environ
from conans.client.command import Command
from conans.client.conan_api import Conan

def prepare_environment():
    # these interfere with conan commands
    if "CONAN_USERNAME" in environ:
        del environ["CONAN_USERNAME"]
    if "CONAN_CHANNEL" in environ:
        del environ["CONAN_CHANNEL"]

    conan = Command(Conan())

    conan.config(["install", "https://github.com/trassir/conan-config.git"])

    # TODO: delete this after https://github.com/trassir/conan-config/pull/11
    conan.remote(["remove", "bintray-trassir"])

    conan.remote(["add", "org-trassir-staging", "https://api.bintray.com/conan/trassir/conan-staging", "True"])
    conan.remote(["add", "org-trassir-public", "https://api.bintray.com/conan/trassir/conan-public", "True"])
    conan.remote(["add", "trassir-staging", "https://api.bintray.com/conan/worldemar/cci-pr", "True"])
    conan.remote(["add", "trassir-public", "https://api.bintray.com/conan/worldemar/cci-master", "True"])

    conan.remote(["add", "conan-center", "https://conan.bintray.com", "True"])

    if environ.get("GITHUB_HEAD_REF", "master") == "master":
        upload_remote = "trassir-public"
    else:
        upload_remote = "trassir-staging"

    # if "CONAN_PASSWORD" in environ:
    #     conan.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "trassir-ci-bot"])
    if "CONAN_PASSWORD" in environ:
        conan.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "worldemar"])

    return conan, upload_remote
