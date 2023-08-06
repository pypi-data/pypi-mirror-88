"""
Wordpress Watcher
Automating WPscan to scan and report vulnerable Wordpress sites

DISCLAIMER - USE AT YOUR OWN RISK.
"""

# Main program, parse the args, read config and launch scans
import argparse
import shlex
import sys
from wpwatcher import log, init_log
from wpwatcher.__version__ import __version__, __author__, __url__
from wpwatcher.utils import parse_timedelta
from wpwatcher.config import WPWatcherConfig
from wpwatcher.core import WPWatcher
from wpwatcher.db import WPWatcherDataBase
from wpwatcher.daemon import WPWatcherDaemon
from wpwatcher.syslogout import WPSyslogOutput
from wpscan_out_parse import format_results


class WPWatcherCLI:
    """Main program class"""

    def __init__(self):
        """Main program entrypoint"""

        # Parse arguments
        args = self.parse_args()

        # Init logger with CLi arguments
        init_log(args.verbose, args.quiet)

        # If template conf , print and exit
        if args.template_conf:
            self.template_conf()

        # Print "banner"
        log.info(
            "WPWatcher -  Automating WPscan to scan and report vulnerable Wordpress sites"
        )

        if args.version:
            # Print and exit
            self.verion()

        if args.wprs != False:
            # Init WPWatcherDataBase object and dump reports
            self.wprs(filepath=args.wprs, daemon=args.daemon)

        # Read config
        configuration = self.build_config_cli(args)

        if args.show:
            # Init WPWatcherDataBase object and dump cli formatted report
            self.show(
                urlpart=args.show,
                filepath=configuration["wp_reports"],
                daemon=args.daemon,
            )

        # Launch syslog test
        if args.syslog_test:
            self.syslog_test(configuration)

        # If daemon lopping
        if configuration["daemon"]:
            # Run 4 ever
            WPWatcherDaemon(configuration)
        else:
            # Run scans and quit
            # Create main object
            wpwatcher = WPWatcher(configuration)
            exit_code, _ = wpwatcher.run_scans_and_notify()
            exit(exit_code)

    @staticmethod
    def wprs(filepath=None, daemon=False):
        """Generate JSON file database summary"""
        db = WPWatcherDataBase(filepath, daemon=daemon)
        sys.stdout.buffer.write(WPWatcher.results_summary(db._data).encode("utf8"))
        sys.stdout.flush()
        exit(0)

    @staticmethod
    def show(urlpart, filepath=None, daemon=False):
        """Inspect a report in database"""
        db = WPWatcherDataBase(filepath, daemon=daemon)
        matching_reports = [r for r in db._data if urlpart in r["site"]]
        eq_reports = [r for r in db._data if urlpart == r["site"]]
        if len(eq_reports):
            sys.stdout.buffer.write(
                format_results(eq_reports[0], format="cli").encode("utf8")
            )
        elif len(matching_reports) == 1:
            sys.stdout.buffer.write(
                format_results(matching_reports[0], format="cli").encode("utf8")
            )
        elif len(matching_reports) > 1:
            sys.stdout.buffer.write(
                "The following sites match your search: \n".encode("utf8")
            )
            sys.stdout.buffer.write(
                WPWatcher.results_summary(matching_reports).encode("utf8")
            )
            sys.stdout.buffer.write("\nPlease be more specific. \n".encode("utf8"))
        else:
            sys.stdout.buffer.write("No report found".encode("utf8"))
            exit(1)
        exit(0)

    @staticmethod
    def verion():
        """Print version and contributors"""
        log.info("Version:\t\t%s" % __version__)
        log.info("Authors:\t\t%s" "" % __author__)
        exit(0)

    @staticmethod
    def template_conf():
        """Print template configuration"""
        sys.stdout.buffer.write(WPWatcherConfig.TEMPLATE_FILE.encode("utf8"))
        sys.stdout.flush()
        exit(0)

    @staticmethod
    def syslog_test(conf):
        """Launch the emit_test_messages() method"""
        syslog = WPSyslogOutput(conf)
        syslog.emit_test_messages()
        exit(0)

    @staticmethod
    def get_arg_parser():
        """Parse CLI arguments, arguments can overwrite config file values"""

        parser = argparse.ArgumentParser(
            description="""WordPress Watcher is a Python wrapper for WPScan that manages scans on multiple sites and reports by email.
    Some config arguments can be passed to the command.
    It will overwrite previous values from config file(s).
    Check %s for more informations."""
            % (__url__)
        )
        parser.add_argument(
            "--conf",
            "-c",
            metavar="File path",
            help="""Configuration file. You can specify multiple files, it will overwrites the keys with each successive file.
    If not specified, will try to load config from file `~/.wpwatcher/wpwatcher.conf`, `~/wpwatcher.conf` and `./wpwatcher.conf`.
    All options can be missing from config file.""",
            nargs="+",
            default=None,
        )
        parser.add_argument(
            "--template_conf",
            "--tmpconf",
            help="""Print a template config file.""",
            action="store_true",
        )

        # Declare arguments
        parser.add_argument(
            "--wp_sites",
            "--url",
            metavar="URL",
            help="Site(s) to scan, you can pass multiple values",
            nargs="+",
            default=None,
        )
        parser.add_argument(
            "--wp_sites_list",
            "--urls",
            metavar="Path",
            help="Read URLs from a text file. File must contain one URL per line",
            default=None,
        )
        parser.add_argument(
            "--send_email_report",
            "--send",
            help="Enable email report sending",
            action="store_true",
        )
        parser.add_argument(
            "--email_to",
            "--em",
            metavar="Email",
            help="Email the specified receipent(s) you can pass multiple values",
            nargs="+",
            default=None,
        )
        parser.add_argument(
            "--send_infos", "--infos", help="Email INFO reports", action="store_true"
        )
        parser.add_argument(
            "--send_errors", "--errors", help="Email ERROR reports", action="store_true"
        )
        parser.add_argument(
            "--attach_wpscan_output",
            "--attach",
            help="Attach WPScan output to emails",
            action="store_true",
        )
        parser.add_argument(
            "--use_monospace_font",
            "--monospace",
            help="Use Courrier New monospaced font in emails",
            action="store_true",
        )
        parser.add_argument(
            "--fail_fast",
            "--ff",
            help="Interrupt scans if any WPScan or sendmail failure",
            action="store_true",
        )
        parser.add_argument(
            "--api_limit_wait",
            "--wait",
            help="Sleep 24h if API limit reached",
            action="store_true",
        )
        parser.add_argument(
            "--daemon", help="Loop and scan for ever", action="store_true"
        )
        parser.add_argument(
            "--daemon_loop_sleep",
            "--loop",
            metavar="Time string",
            help="Time interval to sleep in daemon loop",
            default=None,
        )
        parser.add_argument(
            "--wp_reports",
            "--reports",
            metavar="Path",
            help="Database Json file",
            default=None,
        )
        parser.add_argument(
            "--resend_emails_after",
            "--resend",
            metavar="Time string",
            help="Minimum time interval to resend email report with same status",
            default=None,
        )
        parser.add_argument(
            "--asynch_workers",
            "--workers",
            metavar="Number",
            help="Number of asynchronous workers",
            type=int,
            default=None,
        )
        parser.add_argument(
            "--log_file",
            "--log",
            metavar="Path",
            help="Logfile replicates all output with timestamps",
            default=None,
        )
        parser.add_argument(
            "--follow_redirect",
            "--follow",
            help="Follow site redirection if causes WPscan failure",
            action="store_true",
        )
        parser.add_argument(
            "--wpscan_output_folder",
            "--wpout",
            metavar="Path",
            help="Write all WPScan results in sub directories 'info', 'warning', 'alert' and 'error'",
            default=None,
        )
        parser.add_argument(
            "--wpscan_args",
            "--wpargs",
            metavar="Arguments",
            help="WPScan arguments as string. See 'wpscan --help' for more infos",
            default=None,
        )
        parser.add_argument(
            "--false_positive_strings",
            "--fpstr",
            metavar="String",
            help="False positive strings, you can pass multiple values",
            nargs="+",
            default=None,
        )
        parser.add_argument(
            "--verbose",
            "-v",
            help="Verbose output, print WPScan raw output and parsed WPScan results.",
            action="store_true",
        )
        parser.add_argument(
            "--quiet",
            "-q",
            help="Print only errors and WPScan ALERTS",
            action="store_true",
        )
        parser.add_argument(
            "--version", "-V", help="Print WPWatcher version", action="store_true"
        )
        parser.add_argument(
            "--syslog_test",
            help="Sends syslog testing packets of all possible sorts to the configured syslog server.",
            action="store_true",
        )
        parser.add_argument(
            "--wprs",
            metavar="Path",
            help="Print all reports summary. Leave path blank to find default file. Can be used with --daemon to print default daemon databse.",
            nargs="?",
            default=False,
        )
        parser.add_argument(
            "--show", metavar="Site", help="Inspect a report in the Database"
        )
        return parser
    
    @staticmethod
    def parse_args():
        parser = WPWatcherCLI.get_arg_parser()
        args = parser.parse_args()
        return args

    @staticmethod
    def build_config_cli(args):
        """Assemble the config dict from args and from file.  

        Arguments:

        - 'args': Namespace from `ArgumentParser.parse_args()`
        """

        args = vars(
            args
        )  # if hasattr(args, '__dict__') and not type(args)==dict else args
        # Configuration variables
        conf_files = args["conf"] if "conf" in args else None

        # Init config dict: read config files
        configuration, files = WPWatcherConfig(files=conf_files).build_config()
        if files:
            log.info("Load config file(s) : %s" % files)

        # Sorting out only args that matches config options and that are not None or False
        conf_args = {}
        for k in args:
            if k in WPWatcherConfig.DEFAULT_CONFIG.keys() and args[k]:
                conf_args.update({k: args[k]})

        # Append or init list of urls from file if any
        if args.get("wp_sites_list", None):
            with open(args["wp_sites_list"], "r") as urlsfile:
                sites = [site.replace("\n", "") for site in urlsfile.readlines()]
                conf_args["wp_sites"] = (
                    sites
                    if "wp_sites" not in conf_args
                    else conf_args["wp_sites"] + sites
                )

        conf_args = WPWatcherCLI.adjust_special_cli_args(conf_args)

        # Overwrite with conf dict built from CLI Args
        if conf_args:
            for k in conf_args:
                if k == "wpscan_args":
                    # MAke sure to append new WPScan arguments after defaults
                    configuration[k].extend(conf_args[k])
                else:
                    configuration[k] = conf_args[k]

        return configuration

    @staticmethod
    def adjust_special_cli_args(conf_args):
        """
        Adjust special CLI arguments types.

        Arguments:

        - 'conf_args': Configuration dict with CLI parsed values only
        """

        # Adjust special case of urls that are list of dict
        if "wp_sites" in conf_args:
            conf_args["wp_sites"] = [{"url": site} for site in conf_args["wp_sites"]]
        
        # Adjust special case of resend_emails_after
        if "resend_emails_after" in conf_args:
            conf_args["resend_emails_after"] = parse_timedelta(
                conf_args["resend_emails_after"]
            )
        # Adjust special case of daemon_loop_sleep
        if "daemon_loop_sleep" in conf_args:
            conf_args["daemon_loop_sleep"] = parse_timedelta(
                conf_args["daemon_loop_sleep"]
            )
        # Adjust special case of wpscan_args
        if "wpscan_args" in conf_args:
            conf_args["wpscan_args"] = shlex.split(conf_args["wpscan_args"])
        return conf_args


def main():
    """Main program"""
    WPWatcherCLI()


"""Main program if called with wpwatcher/cli.py"""
if __name__ == "__main__":
    WPWatcherCLI()
