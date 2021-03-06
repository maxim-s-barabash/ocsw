try:
    from colorama import Back, Fore, Style, init

    init()
except ImportError:  # fallback so that the imported classes always exist

    class ColorFallback:
        def __getattr__(self, name):
            return ""

    Fore = Back = Style = ColorFallback()


def color_diff(diff):
    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith("?"):
            yield Fore.BLUE + line + Fore.RESET
        elif line.startswith("@@ "):
            yield Style.BRIGHT + line + Style.RESET_ALL
        else:
            yield line
