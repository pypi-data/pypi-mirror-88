#!python

from __future__ import print_function
from pydoc import locate
from pkg_resources import resource_filename, get_distribution
from pathlib import Path
from collections import OrderedDict
import argparse
import getpass
import logging
import os
import time
import schedule
import threading
import yaml
import shutil
import keyring
import requests
import json


class CloudToken(object):
    def __init__(self):
        self.config = None  # Initialise config variable.
        self.logger = None
        self.version = get_distribution("cloudtoken").version

    def is_update_available(self):
        """Check if an update to Cloudtoken is available.

        :return: Bool indicates update is available, bool indicates a forced update, string of the latest version.
        :rtype: (bool, bool, str)
        """

        url = "http://atl-cloudtoken.s3-website-us-east-1.amazonaws.com/versions.json"
        current_version = self.version.split(".")
        timeout = 1.0

        update_available = False
        force_update = False

        try:
            versions = requests.get(url, timeout=timeout).json()["versions"]
        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError, KeyError, TypeError, IndexError):
            print("Attempted to check if updates are available but check failed. Continuing.")
            return (False, False, None)

        try:
            latest_version = versions[-1]["version"]
            for version in versions:
                tmp_version = version["version"].split(".")
                for i in range(3):
                    if int(tmp_version[i]) > int(current_version[i]):
                        update_available = True
                        if version["force_update"]:
                            force_update = True
                        break
        except KeyError:
            print("Unable to parse required fields from {}. Continuing.".format(url))
            return (False, False, None)

        return (update_available, force_update, latest_version)

    @staticmethod
    def filter_classes(cls_obj):
        if cls_obj.__name__ == "CloudTokenPlugin":
            return True

        return False

    def load_plugins(self):
        plugins = OrderedDict([("pre_auth", list()), ("auth", list()), ("post_auth", list())])

        if self.config:
            for plugin_type in ["pre_auth", "auth", "post_auth"]:
                if self.config["plugins"][plugin_type]:
                    for plugin in self.config["plugins"][plugin_type]:
                        self.logger.debug("Loading plugin {0}.".format(plugin))
                        obj = locate("cloudtoken_plugin.{0}.Plugin".format(plugin))
                        if obj is None:
                            print("Unable to load plugin: {0}".format(plugin))
                            print("Exiting.")
                            exit(1)
                        try:
                            plugins[plugin_type].append(obj(self.config))
                        except Exception:
                            raise Exception("Problem loading plugin: {plugin}".format(plugin=plugin))

        return plugins

    def default_parser_args(self, plugins=None, add_help=True):
        """
        Define an ArgumentParser and set default command line options.

        returns parser.parse_args() list.
        """
        all_plugin_objects = list()
        defaults = dict()

        if self.config:
            defaults = self.config.get("defaults", dict())
            if plugins:
                for plugin in self.iterate_plugins(plugins):
                    all_plugin_objects.append(plugin)

        parser = argparse.ArgumentParser(
            prog="cloudtoken",
            description="Command line utility for authenticating with public clouds.",
            conflict_handler="resolve",
            parents=[plugin.arguments(defaults) for plugin in all_plugin_objects],
            add_help=add_help,
            allow_abbrev=False,
        )
        parser.add_argument(
            "-u", "--username", help="Your username", default="{0}".format(defaults.get("username", getpass.getuser()))
        )
        parser.add_argument(
            "--system-username",
            help="Your system username",
            default="{0}".format(defaults.get("system-username", getpass.getuser())),
        )
        parser.add_argument("-p", "--password", help="Your password.", default=defaults.get("password", None))
        parser.add_argument(
            "--password-file",
            help="File containing your password.",
            type=argparse.FileType("r"),
            default=defaults.get("password-file", None),
        )
        parser.add_argument(
            "--password-prompt",
            help="Prompt for your password.",
            dest="password_prompt",
            action="store_true",
            default=defaults.get("password-prompt", None),
        )
        parser.add_argument(
            "-U",
            "--unset",
            action="store_true",
            help="Remove references to current cloud credentials from your system.",
        )
        parser.add_argument(
            "-q", "--quiet", action="store_true", default=defaults.get("quiet", False), help="Suppress most output."
        )
        parser.add_argument(
            "--refresh-interval",
            default=defaults.get("refresh-interval", (60 * 45)),
            type=int,
            help="How often do we refresh the token (in seconds) if --deamon (-d) is specified.",
        )
        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=defaults.get("debug", False),
            help="Print debug information.",
        )
        parser.add_argument(
            "-d",
            "--daemon",
            dest="daemon",
            action="store_true",
            default=defaults.get("daemon", False),
            help="Run a fake AWS metadata proxy.",
        )
        parser.add_argument(
            "-i",
            "--init",
            dest="init",
            action="store_true",
            help="Initialise ~/.config/cloudtoken directory and populate with skeleton files.",
        )
        parser.add_argument(
            "--cloudtoken-dir",
            dest="cloudtoken_dir",
            default="{0}/.config/cloudtoken".format(str(Path.home())),
            type=str,
            help="Cloudtoken directory.",
        )
        parser.add_argument(
            "--config-file",
            dest="config_file",
            default="{0}/.config/cloudtoken/config.yaml".format(str(Path.home())),
            type=str,
            help="Configuration file.",
        )
        parser.add_argument(
            "--skip-keyring",
            dest="skip_keyring",
            action="store_true",
            default=defaults.get("skip-keyring", False),
            help="Skip system keyring for credentials.",
        )
        parser.add_argument(
            "-V", "--version", dest="version", action="store_true", help="Print version information and exit."
        )
        parser.add_argument(
            "--allowed-cidr",
            dest="allowed_cidr",
            type=str,
            default=defaults.get("allowed-cidr", "169.254.169.254/32"),
            help="Specify a comma delimited list of CIDR's to accept requests from in daemon mode. Defaults to 169.254.169.254/32.",
        )  # noqa
        parser.add_argument(
            "--skip-update-check",
            dest="skip_update_check",
            action="store_true",
            default=defaults.get("skip-update-check", False),
            help="Skip checking if an update is available.",
        )

        return parser

    def unset(self, plugin, args):
        self.logger.debug("Running {0}.unset()".format(plugin))
        try:
            plugin.unset(args)
        except TypeError as e:
            print("Exception when executing unset() on plugin {0}: {1}".format(plugin, e))
            exit(1)

    def metadata_proxy(self, args):
        from cloudtoken.proxy import Proxy

        proxy = Proxy(self.config, args)
        proxy.run()

    def create_cloudtoken_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def copy_skeleton_config_files(self, directory):
        """Copy skeleton configuration files from module site-package directory to user cloudtoken config dir.

        :param directory: configuration directory
        :type directory: str
        """

        # [(src_dir, src_filename, overwrite)]
        files = [
            ("configs", "config.yaml", False),
            ("configs", "proxy.yaml", False),
            ("shell_additions", "bashrc_additions", True),
            ("shell_additions", "fishconfig_additions", True),
        ]

        for src_dir, src_filename, overwrite in files:
            source = resource_filename("cloudtoken", "{0}/{1}".format(src_dir, src_filename))
            dest = "{dir}/{file}".format(dir=directory, file=src_filename)
            self.logger.debug("Copying %s to %s", source, dest)

            if os.path.isfile(dest) and overwrite:
                os.remove(dest)

            if not os.path.isfile(dest):
                shutil.copyfile(source, dest)
            else:
                print("{0} already exists. Skipping.".format(dest))
                self.logger.debug("Successfully copied %s to %s", source, dest)

    def run_plugin(self, plugin, args, data, flags):
        self.logger.debug("Running plugin: {0}".format(plugin))
        data = plugin.execute(data, args, flags)
        self.logger.debug("Data Returned From {0}: {1}".format(plugin, data))

        if not isinstance(data, list):
            print("Plugin {0} did not return valid data. Must return list, returned: {1}".format(plugin, type(data)))
            exit(1)

        return data

    def scheduler_plugin_runner(self, plugins, args, data, flags):
        for plugin in plugins:
            data = self.run_plugin(plugin=plugin, args=args, data=data, flags=flags)

    def init(self, directory):
        print("Creating {0} directory.".format(directory))
        self.create_cloudtoken_directory(directory)
        print("Populating {0} with skeleton configuration files.".format(directory))
        self.copy_skeleton_config_files(directory)
        print("Initialisation complete.")
        print("Please see the documentation for instructions on completing shell integration.")
        print("Shell additions and configuration files have been placed in {0}".format(directory))

    def set_logging_levels(self, args):
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)

        self.logger = logging.getLogger("cloudtoken")

    @staticmethod
    def iterate_plugins(plugins):
        """
        Generator to iterate over the loaded plugins.
        :param plugins: dict of plugins as generated by load_plugins().
        :return: plugin
        """
        for category in plugins.keys():
            for plugin in plugins.get(category, []):
                yield plugin

    @staticmethod
    def save_password(username, password):
        try:
            keyring.set_password("cloudtoken", username, password)
            print("Saved password.")
            return True
        except RuntimeError:
            print("No supported keyring backend found - unable to store password.")
            return False

    @staticmethod
    def prompt_password():
        """
        Prompt the user for their password.
        :return: Password string.
        """
        password = ""
        while password == "":
            password = getpass.getpass("Password: ")
        return password

    def password_flow(self, args):
        """
        Handle the password flow, deciding to save to keychain, etc.
        :return: Password string.
        """
        if args.password:
            tmp_password = args.password
            if not args.skip_keyring:
                self.save_password(args.username, tmp_password)
        elif args.password_file:
            tmp_password = args.password_file.read().rstrip()
            if not args.skip_keyring:
                self.save_password(args.username, tmp_password)
        elif args.password_prompt:
            tmp_password = self.prompt_password()
            if not args.skip_keyring:
                self.save_password(args.username, tmp_password)
        elif args.skip_keyring:
            tmp_password = self.prompt_password()
        else:
            tmp_password = keyring.get_password("cloudtoken", args.username)
            if not tmp_password:
                tmp_password = self.prompt_password()
                self.save_password(args.username, tmp_password)

        return tmp_password

    def main(self):
        # Load argparse initially so we can capture --config and load an alternate config file if required.
        # use parse_known_args() so it ignores unknown arguments.
        parser = self.default_parser_args(add_help=False)
        args = parser.parse_known_args()[0]

        self.set_logging_levels(args)

        if args.version:
            print(self.version)
            exit(0)

        if args.init:
            self.init(args.cloudtoken_dir)
            exit(0)

        try:
            with open(args.config_file) as fh:
                self.config = yaml.safe_load(fh.read())
        except IOError:
            print("Unable to load config file: {0}".format(args.config_file))
            parser.print_help()
            exit(1)

        self.config["config_dir"] = args.cloudtoken_dir

        plugins = self.load_plugins()
        if not plugins["auth"]:
            print("No auth plugins configured. Exiting.")
            exit(1)

        # Load argparse for realz.
        parser = self.default_parser_args(plugins)
        args = parser.parse_args()

        if not args.skip_update_check:
            update_available, force_update, latest_version = self.is_update_available()
            if update_available:
                if force_update:
                    print(
                        "A mandatory update is now available ({0}). Cloudtoken will not run until updated.".format(
                            latest_version
                        )
                    )
                    exit(1)
                print(
                    "An updated version of Cloudtoken is available ({0}). You are currently running {1}.".format(
                        latest_version, self.version
                    )
                )

        args.password = self.password_flow(args)

        # Redefining args.allowed_cidr to be a list of CIDR's and ensuring 169.254.169.254 is in there.
        # filter() removes empty items.
        args.allowed_cidr = list(filter(None, [cidr.strip() for cidr in args.allowed_cidr.split(",")]))
        if "169.254.169.254/32" not in args.allowed_cidr:
            args.allowed_cidr.insert(0, "169.254.169.254/32")

        if args.unset:
            for plugin in self.iterate_plugins(plugins):
                self.unset(plugin, args)
            exit(0)

        # Run the plugins.
        data = list()
        for plugin in self.iterate_plugins(plugins):
            data = self.run_plugin(plugin=plugin, args=args, data=data, flags={})

        # Metadata proxy.
        try:
            if args.daemon:
                t = threading.Thread(target=self.metadata_proxy, kwargs={"args": args})
                t.daemon = True
                t.start()

                scheduled_plugins = plugins["auth"] + plugins["post_auth"]
                schedule.every(args.refresh_interval).seconds.do(
                    self.scheduler_plugin_runner,
                    plugins=scheduled_plugins,
                    args=args,
                    data=data,
                    flags={"daemon_mode": True},
                )

                print("Accepting requests from: " + ", ".join(args.allowed_cidr))
                print("Metadata proxy now available on http://169.254.169.254")
                print("--")

                while True:
                    schedule.run_pending()
                    time.sleep(1)
        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    try:
        cloudtoken = CloudToken()
        cloudtoken.main()
    except KeyboardInterrupt:
        pass
    except Exception:
        raise
