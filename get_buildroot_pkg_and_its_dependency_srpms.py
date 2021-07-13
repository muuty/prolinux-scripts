import os
import subprocess

WORKING_DIRECTORY = os.path.abspath(os.getcwd())
INSTALL_ROOT_DIR = WORKING_DIRECTORY + "/install_root"
BUILD_ROOT_PACKAGES= "bash bzip2 coreutils cpio diffutils findutils gawk gcc gcc-c++ gnupg2 grep gzip info make patch prolinux-release redhat-rpm-config rpm-build scl-utils-build sed shadow-utils tar unzip util-linux which"
BUILD_ROOT_PACKAGES = BUILD_ROOT_PACKAGES.replace('prolinux-release','')
APPSTREAM_REPO_URL = "http://192.168.2.136/rhel/8.3/os/AppStream/Packages/"
BASEOS_REPO_URL = "http://192.168.2.136/rhel/8.3/os/BaseOS/Packages/"

print(WORKING_DIRECTORY)
print(INSTALL_ROOT_DIR)



def install_buildroot_packages():
    subprocess.run(['mkdir', '-p', INSTALL_ROOT_DIR])
    result = subprocess.Popen(['yum -y install --installroot ' + INSTALL_ROOT_DIR + BUILD_ROOT_PACKAGES], shell=True)
    f = open("output.txt", "w")
    f.write(result.stdout.decode('utf-8'))
    f.close()


def get_rpm_url(rpm_info):
    print(rpm_info)
    rpm_name, arch, version, repo = rpm_info.split()[0:4]
    if ":" in version:
        version = version.split(":")[1]
    rpm_full_name = rpm_name + "-" + version + "." + arch  + ".rpm"
    if repo == "rhel-basos":
        return BaseOS_url + rpm_full_name

    else:
        return Appstream_url + rpm_full_name

def get_src_rpm(rpm_path):
    result = subprocess.run(['rpm', '-qp', '--queryformat=%{sourcerpm}', rpm_path], stdout=subprocess.PIPE)
    return str(result.stdout.decode('utf-8'))


file_out = open("result.txt", "w")

for info in infos:
    rpm_url = get_rpm_url(info)
    src_rpm = get_src_rpm(rpm_url)
    file_out.write(src_rpm + "\n")

file_out.close()