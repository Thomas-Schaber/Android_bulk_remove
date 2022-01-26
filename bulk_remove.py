import subprocess

#com.expressvpn.vpn

def main():
    devices = read_devices()
    package_list = []
    uninstall_list = []
    count = 0
    print("Please select option: \n")
    for device in devices:
        print("[",count,"]", device)
        count += 1
    print("[", count, "] For all")
    try:
        choice = int(input(""))
        #choice = 0
        if choice == count:

            for device in devices:
                create_package_list(device)
                uninstall_list = create_uninstall_list()
                uninstall(device, uninstall_list)


                #uninstall(device, final_list)

        elif count > choice >= 0:

            device = devices[choice]
            create_package_list(device)
            uninstall_list = create_uninstall_list()
            uninstall(device, uninstall_list)
        else:
            print("Invalid input")
    except Exception as e:
        print(e.with_traceback())
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


#creates a list of apps to unsistall from devices
def create_uninstall_list():
    count = 0
    package_on_device = open("packages.txt", "r")
    sys_files = open('sys_files.txt', 'r')
    #master_package_file = open("master-package-list.txt", "r")
    #master_list = []
    package_on_device_list = []
    sys_files_list = []
    uninstall_list = []
    for package in sys_files.readlines():
        #print(package)
        if package.__contains__("\n"):
            sys_files_list.append(package.split("\n")[0])
        else:
            sys_files_list.append(package)
    sys_files.close()
    #print(len(master_list))
    for x in package_on_device.readlines():
        if(x != "\n"):
            package_on_device_list.append(x.split("package:")[1].split("\n")[0])

    package_on_device.close()
    # master_package_file.close()
    print('Creating uninstall list')
    in_list = False
    for y in package_on_device_list:
        for x in sys_files_list:
            if y == x or y == 'com.expressvpn.vpn' or y == 'com.apkpremier.app':
                in_list = True
        if in_list:
            in_list = False
            continue
        else:
            uninstall_list.append(y)

        # print('y ', y)
        # for package in sys_files_list:
        #     #print("package = ", package, " x = ", x)
        #     if y == package:
        #         # print('DEBUG package = ', package)
        #         # print('DEBUG x = ', x)
        #         continue
        #     elif y == 'com.expressvpn.vpn' or y in uninstall_list:
        #
        #         continue
        #     else:
        #         print('else ', package)
        #         uninstall_list.append(y)
    print(package_on_device_list)
    print(sys_files_list)
    print(uninstall_list)

    return uninstall_list




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
    print('Uninstalling apks')
    for package in package_list:
        sys_files = open('sys_files.txt', 'r')

        if package not in sys_files.read():
            print(package)
            print("Uninstalling " + package)
            shellcommand = "adb -s " + device + " uninstall " + package
            p2 = subprocess.Popen(shellcommand, stdout=subprocess.PIPE,
                                  stderr=None, shell=True)
            for line in p2.stdout.readlines():
                line = line.decode("utf-8", "ignore")
                print(line)

                if 'Failure [DELETE_FAILED_INTERNAL_ERROR]' in line or 'Failure [DELETE_FAILED_INTERNAL_ERROR]' in \
                        line or 'Failure [DELETE_FAILED_DEVICE_POLICY_MANAGER]' in line\
                        or 'Failure [DELETE_FAILED_OWNER_BLOCKED]' in line:
                    # sys_files = open('sys_files.txt', 'a')
                    # sys_files.write(package + '\n')
                    print("Error #############################################", package)
        sys_files.close()
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

