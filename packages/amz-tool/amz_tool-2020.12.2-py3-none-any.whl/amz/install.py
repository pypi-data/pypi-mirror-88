# Handles install routine - `amz install`
import subprocess as sp
import os

from amz.loading import Loading


def apt_deps(filepath, verbose=False):

    filepath_display = filepath
    # Check file exists
    try:
        if os.path.exists(filepath):
            if len(filepath) > 30:
                filepath_display = f'...{filepath[-25:]}'
        else:
            print(f'{filepath} - file does not exist')
            print('Exiting...')
            return
    except:
        return

    l = Loading(f"Installing apt dependencies from - {filepath_display}")
    l.end(-2)

    p0 = sp.run('apt list --installed', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    apt_exist_list = [x.split("/")[0].lower() for x in p0.stdout.decode().split('\n')]
    apt_dep_list = open(filepath, 'r').read().split('\n')

    # Refine Lists not to contain comments(#) or empty lines
    apt_dep_list = [pkg for pkg in apt_dep_list if pkg != '' and '#' not in pkg]

    for package in apt_dep_list:
        if package.lower() in apt_exist_list:
            if not verbose:
                l.chain(f'{package} already installed', '\t')
                l.end(0)
            elif verbose:
                print(f'{package} already installed')
        elif package.lower() not in apt_exist_list:
            if not verbose: l.chain(f'{package}', '\t')
            p = sp.run(f'sudo apt --yes install {package}',
                       shell=True,
                       stdout=(None if verbose else sp.PIPE),
                       stderr=(None if verbose else sp.PIPE))
            if not verbose: l.end(p.returncode)


def py2_deps(filepath, verbose=False):

    filepath_display = filepath
    # Check file exists
    try:
        if os.path.exists(filepath):
            if len(filepath) > 30:
                filepath_display = f'...{filepath[-25:]}'
        else:
            print(f'{filepath} - file does not exist')
            print('Exiting...')
            return
    except:
        return

    l = Loading(f"Installing Py2 dependencies from - {filepath_display}")
    l.end(-2)

    p0 = sp.run('pip list', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    py2_exist_list = [x.split(" ")[0].lower() for x in p0.stdout.decode().split('\n')]
    py2_dep_list = open(filepath, 'r').read().split('\n')

    # Refine Lists not to contain comments(#) or empty lines
    py2_dep_list = [pkg for pkg in py2_dep_list if pkg != '' and '#' not in pkg]

    for package in py2_dep_list:
        if package.lower() in py2_exist_list:
            if not verbose:
                l.chain(f'{package} already installed', '\t')
                l.end(0)
            elif verbose:
                print(f'{package} already installed')
        elif package.lower() not in py2_exist_list:
            if not verbose: l.chain(f'{package}', '\t')
            p = sp.run(f'pip install {package}',
                       shell=True,
                       stdout=(None if verbose else sp.PIPE),
                       stderr=(None if verbose else sp.PIPE))
            if not verbose: l.end(p.returncode)


def py3_deps(filepath, verbose=False):

    filepath_display = filepath
    # Check file exists
    try:
        if os.path.exists(filepath):
            if len(filepath) > 30:
                filepath_display = f'...{filepath[-25:]}'
        else:
            print(f'{filepath} - file does not exist')
            print('Exiting...')
            return
    except:
        return

    l = Loading(f"Installing Py3 dependencies from - {filepath_display}")
    l.end(-2)

    p0 = sp.run('pip3 list', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    py3_exist_list = [x.split(" ")[0].lower() for x in p0.stdout.decode().split('\n')]
    py3_dep_list = open(filepath, 'r').read().split('\n')

    # Refine Lists not to contain comments(#) or empty lines
    py3_dep_list = [pkg for pkg in py3_dep_list if pkg != '' and '#' not in pkg]

    for package in py3_dep_list:
        if package.lower() in py3_exist_list:
            if not verbose:
                l.chain(f'{package} already installed', '\t')
                l.end(0)
            elif verbose:
                print(f'{package} already installed')
        elif package.lower() not in py3_exist_list:
            if not verbose: l.chain(f'{package}', '\t')
            p = sp.run(f'pip3 install {package}',
                       shell=True,
                       stdout=(None if verbose else sp.PIPE),
                       stderr=(None if verbose else sp.PIPE))
            if not verbose: l.end(p.returncode)


def script(filepath, verbose=False):
    pass