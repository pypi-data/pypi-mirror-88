# Defines routine for `amz init`
import os, getpass
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import yaml
import subprocess as sp

from amz.loading import Loading
import amz.meta as meta
import amz.install as install

HOME_DIR = os.environ["HOME"]
PKG_DIR = os.path.dirname(__file__)
AMZ_DATA_DIR = HOME_DIR + '/.amz/data'


# General Initialization
def amz_gen_init(verbose=False):

    l = Loading("AMZ tool initialization routine")
    l.end(-2)

    # Check for `~/.amz` directory and make one if not there
    l.chain("Checking for `~/.amz` directory", "\t")
    AMZ_DIR_PRESENT = os.path.exists(f"{HOME_DIR}/.amz")
    if not AMZ_DIR_PRESENT:
        os.mkdir(f"{HOME_DIR}/.amz")

    # Copy data folder if contents do not match
    l.chain("Copying data", "\t", 0)
    try:
        copy_tree(f'{PKG_DIR}/data', f'{HOME_DIR}/.amz/data')
    except FileExistsError:
        l.end(1)

    # Update version info in amz-config yaml
    try:
        amz_user_config = yaml.load(open(f'{AMZ_DATA_DIR}/amz-config.yaml'), Loader=yaml.FullLoader)
        amz_user_config['amz_tool_meta']['version'] = open(f'{AMZ_DATA_DIR}/VERSION').readlines()[0]
        amz_user_config['amz_tool_meta']['user'] = getpass.getuser()
        with open(f'{AMZ_DATA_DIR}/amz-config.yaml', 'w') as f:
            yaml.dump(amz_user_config, f)
            f.close()
    except:
        l.end(1)

    # Source `data/amz_source.sh` at the end of bashrc if it's not present
    l.chain("Appending `source ~/.amz/data/amz_source.sh` to bashrc", "\t", 0)

    BASHRC_LINE_EXISTS = "source ~/.amz/data/amz_source.sh\n" in open(f"{HOME_DIR}/.bashrc", 'r').readlines()

    if not BASHRC_LINE_EXISTS:
        with open(f"{HOME_DIR}/.bashrc", 'a') as f:
            f.write("\n# AMZ Tool Helper \nsource ~/.amz/data/amz_source.sh\n")
            f.close()

    l.end(0)


# Repo Initialization
def amz_repo_init(verbose=False):

    l = Loading("Initializing AMZ Repo")
    l.end(-2)

    l.chain("Preliminary Checks - are you inside the repo root? ", "\t")
    l.end(-3)

    # Check if `amz init gen` has been executed
    AMZ_INIT_EXECUTED = os.path.exists(f"{HOME_DIR}/.amz/data/amz_source.sh")
    if not AMZ_INIT_EXECUTED:
        print("Run `amz init gen` first!")
        l.end(1)
        return

    # Ask if user is in AMZ_ROOT
    while True:
        IN_AMZ_ROOT = input("\t\t (y/n): ").lower()
        if IN_AMZ_ROOT == 'n':
            print("Please run this command from the repo root")
            l.end(1)
            return
        elif IN_AMZ_ROOT not in ['y', 'n']:
            print("Didn't quite catch you there!")
        else:
            break

    # Check if actually inside AMZ Repo
    if not os.path.exists('amz.yaml'):
        print("You are lying! Not in amz repo root")
        l.end(1)
        return

    # Fetch some data and write into amz-config YAML file
    l.chain("Configuring the repo", "\t", 0)

    # Set cur dir as AMZ Root and set git repo root
    amz_root_dir = os.getcwd()
    auto_repo = False
    try:
        amz_git_remote = open(f'{amz_root_dir}/.git/config', 'r').readlines()[6][7:-1]
        if 'autonomous' in amz_git_remote:
            auto_repo = True
    except:
        print("Is it a git repo??? and has a valid remote?")
        l.end(1)
        return

    if auto_repo:

        try:
            amz_user_config = yaml.load(open(f'{HOME_DIR}/.amz/data/amz-config.yaml'), Loader=yaml.FullLoader)
            amz_user_config['amz_repo_meta']['amz_root'] = amz_root_dir
            amz_user_config['amz_repo_meta']['amz_repo_git_src'] = amz_git_remote
            amz_user_config['amz_repo_meta']['amz_repo_config'] = f'{amz_root_dir}/amz.yaml'
            with open(f'{AMZ_DATA_DIR}/amz-config.yaml', 'w') as f:
                yaml.dump(amz_user_config, f)
                f.close()
        except:
            print("Some issue with data files... Run `amz init gen` again. ")
            l.end(1)
            return

        # Update `amz_source.sh` with AMZ_ROOT
        meta.update_line_in_file('export AMZ_ROOT=', f"export AMZ_ROOT={amz_root_dir}", f"{AMZ_DATA_DIR}/amz_source.sh")
        meta.update_line_in_file('export AMZ_DATA=', f"export AMZ_DATA={AMZ_DATA_DIR}", f"{AMZ_DATA_DIR}/amz_source.sh")

    # Setup githooks and Linter
    l.chain("Installing Githooks", "\t", 0)
    try:
        # Ensure to be in the amz root
        os.chdir(amz_root_dir)
        copy_file(f'{AMZ_DATA_DIR}/githooks/pre-commit', f'{amz_root_dir}/.git/hooks/pre-commit', link='hard')
    except:
        l.end(1)

    l.chain("Installing Linter", "\t", 0)
    try:
        # Ensure to be in the amz root
        os.chdir(amz_root_dir)
        meta.update_line_in_file('export AMZ_LINT=', f"export AMZ_LINT={AMZ_DATA_DIR}/linter/",
                                 f"{AMZ_DATA_DIR}/amz_source.sh")
        p1 = sp.run('sudo apt update && sudo apt install --yes python-pip python3-pip yapf pylint clang-format',
                    shell=True,
                    stdout=sp.PIPE,
                    stderr=sp.PIPE)
        # Still necessary for py2 deps
        p2 = sp.run('pip install requests pyyaml', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        p3 = sp.run(f'{AMZ_DATA_DIR}/linter/bin/init_linter_git_hooks', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        l.end(p1.returncode + p2.returncode + p3.returncode)
        print(f"\t\t Please run {meta.highlight_cmd('source ~/.bashrc')} now")
    except:
        l.end(1)

    # Clone submodules
    l.chain("Cloning submodules", "\t", 0)
    try:
        os.chdir(amz_root_dir)
        sp.run('git submodule update --init --recursive', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    except:
        l.end(1)

    # TODO: Clone bigfiles

    l.chain("Do you want to proceed with remaining setup? (Dependencies..)", "\t", 0)
    l.end(-3)
    INSTALL_DEPS = input('\t\t (y/n): ').lower()
    if INSTALL_DEPS == 'n':
        print("Exiting...")
        l.end(1)
        return
    elif INSTALL_DEPS not in ['y', 'n']:
        print("Didn't understand! - Exiting...")
        l.end(1)
        return

    # Repo Deps Config
    amz_repo_config = yaml.load(open(f'{amz_root_dir}/amz.yaml'), Loader=yaml.FullLoader)

    # TODO: Install ROS

    # Install apt deps
    try:
        APT_DEPS_DIR = f'{amz_root_dir}/{amz_repo_config["apt-deps"]}'
        install.apt_deps(APT_DEPS_DIR, verbose)
    except KeyError:
        l.chain("No apt dependencies file found", "\t")
        l.end(1)

    # Install python2 deps
    try:
        PY2_DEPS_DIR = f'{amz_root_dir}/{amz_repo_config["py2-deps"]}'
        install.py2_deps(PY2_DEPS_DIR, verbose)
    except KeyError:
        l.chain("No Py2 dependencies file found", "\t")
        l.end(1)

    # Install python3 deps
    try:
        PY3_DEPS_DIR = f'{amz_root_dir}/{amz_repo_config["py3-deps"]}'
        install.py3_deps(PY3_DEPS_DIR, verbose)
    except KeyError:
        l.chain("No Py3 dependencies file found", "\t")
        l.end(1)

    return