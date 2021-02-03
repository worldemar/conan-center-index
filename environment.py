#!/usr/bin/env python

from os import environ
from conans.client.command import Command
from conans.client.conan_api import Conan

def prepare_environment():
    dev_repo = False
    # these interfere with conan commands
    if "CONAN_USERNAME" in environ:
        if environ["CONAN_USERNAME"] == "worldemar":
            dev_repo = True
        del environ["CONAN_USERNAME"]
    if "CONAN_CHANNEL" in environ:
        del environ["CONAN_CHANNEL"]

    conan = Command(Conan())

    conan.config(["install", "https://github.com/trassir/conan-config.git"])

    # TODO: delete this after https://github.com/trassir/conan-config/pull/11
    conan.remote(["remove", "bintray-trassir"])

    if dev_repo:
        # allow download from official repos
        conan.remote(["add", "org-trassir-staging", "https://api.bintray.com/conan/trassir/conan-staging", "True"])
        conan.remote(["add", "org-trassir-public", "https://api.bintray.com/conan/trassir/conan-public", "True"])
        conan.remote(["add", "conan-center", "https://conan.bintray.com", "True"])
        # use unofficial repos for dev repo
        conan.remote(["add", "trassir-staging", "https://api.bintray.com/conan/worldemar/cci-pr", "True"])
        conan.remote(["add", "trassir-public", "https://api.bintray.com/conan/worldemar/cci-master", "True"])
    else:
        conan.remote(["add", "trassir-staging", "https://api.bintray.com/conan/trassir/conan-staging", "True"])
        conan.remote(["add", "trassir-public", "https://api.bintray.com/conan/trassir/conan-public", "True"])
        conan.remote(["add", "conan-center", "https://conan.bintray.com", "True"])

    if environ.get("GITHUB_HEAD_REF", "master") == "master":
        upload_remote = "trassir-public"
    else:
        upload_remote = "trassir-staging"

    if dev_repo:
        if "CONAN_PASSWORD" in environ:
            conan.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "worldemar"])
    else:
        if "CONAN_PASSWORD" in environ:
            conan.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "trassir-ci-bot"])

    return conan, upload_remote
