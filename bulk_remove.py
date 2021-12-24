import subprocess


def main():
    devices = read_devices()
    package_list = []
    count = 0
    print("Please select option: \n")
    for device in devices:
        print("[",count,"]", device)
        count += 1
    print("[", count, "] For all")
    try:
        choice = int(input(""))
        if choice == count:

            for device in devices:
                create_package_list(device)
                file = open("packages.txt", "r")
                for line in file:
                    package_list.append(line)
                file.close()
                package_list = format_packages(package_list)
                final_list = []
                master_list = open("master-package-list.txt", "r")
                for line in master_list:
                    for x in package_list:
                        if line.__contains__(x) and line != "" and line != " ":
                            if x == "android" or x == "com.expressvpn.vpn":
                                continue
                            else:
                                final_list.append(x)

                print("Removing ", len(final_list), "apps")
                final_list = format_packages(final_list)
                uninstall(device, final_list)

        elif count > choice >= 0:

            device = devices[choice]
            create_package_list(device)
            file = open("packages.txt", "r")
            for line in file:
                package_list.append(line)
            package_list = format_packages(package_list)
            final_list = []
            master_list = open("master-package-list.txt", "r")
            for line in master_list:
                for x in package_list:
                    if line.__contains__(x):
                        if x == "android" or x == "com.expressvpn.vpn":
                            continue
                        else:
                            final_list.append(x)

            print("Removing ", len(final_list), "apps")
            final_list = format_packages(final_list)
            uninstall(device, final_list)
        else:
            print("Invalid input")
    except ValueError:
        print("Invalid input")


# Uses adb shell command to generate a list of packages by device for use later in code
def create_package_list(device):
    shellcommand = "adb -s " + device + " shell pm list packages > packages.txt"
    print(shellcommand)
    p2 = subprocess.Popen(shellcommand, stdout=subprocess.PIPE,
                          stderr=None, shell=True)
    for line in p2.stdout.readlines():
        line = line.decode("utf-8", "ignore")
        print(line)


# Formats the package file to better use adb uninstall command by splitting the package: and \n at end of file
def format_packages(package_list):
    formatted_list = []
    for package in package_list:
        package = package.split("package:")
        #print(package)
        #print(len(package))
        if len(package) > 1:
            package = package[1].split("\n")
        formatted_list.append(package[0])

    return formatted_list


# Uses adb shell command to uninstall packages in the packages.txt and prints a messages at the end
def uninstall(device, package_list):
    for package in package_list:
        print("Uninstalling " + package)
        shellcommand = "adb -s " + device + " uninstall " + package
        p2 = subprocess.Popen(shellcommand, stdout=subprocess.PIPE,
                              stderr=None, shell=True)
        for line in p2.stdout.readlines():
            line = line.decode("utf-8", "ignore")
            print(line)
    print("\n####################\n####### Done #######\n####################\n")


# Uses an adb command to get a list of devices currently connected
def read_devices():
    devices = []
    shellcommand = "adb devices"
    devicesCommand = subprocess.Popen(shellcommand, shell=True, stderr=None, stdout=subprocess.PIPE)
    for line in devicesCommand.stdout.readlines():
        line = line.decode("utf-8")
        if line.__contains__("device") and not line.__contains__("devices"):
            line = line.split("\t")
            if line not in devices:
                #devices.append(line[0])
                devices.insert(0, line[0])

    return devices


if __name__ == '__main__':
    main()

