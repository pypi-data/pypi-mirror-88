
import json
import platform
import os
import shutil
import stat
import subprocess
import sys
import tarfile

try:
    from urllib.request import urlretrieve, urlopen
except:
    # Python 2
    from urllib import urlretrieve
    from urllib2 import urlopen

from modian import PREFIXES

def conda_package_url(name, version=None, label="main"):
    system = platform.system().lower()
    machine = platform.machine()
    if system == "windows":
        system = "win"
        machine = "x86_64" if machine == "AMD64" else "x86"
    fd = urlopen("http://api.anaconda.org/package/{}".format(name))
    data = json.load(fd)
    fd.close()
    if version is None:
        version = data["latest_version"]
    b = None
    for f in data["files"]:
        if f["version"] != version:
            continue
        if label not in f["labels"]:
            continue
        if f["attrs"]["operatingsystem"] is not None:
            if f["attrs"]["operatingsystem"] != system and f["attrs"]["platform"] != system:
                continue
            if f["attrs"]["machine"] != machine and f["attrs"]["arch"] != machine :
                continue
        if b is None or f["attrs"]["build_number"] > b["attrs"]["build_number"]:
            b = f
    return "http:{}".format(b["download_url"]) if b else None

def prepare_dest(dest):
    destdir = os.path.dirname(dest)
    if not os.path.exists(destdir):
        os.makedirs(destdir)

def conda_package_extract(conda_url, prefix):
    print("downloading {}".format(conda_url))
    localfile = urlretrieve(conda_url)[0]
    fmt = conda_url.split(".")[-1]
    def match_member(m):
        return m.name.split('/')[0] != 'info'
    with tarfile.open(localfile, "r:%s"%fmt) as tar:
        for m in tar:
            if match_member(m):
                dest = os.path.join(prefix, m.name)
                print("installing %s" % dest)
                tar.extract(m, prefix)
    os.unlink(localfile)

def is_installed(progname):
    if sys.version_info[0] < 3:
        paths = os.environ["PATH"].split(":")
        for p in paths:
            if os.path.exists(os.path.join(p, progname)):
                return True
        return False
    print(shutil.which(progname))
    return shutil.which(progname) is not None

def installation_prefix():
    if platform.system() == "Windows":
        return PREFIXES[0]
    if os.getuid() == 0:
        return PREFIXES[0]
    else:
        return PREFIXES[-1]

def setup(*specs):
    in_conda = os.path.exists(os.path.join(sys.prefix, 'conda-meta'))
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-f", "--force", default=False, action="store_true",
            help="Force installation")
    args = parser.parse_args()
    prefix = installation_prefix()
    for spec in specs:
        name = spec["pkg"].split('/')[-1]
        if not args.force:
            print("# checking for {}".format(name))
            skip = True
            for prog in spec.get("check_progs", []):
                if not is_installed(prog):
                    skip = False
                    break
            if skip and "check_install" in spec:
                skip = spec["check_install"]()
            if skip:
                print("# {} is already installed.".format(name))
                continue
        print("# installing {} in {}".format(spec["pkg"], prefix))
        if "install" in spec:
            spec["install"](prefix)
            continue
        if in_conda:
            subprocess.call(["conda", "install", spec["pkg"].split("/")[-1]])
            continue
        pkg = conda_package_url(spec["pkg"], version=spec.get("version"))
        if pkg is None:
            print("Error: no package found for your system!")
            continue
        conda_package_extract(pkg, prefix)

def nusmv_install(prefix):
    def chmod_x(filename):
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    def prepare_dest(dest):
        destdir = os.path.dirname(dest)
        if not os.path.exists(destdir):
            os.makedirs(destdir)

    def install_bin_from_tar(tar, member, dest):
        fd = tar.extractfile(member)
        print("installing %s" % dest)
        prepare_dest(dest)
        with open(dest, "wb") as o:
            o.write(fd.read())
        fd.close()
        chmod_x(dest)

    def install_from_tarurl(url, match_member, prefix):
        localfile = urlretrieve(url)[0]
        if url.endswith(".gz"):
            mode = "r:gz"
        elif url.endswith(".bz2"):
            mode = "r:bz2"
        with tarfile.open(localfile, mode) as t:
            for m in t:
                if match_member(m):
                    dest = os.path.join(prefix, "bin", os.path.basename(m.name))
                    install_bin_from_tar(t, m, dest)
        os.unlink(localfile)

    system = platform.system().lower()
    if system == "linux":
        system = "%s%s" % (system, platform.architecture()[0][:2])
    #url_pat = "http://nusmv.fbk.eu/distrib/NuSMV-2.6.0-%s.tar.gz"
    url_pat = "https://loicpauleve.name/share/NuSMV-2.6.0-%s.tar.gz"
    binfile = {
        "linux64": "https://api.anaconda.org/download/colomoto/nusmv/2.6.0/linux-64/nusmv-2.6.0-0.tar.bz2",
        "linux32": url_pat % "linux32",
        "darwin": "https://api.anaconda.org/download/colomoto/nusmv/2.6.0/osx-64/nusmv-2.6.0-0.tar.bz2",
        "windows": url_pat % "win32",
    }
    binfile = binfile.get(system)
    def match_entry(m):
        return m.name.endswith("bin/NuSMV") \
            or  m.name.endswith("bin/NuSMV.exe")
    install_from_tarurl(binfile, match_entry, prefix)

setup({"pkg": "conda-forge/graphviz", "version": "2.38.0", "check_progs": ["dot"]},
        {"pkg": "colomoto/nusmv", "check_progs": ["NuSMV"], "install": nusmv_install})

