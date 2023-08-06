from __future__ import print_function
try:
    from shutil import which
except ImportError:
    def which(name):
        for path_dir in os.environ['PATH'].split(':'):
            if name in os.listdir(path_dir):
                return True
        return False
import shutil
import sys
import os
import tempfile
import zipfile


def find_all(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def find_so(path):
    for filename in find_all(path):
        if filename.lower().endswith('.so'):
            yield filename


def process_wheel(path):
    cwd = os.getcwd()

    tempdir = tempfile.mkdtemp()
    os.chdir(tempdir)

    if path.startswith('/'):
        path_to_file = path
    else:
        path_to_file = os.path.join(cwd, path)

    print('Processing %s' % (path_to_file, ))

    with zipfile.ZipFile(path_to_file, 'r') as zip_f:
        zip_f.extractall()

    for so_file in find_so('.'):
        os.system('strip %s' % (so_file, ))

    with zipfile.ZipFile(path_to_file, 'w') as zip_f:
        for file in find_all('.'):
            zip_f.write(file, compress_type=zipfile.ZIP_DEFLATED)

    os.chdir(cwd)
    shutil.rmtree(tempdir)


def run():
    try:
        sys.argv[1]
    except IndexError:
        print('Usage:'
              'doctor-wheel <path to whl1 file> <path to whl2 file> ...'
              'Files will be updated in place.', file=sys.stderr)
        sys.exit(1)

    if not shutil.which('strip'):
        print('This required strip to be installed', file=sys.stderr)
        sys.exit(1)

    for wheel_path in sys.argv[1:]:
        if not os.path.isfile(wheel_path):
            print('%s is not a file aborting' % (wheel_path, ), sys=sys.stderr)
            sys.exit(1)

    cwd = os.getcwd()

    for wheel_path in sys.argv[1:]:
        process_wheel(wheel_path)

    os.chdir(cwd)

    sys.exit(0)
