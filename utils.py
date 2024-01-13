from colorama import Fore, Style


def print_success(str):
    print(Fore.GREEN + str + Style.RESET_ALL)


def print_info(str, end="\n", flush=False):
    print(Fore.BLUE + str + Style.RESET_ALL, end=end, flush=flush)


def print_warning(str):
    print(Fore.YELLOW + str + Style.RESET_ALL)


def print_error(str, end="\n", flush=False):
    print(Fore.RED + str + Style.RESET_ALL, end=end, flush=flush)
