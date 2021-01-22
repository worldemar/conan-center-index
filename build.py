from os import environ, path
from sys import exit
# from cpt.packager import ConanMultiPackager
# from cpt.tools import get_bool_from_env
from conans.client.conan_api import Conan
from conans.client.command import Command


# CONAN_USERNAME = trassir
# XCODE_11_DEVELOPER_DIR = /Applications/Xcode_11.7.app/Contents/Developer
# NUNIT3_PATH = /Library/Developer/nunit/3.6.0
# SSH_AUTH_SOCK = /private/tmp/com.apple.launchd.YbPvUVCyLo/Listeners
# DOTNET_ROOT = /Users/runner/.dotnet
# JAVA_HOME = /Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home
# NUNIT_BASE_PATH = /Library/Developer/nunit
# LC_ALL = en_US.UTF-8
# ANDROID_NDK_18R_PATH = /Users/runner/Library/Android/sdk/ndk/18.1.5063045
# _ = /usr/local/opt/runner/provisioner/provisioner
# HOME = /Users/runner
# RCT_NO_LAUNCH_PACKAGER = 1
# ANDROID_SDK_ROOT = /Users/runner/Library/Android/sdk
# JAVA_HOME_11_X64 = /Library/Java/JavaVirtualMachines/adoptopenjdk-11.jdk/Contents/Home
# GITHUB_ACTIONS = true
# VCPKG_INSTALLATION_ROOT = /usr/local/share/vcpkg
# XCODE_12_DEVELOPER_DIR = /Applications/Xcode_12.3.app/Contents/Developer
# CI = true
# DOTNET_MULTILEVEL_LOOKUP = 0
# PIPX_BIN_DIR = /usr/local/opt/pipx_bin
# XPC_SERVICE_NAME = 0
# BOOTSTRAP_HASKELL_NONINTERACTIVE = 1
# CONDA = /usr/local/miniconda
# CHROMEWEBDRIVER = /usr/local/Caskroom/chromedriver/87.0.4280.88
# LANG = en_US.UTF-8
# LC_CTYPE = en_US.UTF-8
# RUNNER_PERFLOG = /usr/local/opt/runner/perflog
# POWERSHELL_DISTRIBUTION_CHANNEL = GitHub-Actions-macos1015
# NVM_CD_FLAGS =
# HOMEBREW_CLEANUP_PERIODIC_FULL_DAYS = 3650
# LOGNAME = runner
# RUNNER_TOOL_CACHE = /Users/runner/hostedtoolcache
# JAVA_HOME_12_X64 = /Library/Java/JavaVirtualMachines/adoptopenjdk-12.jdk/Contents/Home
# NVM_DIR = /Users/runner/.nvm
# RUNNER_TRACKING_ID = github_551bff22-d834-4571-a6f6-04f4666468ee
# PATH = /Users/runner/hostedtoolcache/Python/3.9.1/x64/bin:/Users/runner/hostedtoolcache/Python/3.9.1/x64:/usr/local/opt/pipx_bin:/Users/runner/.cargo/bin:/usr/local/lib/ruby/gems/2.7.0/bin:/usr/local/opt/ruby@2.7/bin:/usr/local/opt/curl/bin:/usr/local/bin:/usr/local/sbin:/Users/runner/bin:/Users/runner/.yarn/bin:/usr/local/go/bin:/Users/runner/Library/Android/sdk/tools:/Users/runner/Library/Android/sdk/platform-tools:/Users/runner/Library/Android/sdk/ndk-bundle:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/usr/bin:/bin:/usr/sbin:/sbin:/Users/runner/.dotnet/tools:/Users/runner/.ghcup/bin:/Users/runner/hostedtoolcache/stack/2.5.1/x64
# GECKOWEBDRIVER = /usr/local/opt/geckodriver/bin
# JAVA_HOME_7_X64 = /Library/Java/JavaVirtualMachines/zulu-7.jdk/Contents/Home
# JAVA_HOME_13_X64 = /Library/Java/JavaVirtualMachines/adoptopenjdk-13.jdk/Contents/Home
# USER = runner
# ANDROID_NDK_HOME = /Users/runner/Library/Android/sdk/ndk-bundle
# JAVA_HOME_14_X64 = /Library/Java/JavaVirtualMachines/adoptopenjdk-14.jdk/Contents/Home
# __CF_USER_TEXT_ENCODING = 0x1F5:0:0
# EDGEWEBDRIVER = /usr/local/share/edge_driver
# XPC_FLAGS = 0x0
# TMPDIR = /var/folders/24/8k48jl6d249_n_qfxwsl6xvm0000gn/T/
# ANDROID_HOME = /Users/runner/Library/Android/sdk
# PIPX_HOME = /usr/local/opt/pipx
# XCODE_10_DEVELOPER_DIR = /Applications/Xcode_10.3.app/Contents/Developer
# JAVA_HOME_8_X64 = /Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home
# PERFLOG_LOCATION_SETTING = RUNNER_PERFLOG
# AGENT_TOOLSDIRECTORY = /Users/runner/hostedtoolcache
# ImageVersion = 20210110.1
# PWD = /
# SHELL = /bin/bash
# HOMEBREW_CASK_OPTS = --no-quarantine
# HOMEBREW_NO_AUTO_UPDATE = 1
# SHLVL = 1
# ImageOS = macos1015
# CONAN_PASSWORD = ***
# IS_PURE_C = true
# pythonLocation = /Users/runner/hostedtoolcache/Python/3.9.1/x64
# CONAN_TXT = conanfile-osx.txt
# CONAN_PR = conanprofile.osx
# MACOSX_DEPLOYMENT_TARGET = 10.14
# CONAN_REFERENCE = zlib/1.2.11
# CONAN_VISUAL_RUNTIMES =
# CONAN_ARCHS = x86_64
# CONAN_BUILD_TYPES = Release
# DEVELOPER_DIR = /Applications/Xcode_11.4.app/Contents/Developer
# INPUT_INSTALL = custom
# INPUT_CUSTOM-PACKAGE = git+https://github.com/trassir/conan-package-tools@log-remotes-before-upload
# INPUT_WORK-DIR = sources/
# INPUT_BUILD-SCRIPT = build.py
# INPUT_COMPILER = apple_clang
# INPUT_COMPILER-VERSIONS = 11.0
# INPUT_DOCKER-IMAGES =
# GITHUB_JOB = zlib_1_2_11
# GITHUB_REF = refs/pull/254/merge
# GITHUB_SHA = 536430ff5e503abc313e2da959f8cc3107d6b705
# GITHUB_REPOSITORY = trassir/conan-center-index
# GITHUB_REPOSITORY_OWNER = trassir
# GITHUB_RUN_ID = 500665240
# GITHUB_RUN_NUMBER = 173
# GITHUB_RETENTION_DAYS = 90
# GITHUB_ACTOR = worldemar
# GITHUB_WORKFLOW = zlib-1.2.11 CI
# GITHUB_HEAD_REF = upload-staging-packages
# GITHUB_BASE_REF = master
# GITHUB_EVENT_NAME = pull_request
# GITHUB_SERVER_URL = https://github.com
# GITHUB_API_URL = https://api.github.com
# GITHUB_GRAPHQL_URL = https://api.github.com/graphql
# GITHUB_WORKSPACE = /Users/runner/work/conan-center-index/conan-center-index
# GITHUB_ACTION = trassirrun-cpt
# GITHUB_EVENT_PATH = /Users/runner/work/_temp/_github_workflow/event.json
# GITHUB_ACTION_REPOSITORY = trassir/run-cpt
# GITHUB_ACTION_REF = v0.2.2-trassir
# GITHUB_PATH = /Users/runner/work/_temp/_runner_file_commands/add_path_ecdb842d-a39f-4aad-87bc-98080b9876a1
# GITHUB_ENV = /Users/runner/work/_temp/_runner_file_commands/set_env_ecdb842d-a39f-4aad-87bc-98080b9876a1
# RUNNER_OS = macOS
# RUNNER_TEMP = /Users/runner/work/_temp
# RUNNER_WORKSPACE = /Users/runner/work/conan-center-index
# ACTIONS_RUNTIME_URL = https://pipelines.actions.githubusercontent.com/hUh30gkjxhVdc4B3atggKYbYBqA9E7F8EyhkItf3YTZ0OvYff7/
# ACTIONS_RUNTIME_TOKEN = ***
# ACTIONS_CACHE_URL = https://artifactcache.actions.githubusercontent.com/hUh30gkjxhVdc4B3atggKYbYBqA9E7F8EyhkItf3YTZ0OvYff7/
# CONAN_APPLE_CLANG_VERSIONS = 11.0

cmd = Command(Conan())

#cmd.user(["--password", "b69485cb5ca8f4af414a5d7a7f6b0afcad642254", "--remote", "trassir-staging", "trassir-ci-bot"])

#exit(0)

cmd.config(["install", "https://github.com/trassir/conan-config.git"])
cmd.remote(["remove", "bintray-trassir"])
cmd.remote(["add", "trassir-staging", "https://api.bintray.com/conan/trassir/conan-staging", "True"])
cmd.remote(["add", "trassir-public", "https://api.bintray.com/conan/trassir/conan-public", "True"])
cmd.remote(["add", "conan-center", "https://conan.bintray.com", "True"])

if environ.get("GITHUB_HEAD_REF", "master") == "master":
    upload_remote = "trassir-public"
    upload_channel = "stable"
    user_channel = ""
else:
    upload_remote = "trassir-staging"
    upload_channel = environ["GITHUB_HEAD_REF"]
    user_channel = "@trassir/" + upload_channel

for line in open(environ["CONAN_TXT"], "rb").read().splitlines():
    strline = line.decode("ascii")
    if strline.startswith("#") or "# disable GHA" in strline:
        continue
    if "/" not in strline or "@" in strline:
        with open("conanfile.txt", "wb") as f:
            f.write((strline + "\n").encode("utf-8"))
        continue

    package, version = strline.split("/")
    upload_ref = package + "/" + version + user_channel
    with open("conanfile.txt", "wb") as f:
        f.write((upload_ref + "\n").encode("utf-8"))

    conanfile_location = None
    possible_conanfile_locations = [
            path.join("recipes", package, version, "conanfile.py"),
            path.join("recipes", package, "all", "conanfile.py"),
        ]
    for loc in possible_conanfile_locations:
        if path.isfile(loc):
            conanfile_location = loc
    if not conanfile_location:
        raise RuntimeError("Could not find recipe for package ref %s" % strline)

    cmd.export([conanfile_location, upload_ref])

with open("conanfile.txt", "r") as f:
    print("conanfile.txt ready:\n" + f.read())

cmd.install([environ["CONAN_TXT"], "-if", "install_dir", "--update", "-pr", environ["CONAN_PR"], "-s", "build_type=Release", "--build", "missing"])

cmd.user(["--password", environ["CONAN_PASSWORD"], "--remote", upload_remote, "trassir-ci-bot"])

cmd.upload(["--confirm", "--force", "--all", "-r", upload_remote, "*"])


exit(0)

if __name__ == "__main__":
    environ["CONAN_USERNAME"] = "_"
    environ["CONAN_CHANNEL"] = "ci"
    environ["CONAN_TEST_SUITE"] = "True" # trick CPT into uploading from PR

    if "CONAN_OPTIONS" in environ and environ["CONAN_OPTIONS"] != "":
        environ["CONAN_OPTIONS"] = "*:shared=True," + environ["CONAN_OPTIONS"]
    else:
        environ["CONAN_OPTIONS"] = "*:shared=True"

    conan_config_url = None
    if platform != "linux":
        conan_config_url="https://github.com/trassir/conan-config.git"

    # if environ.get("GITHUB_HEAD_REF", "master") == "master":
    #     environ["CONAN_REMOTES"] = "https://api.bintray.com/conan/trassir/conan-public@True@bintray-trassir-public"
    #     environ["CONAN_UPLOAD"] = "https://api.bintray.com/conan/trassir/conan-public@True@bintray-trassir-public"
    # else:
    #     environ["CONAN_REMOTES"] = ",".join([
    #         "https://api.bintray.com/conan/trassir/conan-staging@True@bintray-trassir-staging"
    #         ,"https://api.bintray.com/conan/trassir/conan-public@True@bintray-trassir-public"
    #         ])
    #     environ["CONAN_UPLOAD"] = "https://api.bintray.com/conan/trassir/conan-staging@True@bintray-trassir-staging"

    # api, _, _ = Conan.factory()
    # api.remote_remove("bintray-trassir")

    is_pure_c = get_bool_from_env('IS_PURE_C')
    builder = ConanMultiPackager(
        login_username="trassir-ci-bot",
        upload_only_when_stable=1,
        upload=("https://api.bintray.com/conan/trassir/conan-staging", True, "trassir-staging"),
        stable_branch_pattern="master",
        stable_channel="_",
        # config_url=conan_config_url,
        remotes=[
            ("https://api.bintray.com/conan/trassir/conan-staging", True, "trassir-staging"),
            ("https://api.bintray.com/conan/trassir/conan-public", True, "trassir-public"),
        ]
        )

    builder.add_common_builds(shared_option_name=False, pure_c=is_pure_c)
    builder.run()

# rebuild everything 7
