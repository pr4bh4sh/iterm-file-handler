# -*- coding: utf-8 -*-

# https://github.com/dandavison/iterm2-dwim/blob/master/iterm2_dwim/parsers/parsers.py
__version__ = "0.0.3"

import sys, os, json

global cli_map
cli_map = {
    'java': 'idea',
    'rb': 'mine',
    'py': 'charm',
    'kt': 'studio',
    'txt': os.getenv('EDITOR', ''),
}


def main():
    _file, _line = _sanitize_params()
    _run([_get_cli(_file), _file, _line])


def _sanitize_params():
    global cli_map

    config_file = os.path.expanduser('~/.iterm_file_handler.json')

    if any(_arg in ['-O', 'override'] for _arg in sys.argv):
        with open(config_file, "w+") as jf:
            json.dump(cli_map, jf)
        print("Config file created at '{}', Please make the changes".format(
            config_file))
        sys.exit()

    if any(_arg in ['-h', 'help'] for _arg in sys.argv):
        # User a cli lib for parsing param
        print('''
        -h, help -- print help
        -O, override -- creates json file at '~/.iterm_file_handler.json' to override defalt file handler
        ''')
        sys.exit()

    if os.path.exists(config_file):
        with open(config_file, 'r') as jf:
            cli_map = json.load(jf)

    if ':' in sys.argv[1]:
        file, line = sys.argv[1].split(':')
    else:
        file, line = sys.argv[1:3]

    if not file.startswith('/'):
        """ Appending PWD if file path is not absolute"""
        file = sys.argv[3] + '/' + file

    if len(line) < 1:
        line = '1'
    return file, line


def _get_extention(file):
    if '.' in file:
        return file.split('.')[-1]
    raise RuntimeError("File extenstion not found in '{}'".format(file))


def _get_cli(for_file):
    try:
        from distutils.spawn import find_executable as which
        global cli_map
        name = cli_map.get(_get_extention(for_file), '')
        cli = (which(name, path='/usr/local/bin') or '/usr/bin/open')
        return cli
    except Exception as e:
        _log(e)
        _log('cli app is ---> ' + name)
        _log('cli path ---> ' + cli)


def _run(cmd):
    import subprocess
    args = sys.argv[1:]
    if '/usr/bin/open' in cmd:
        del cmd[-1]
    else:
        # converting file_name.rb:23 to --line 23 file_name.rb
        cmd[-2:] = ['--line',cmd[-2:][1], cmd[-2:][0]]

    out = subprocess.call(cmd)
    if (out is not 0) or ('test' in args):
        _log('Comand created --> ' + ' '.join(cmd))
        _log('Input passsed --> ' + str(args))


def _log(msg):
    import datetime
    log_file = os.path.expanduser('~/.iterm_file_handler.log')

    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write("[{}] {} \n".format(time_stamp, msg))
