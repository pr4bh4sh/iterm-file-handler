#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/dandavison/iterm2-dwim/blob/master/iterm2_dwim/parsers/parsers.py
__version__ = "0.0.3"

import sys, os, json, re


global cli_map
cli_map = {
    'java': 'idea',
    'rb': 'mine',
    'ruby': 'mine',
    'py': 'charm',
    'python': 'charm',
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

        Set `/usr/local/bin/itfh "\1" "\2" "\5" 'test'` in Iterm2 settings > profile > Advandced > Run Command
        To activate itfh
        ''')
        sys.exit()

    if os.path.exists(config_file):
        with open(config_file, 'r') as jf:
            cli_map.update(json.load(jf))

    if ':' in sys.argv[1]:
        file, line = sys.argv[1].split(':')
    elif sys.argv[2].isnumeric() and os.path.exists(sys.argv[1]):
        file, line = sys.argv[1], sys.argv[2]
    elif 'line' in sys.argv[4]:
        # for ruby pry session
        try:
            file, line = sys.argv[1],re.search('line.* (\d+)',sys.argv[4]).group(1)
        except:
            file, line = sys.argv[1], '1'
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
    elif os.path.exists(file.split(':')[0]):
        # getting file type from shebang
        with open(file.split(':')[0]) as f:
            first_line = f.readline().rstrip()
            # _log('first_line --> ' + first_line)
            file_type = first_line.split(' ')[-1]
            # _log('file_type --> ' + file_type)
            return file_type


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
        out = subprocess.call(cmd)
    if 'mine' in cmd[0]:
        import requests
        out = requests.get(f"http://localhost:63342/api/file/{cmd[1]}:{cmd[2]}").status_code
    else:
        # converting file_name.rb:23 to --line 23 file_name.rb
        cmd[-2:] = ['--line',cmd[-2:][1], cmd[-2:][0]]

    if (out != 0 or out == 200) or ('test' in args):
        _log('Comand created --> ' + ' '.join(cmd))
        _log('Input passsed --> ' + str({k+1 : v for k, v in enumerate(args)}))
        _log('Command for debug --> ' + "/usr/local/bin/itfh " + ' '.join(['"{0}"'.format(x) for x in args]))
        _log('')
        # _log('Input passsed --> ' + str(args))


def _log(msg):
    import datetime
    log_file = os.path.expanduser('~/.iterm_file_handler.log')

    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write("[{}] {} \n".format(time_stamp, msg))


if __name__ == '__main__':
    main()