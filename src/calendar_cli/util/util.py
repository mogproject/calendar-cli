from __future__ import division, print_function, absolute_import, unicode_literals

import os
import errno
import subprocess
import six


#
# Path operation
#
def normalize_path(path, base_dir):
    return path if os.path.isabs(path) else os.path.join(base_dir, path)


#
# Process operation
#
def execute_command(args, shell=False, cwd=None, env=None, stdin=None, stdout=None, stderr=None):
    """
    Execute external command

    :param args: command line arguments : [string]
    :param shell: True when using shell : boolean
    :param cwd: working directory : string
    :param env: environment variables : dict
    :param stdin: standard input
    :param stdout: standard output
    :param stderr: standard error
    :return: return code
    """
    return subprocess.call(args=args, shell=shell, cwd=cwd, env=dict(os.environ, **(oget(env, {}))),
                           stdin=stdin, stdout=stdout, stderr=stderr)


def capture_command(args, shell=False, cwd=None, env=None, stdin=None):
    """
    Execute external command and capture output

    :param args: command line arguments : [string]
    :param shell: True when using shell : boolean
    :param cwd: working directory : string
    :param env: environment variables : dict
    :param stdin: standard input
    :return: tuple of return code, stdout data and stderr data
    """
    p = subprocess.Popen(
        args, shell=shell, cwd=cwd, env=dict(os.environ, **(oget(env, {}))),
        stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    return p.returncode, stdout_data, stderr_data


def execute_command_with_pid(args, pid_file=None, shell=False, cwd=None, env=None,
                             stdin=None, stdout=None, stderr=None):
    if pid_file is None:
        return execute_command(args, shell, cwd, env, stdin, stdout, stderr)
    else:
        try:
            p = subprocess.Popen(
                args, shell=shell, cwd=cwd, env=dict(os.environ, **(oget(env, {}))),
                stdin=stdin, stdout=stdout, stderr=stderr)
            with open(pid_file, 'w') as f:
                f.write(str(p.pid))
            ret = p.wait()
        finally:
            # clean up pid file
            if pid_file is not None and os.path.exists(pid_file):
                os.remove(pid_file)
        return ret


def pid_exists(pid):
    # Steeled from https://github.com/giampaolo/psutil/blob/master/psutil/_psposix.py
    """Check whether pid exists in the current process table."""
    if pid == 0:
        # According to "man 2 kill" PID 0 has a special meaning:
        # it refers to <<every process in the process group of the
        # calling process>> so we don't want to go any further.
        # If we get here it means this UNIX platform *does* have
        # a process with id 0.
        return True
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH) therefore we should never get
            # here. If we do let's be explicit in considering this
            # an error.
            raise err
    else:
        return True


#
# Functional operation
#
def omap(function, optional):
    """Map optional value"""
    return None if optional is None else function(optional)


def oget(optional, default=None):
    return default if optional is None else optional


def ozip(optional1, optional2):
    return None if optional1 is None or optional2 is None else (optional1, optional2)


#
# String util
#
def is_unicode(s):
    return (six.PY2 and isinstance(s, unicode)) or (six.PY3 and isinstance(s, str))


def is_strlike(s):
    return isinstance(s, (six.string_types, bytes))


def to_unicode(s, encoding=None, errors='strict'):
    """
    Make unicode string from any value
    :param s:
    :param encoding:
    :param errors:
    :return: unicode
    """
    encoding = encoding or 'utf-8'

    if is_unicode(s):
        return s
    elif is_strlike(s):
        return s.decode(encoding, errors)
    else:
        if six.PY2:
            return str(s).decode(encoding, errors)
        else:
            return str(s)


def to_str(s, encoding=None, errors='strict'):
    """
    Make str from any value
    :param s:
    :param encoding:
    :param errors:
    :return: str (not unicode in Python2, nor bytes in Python3)
    """
    encoding = encoding or 'utf-8'

    if is_strlike(s):
        if six.PY2:
            return s.encode(encoding, errors) if isinstance(s, unicode) else s
        else:
            return s.decode(encoding, errors) if isinstance(s, bytes) else s
    else:
        return str(s)


def universal_print(output, str_or_bytes, encoding='utf-8'):
    """Print unicode or bytes universally"""

    if is_unicode(str_or_bytes):
        bs = str_or_bytes.encode(encoding)
    else:
        bs = str_or_bytes

    if hasattr(output, 'buffer'):
        output.buffer.write(bs)
    else:
        try:
            output.write(bs)
        except TypeError:
            output.write(str_or_bytes)

    output.flush()
