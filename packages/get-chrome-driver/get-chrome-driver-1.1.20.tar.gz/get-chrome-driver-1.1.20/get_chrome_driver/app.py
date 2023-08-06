import sys
import argparse
from signal import signal, SIGINT

import colorama

from . import __version__
from . import arguments
from .get_driver import GetChromeDriver
from .platforms import Platforms
from .phase import Phase
from .exceptions import GetChromeDriverError


def main():
    # noinspection PyUnusedLocal
    def signal_handler(signal_received, frame):
        """ Handles clean Ctrl+C exit """

        sys.stdout.write('\n')
        sys.exit(0)

    signal(SIGINT, signal_handler)
    App()


class App:

    def __init__(self):
        self.__c_fore = colorama.Fore
        self.__c_style = colorama.Style
        colorama.init()

        self.__platforms = Platforms()
        self.__phases = Phase()

        self.__msg_download_finished = 'download finished'
        self.__msg_required_choose_platform = (self.__c_fore.RED + 'required: choose one of the following platforms: '
                                               + str(self.__platforms.list) + self.__c_style.RESET_ALL)
        self.__msg_required_add_release = (self.__c_fore.RED + 'required: add a release version'
                                           + self.__c_style.RESET_ALL)
        self.__msg_optional_add_extract = 'optional: add --extract to extract the zip file'
        self.__msg_error_unrecognized_argument = (
                self.__c_fore.RED + 'error: unrecognized argument(s) detected' + self.__c_style.RESET_ALL
                + '\n' + 'tip: use --help to see all available arguments')
        self.__msg_download_error = (self.__c_fore.RED + 'error: an error occurred at downloading'
                                     + self.__c_style.RESET_ALL)
        self.__msg_no_release_version_error = (self.__c_fore.RED + 'error: could not find release version'
                                               + self.__c_style.RESET_ALL)
        self.__msg_release_url_error = (self.__c_fore.RED + 'error: could not find release url'
                                        + self.__c_style.RESET_ALL)
        self.__msg_not_found_error = (self.__c_fore.RED + 'not found'
                                      + self.__c_style.RESET_ALL)
        self.__msg_no_beta_release_version_error = (self.__c_fore.RED
                                                    + 'error: could not find a beta release version'
                                                    + self.__c_style.RESET_ALL)
        self.__msg_no_stable_release_version_error = (self.__c_fore.RED
                                                      + 'error: could not find a stable release version'
                                                      + self.__c_style.RESET_ALL)

        self.__parser = argparse.ArgumentParser(add_help=False)
        for i, arg in enumerate(arguments.args_options):
            self.__parser.add_argument(arguments.args_options[i][0], nargs='*')
        self.__args, self.__unknown = self.__parser.parse_known_args()

        if self.__unknown:
            print(self.__msg_error_unrecognized_argument)
            sys.exit(0)

        ###################
        # DEFAULT NO ARGS #
        ###################
        if len(sys.argv) == 1:
            arguments.print_help()
            sys.exit(0)

        ########
        # HELP #
        ########
        self.__arg_help = self.__args.help
        if self.__arg_passed(self.__arg_help):
            arguments.print_help()
            sys.exit(0)

        ################
        # BETA VERSION #
        ################
        self.__arg_beta_version = self.__args.beta_version
        if self.__arg_passed(self.__arg_beta_version):
            self.print_phase_version(self.__phases.beta)
            sys.exit(0)

        ##################
        # STABLE VERSION #
        ##################
        self.__arg_stable_version = self.__args.stable_version
        if self.__arg_passed(self.__arg_stable_version):
            self.print_phase_version(self.__phases.stable)
            sys.exit(0)

        ########
        # URLS #
        ########
        self.__arg_latest_urls = self.__args.latest_urls
        if self.__arg_passed(self.__arg_latest_urls):
            self.print_urls()
            sys.exit(0)

        ###############
        # RELEASE URL #
        ###############
        self.__arg_release_url = self.__args.release_url
        if self.__arg_passed(self.__arg_release_url):
            custom_required_message = (self.__msg_required_choose_platform + '\n' + self.__msg_required_add_release)
            if not self.__arg_release_url:
                print(custom_required_message)
                sys.exit(0)
            if len(self.__arg_release_url) != 2:
                print(custom_required_message)
                sys.exit(0)

            platform = self.__arg_release_url[0]
            release = self.__arg_release_url[1]
            if self.__platforms.win == platform:
                self.print_release_url(self.__platforms.win, release)
            elif self.__platforms.linux == platform:
                self.print_release_url(self.__platforms.linux, release)
            elif self.__platforms.mac == platform:
                self.print_release_url(self.__platforms.mac, release)
            else:
                print(custom_required_message)
            sys.exit(0)

        ############
        # BETA URL #
        ############
        self.__arg_beta_url = self.__args.beta_url
        if self.__arg_passed(self.__arg_beta_url):
            if not self.__arg_beta_url:
                print(self.__msg_required_choose_platform)
                sys.exit(0)
            if len(self.__arg_beta_url) != 1:
                print(self.__msg_required_choose_platform)
                sys.exit(0)

            platform = self.__arg_beta_url[0]
            if self.__platforms.win == platform:
                self.print_phase_url(self.__platforms.win, self.__phases.beta)
            elif self.__platforms.linux == platform:
                self.print_phase_url(self.__platforms.linux, self.__phases.beta)
            elif self.__platforms.mac == platform:
                self.print_phase_url(self.__platforms.mac, self.__phases.beta)
            else:
                print(self.__msg_required_choose_platform)
            sys.exit(0)

        ##############
        # STABLE URL #
        ##############
        self.__arg_stable_url = self.__args.stable_url
        if self.__arg_passed(self.__arg_stable_url):
            if not self.__arg_stable_url:
                print(self.__msg_required_choose_platform)
                sys.exit(0)
            if len(self.__arg_stable_url) != 1:
                print(self.__msg_required_choose_platform)
                sys.exit(0)

            self.__platform = self.__arg_stable_url[0]
            if self.__platforms.win == self.__platform:
                self.print_phase_url(self.__platforms.win, self.__phases.stable)
            elif self.__platforms.linux == self.__platform:
                self.print_phase_url(self.__platforms.linux, self.__phases.stable)
            elif self.__platforms.mac == self.__platform:
                self.print_phase_url(self.__platforms.mac, self.__phases.stable)
            else:
                print(self.__msg_required_choose_platform)
            sys.exit(0)

        #################
        # DOWNLOAD BETA #
        #################
        self.__arg_download_beta = self.__args.download_beta
        if self.__arg_passed(self.__arg_download_beta):
            if not self.__arg_download_beta:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
                sys.exit(0)

            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True

            platform = self.__arg_download_beta[0]
            if platform in self.__platforms.list:
                self.download_phase_release(platform, self.__phases.beta, extract)
            else:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
            sys.exit(0)

        ###################
        # DOWNLOAD STABLE #
        ###################
        self.__arg_download_stable = self.__args.download_stable
        if self.__arg_passed(self.__arg_download_stable):
            if not self.__arg_download_stable:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
                sys.exit(0)

            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True

            platform = self.__arg_download_stable[0]
            if platform in self.__platforms.list:
                self.download_phase_release(platform, self.__phases.stable, extract)
            else:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
            sys.exit(0)

        ####################
        # DOWNLOAD RELEASE #
        ####################
        self.__arg_download_release = self.__args.download_release
        if self.__arg_passed(self.__arg_download_release):
            custom_required_message = (self.__msg_required_choose_platform
                                       + '\n' + self.__msg_required_add_release)
            if not self.__arg_download_release:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            if len(self.__arg_download_release) != 2:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)

            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            if len(self.__arg_download_release) != 2:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            else:
                platform = self.__arg_download_release[0]
                if platform in self.__platforms.list:
                    release = self.__arg_download_release[1]
                    self.download_release(platform, release, extract)
                else:
                    print(custom_required_message)
                    print(self.__msg_optional_add_extract)
            sys.exit(0)

        ###########
        # VERSION #
        ###########
        self.__arg_version = self.__args.version
        if self.__arg_passed(self.__arg_version):
            print('v' + __version__)
            sys.exit(0)

    def __arg_passed(self, arg):
        """ Check if arguments were passed """

        if isinstance(arg, list):
            return True
        return False

    def print_urls(self):
        """ Print the stable url release for all platforms """

        latest_stable_release_for_str = 'Latest stable release for '

        get_driver = GetChromeDriver(self.__platforms.win)
        print(latest_stable_release_for_str + 'Windows:')
        try:
            print(get_driver.stable_release_url())
        except GetChromeDriverError:
            print(self.__msg_not_found_error)
        print('')

        get_driver = GetChromeDriver(self.__platforms.linux)
        print(latest_stable_release_for_str + 'Linux:')
        try:
            print(get_driver.stable_release_url())
        except GetChromeDriverError:
            print(self.__msg_not_found_error)
        print('')

        get_driver = GetChromeDriver(self.__platforms.mac)
        print(latest_stable_release_for_str + 'Mac:')
        try:
            print(get_driver.stable_release_url())
        except GetChromeDriverError:
            print(self.__msg_not_found_error)

    def print_phase_version(self, phase):
        """ Print stable version or beta version """

        if phase == self.__phases.beta:
            get_driver = GetChromeDriver(self.__platforms.win)
            try:
                print(get_driver.beta_release_version())
            except GetChromeDriverError:
                print(self.__msg_no_beta_release_version_error)
        elif phase == self.__phases.stable:
            get_driver = GetChromeDriver(self.__platforms.win)
            try:
                print(get_driver.stable_release_version())
            except GetChromeDriverError:
                print(self.__msg_no_stable_release_version_error)
        else:
            print(self.__msg_no_release_version_error)

    def print_phase_url(self, platform, phase):
        """ Print stable url or beta url """

        get_driver = GetChromeDriver(platform)
        if phase == self.__phases.beta:
            try:
                print(get_driver.beta_release_url())
            except GetChromeDriverError:
                print(self.__msg_release_url_error)
        elif phase == self.__phases.stable:
            try:
                print(get_driver.stable_release_url())
            except GetChromeDriverError:
                print(self.__msg_release_url_error)

    def print_release_url(self, platform, release):
        """ Print the url for a given version """

        get_driver = GetChromeDriver(platform)
        try:
            print(get_driver.release_url(release))
        except GetChromeDriverError:
            print(self.__msg_release_url_error)

    def download_phase_release(self, platform, phase, extract):
        """ Download the release for the stable version or beta version """

        get_driver = GetChromeDriver(platform)
        if phase == self.__phases.beta:
            try:
                get_driver.download_beta_release(extract=extract)
                print(self.__msg_download_finished)
            except GetChromeDriverError:
                print(self.__msg_download_error)
                print(self.__msg_no_beta_release_version_error)
        elif phase == self.__phases.stable:
            try:
                get_driver.download_stable_release(extract=extract)
                print(self.__msg_download_finished)
            except GetChromeDriverError:
                print(self.__msg_download_error)

    def download_release(self, platform, release, extract):
        """ Download the release of a given version """

        get_driver = GetChromeDriver(platform)
        try:
            get_driver.download_release(release, extract=extract)
            print(self.__msg_download_finished)
        except GetChromeDriverError:
            print(self.__msg_download_error)
