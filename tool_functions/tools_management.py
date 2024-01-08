import style.colors as colors
import shutil
import subprocess


# Check if all the required tool are installed...
def check_installed(tool):
    return shutil.which(tool) is not None


# Installs missing tools
def install_missing_tools(not_installed_tools):
    for tool in not_installed_tools:
        print(["sudo", "apt", "install", tool])
        # subprocess.run(["sudo", "apt", "install", tool])


# This function handle the core functionality of managing all other functions...
def manage_tools():
    install_tools = None

    tools_list = ["airmon-ng", "airodump-ng"]  # Required tools list
    not_installed_tools = []  # Not installed required tools list

    python_library_list = ["tabulate", "psutil"]  # Required python library list
    not_installed_libraries = []  # Not installed required python library list

    #
    for tool in tools_list:
        if check_installed(tool):
            print(f"{colors.MAGENTA}{tool}: {colors.GREEN}Installed...{colors.RESET}")
        else:
            not_installed_tools.append(tool)
            print(f"{colors.MAGENTA}{tool}: {colors.RED}No installed...{colors.RESET}")

    #
    while install_tools is None and (len(not_installed_tools) > 0 or len(not_installed_libraries) > 0):
        install_tools = input("\n Install required applications: (Y/N) / (y/n)\n")

        if install_tools == "y" or install_tools == "Y":
            print(f"{colors.GREEN} Installing required applications... {colors.RESET}")

            try:
                install_missing_tools(not_installed_tools)
                print(f"{colors.GREEN}Successfully installed all missing tools...{colors.RESET}")

            except subprocess.CalledProcessError:
                print(f"{colors.RED}Failed to install applications...{colors.RESET}")

        else:
            print(f"{colors.YELLOW}Starting application with limited functionality... \n{colors.RESET}")
