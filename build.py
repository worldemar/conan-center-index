from os import environ
from sys import exit
# from cpt.packager import ConanMultiPackager
# from cpt.tools import get_bool_from_env
from conans.client.conan_api import Conan
from conans.client.command import Command

cmd = Command(Conan())
cmd.config(["install", "https://github.com/trassir/conan-config.git"])
cmd.remote(["remove", "bintray-trassir"])
cmd.remote(["add", "trassir-staging", "https://api.bintray.com/conan/trassir/conan-staging", "True"])
cmd.remote(["add", "trassir-public", "https://api.bintray.com/conan/trassir/conan-public", "True"])
cmd.remote(["add", "conan-center", "https://conan.bintray.com", "True"])

cmd.install([environ["CONAN_TXT"], "-if", "install_dir", "--update", "-pr", environ["CONAN_PR"], "-s", "build_type=Release", "--build", "missing"])

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
