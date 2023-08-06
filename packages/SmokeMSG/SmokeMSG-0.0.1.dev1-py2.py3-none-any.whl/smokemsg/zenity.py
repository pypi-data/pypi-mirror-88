import subprocess
from os import environ


def _message(args, r=False):
    env = environ.copy()
    env["WINDOWID"] = ""

    p = subprocess.Popen(['zenity'] + args,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         env=env)
    if r:
        return p
    try:
        lines_iterator = iter(p.stdout.readline, b"")
        data = ""

        while p.poll() is None:

            for line in lines_iterator:
                nline = line.rstrip()
                nline = nline.decode("utf-8", "ignore")
                data += nline + "\n"
        if data != "":
            data = data[:-1]
        return not p.poll(), data

    finally:

        if p.poll() is None:  # pragma: no cover
            p.kill()


works, __version__ = _message(['--version'])

if not works:
    raise ImportError

_list = list

class fake:
    pass


def kwargshelper(kwargs):
    result = []
    for i in kwargs:
        if isinstance(kwargs[i], _list):
            for item in kwargs[i]:
                result.append("--" + i.replace("_", "-") + "=" + str(item))
        if kwargs[i] == False:
            continue
        elif kwargs[i] == None:
            continue
        elif kwargs[i] == True:
            result.append("--" + i.replace("_", "-"))
        else:
            result.append("--" + i.replace("_", "-") + "=" + str(kwargs[i]))
    return result


def argshelper(avargs, args, kwargs, name):
    for i in range(len(args)):
        if args[i] == None:
            continue
        try:
            kwargs[avargs[i]] = args[i]
        except IndexError:
            raise TypeError(name + "() takes " + str(len(avargs)) +
                            " positional argument(s) but " + str(len(args)) +
                            " were given")
    return kwargs


def calendar(*args, **kwargs):
    """Display calendar dialog"""
    date_format = None
    avargs = ("text", "date", "month", "year", "date_format")
    kwargs = argshelper(avargs, args, kwargs, calendar.__name__)
    if kwargs.get("date_format"):
        date_format = kwargs.get("date_format")
        kwargs["date_format"] = None
    r = _message(["--calendar"] + kwargshelper(kwargs))
    if r[0]:
        date = r[1].split("/")
        if date_format:
            return date_format.replace("yyyy", str(date[2])).replace(
                "yy", str(date[2])).replace("mm", str(date[1])).replace(
                    "dd", str(date[0]))
        return str(date[0]), str(date[1]), str(date[2])
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def entry(*args, **kwargs):
    """Display entry dialog"""
    avargs = ("text", "entry_text", "hide_text")
    kwargs = argshelper(avargs, args, kwargs, entry.__name__)
    r = _message(["--entry"] + kwargshelper(kwargs))
    if r[0]:
        return r[1]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def error(*args, **kwargs):
    """Display error dialog"""
    avargs = ("text", "icon_name", "no_wrap", "no_markup", "ellipsize")
    kwargs = argshelper(avargs, args, kwargs, error.__name__)
    r = _message(["--error"] + kwargshelper(kwargs))
    if r[0]:
        return r[0]
    elif r[0] == False:
        return r[0]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def info(*args, **kwargs):
    """Display info dialog"""
    avargs = ("text", "icon_name", "no_wrap", "no_markup", "ellipsize")
    kwargs = argshelper(avargs, args, kwargs, info.__name__)
    r = _message(["--info"] + kwargshelper(kwargs))
    if r[0]:
        return r[0]
    elif r[0] == False:
        return r[0]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def file_selection(*args, **kwargs):
    """Display file selection dialog"""
    extra = []
    if len(args) > 6:
        for i in args[6]:
            extra.append("--file-filter=" + i[0] + "|" + i[1])
        args[6] = None
    if kwargs.get("file_filter"):
        for i in kwargs.get("file_filter"):
            extra.append("--file-filter=" + i[0] + "|" + i[1])
        kwargs["file_filter"] = None
    avargs = ("filename", "multiple", "directory", "save", "separator",
              "confirm_overwrite", "file_filter")
    kwargs = argshelper(avargs, args, kwargs, file_selection.__name__)
    r = _message(["--file-selection"] + kwargshelper(kwargs))
    if r[0]:
        if kwargs.get("multiple"):
            return r[1].split(kwargs.get("separator", "|"))
        return r[1]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def list(*args, **kwargs):
    """Display list dialog"""
    extra = []
    max_len = 0
    if len(args) > 1:
        for i in args[1]:
            if len(i) > max_len:
                max_len = len(i)
        for i in args[1]:
            while len(i) != max_len:
                i.append(" ")
        for i in args[1]:
            extra.append("--column=" + str(i[0]))
        for item in range(len(args[1][0])):
            if item == 0:
                continue
            for i in args[1]:
                extra.append(str(i[item]))
    elif kwargs.get("columns"):
        for i in kwargs.get("columns"):
            if len(i) > max_len:
                max_len = len(i)
        for i in kwargs.get("columns"):
            while len(i) != max_len:
                i.append("")
        for i in kwargs.get("columns"):
            extra.append("--column=" + str(i[0]))
        for item in range(len(kwargs.get("columns")[0])):
            if item == 0:
                continue
            for i in kwargs.get("columns"):
                extra.append(str(i[item]))
    else:
        raise TypeError("columns option required")
    avargs = ("text", "columns", "checklist", "radiolist", "imagelist",
              "separator", "multiple", "editable", "print_column",
              "hide_column", "hide_header", "mid_search")
    kwargs = argshelper(avargs, args, kwargs, list.__name__)
    del kwargs["columns"]
    r = _message(["--list"] + kwargshelper(kwargs) + extra)
    if r[0]:
        if kwargs.get("multiple"):
            return r[1].split(kwargs.get("separator", "|"))
        return r[1]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def notification(*args, **kwargs):
    """Display notification"""
    avargs = ("text", "listen", "hint")
    kwargs = argshelper(avargs, args, kwargs, notification.__name__)

    def update(**kw):
        """Call back function to update progress bar.

        Returns:
            status : returncode of the proc
        """
        for i in kw:
            p.stdin.write(i + ":" + str(kw[i]) + "\n")
        p.stdin.flush()
        return p.returncode

    if kwargs.get("listen"):
        p = subprocess.Popen(['zenity'] + ["--notification"] + kwargshelper(kwargs),
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
        return update
    return _message(["--notification"] + kwargshelper(kwargs))[0]


def progress(*args, **kwargs):
    """Display progress indication"""
    avargs = ("text", "percentage", "pulsate", "auto_close", "auto_kill",
              "no_cancel", "time_remaining")
    kwargs = argshelper(avargs, args, kwargs, progress.__name__)

    # thanks D V Sagar yad.py

    def update(percent):
        """Call back function to update progress bar.

        Args:
            percent (int|float) : set percentage of the bar.

        Returns:
            status : returncode of the proc
        """
        if isinstance(percent, float):
            p.stdin.write('%f\n' % percent)
        else:
            p.stdin.write('%d\n' % int(percent))
        p.stdin.flush()
        return p.returncode

    def read():
        data = p.stdout.read()[:-1]
        if data == kwargs.get("extra_button"):
            return data
        return not p.poll

    p = subprocess.Popen(['zenity'] + ["--progress"] + kwargshelper(kwargs),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
    r = fake()
    r.update = update
    r.kill = p.kill
    r.read = read
    return r


def question(*args, **kwargs):
    """Display question dialog"""
    avargs = ("text", "icon_name", "no_wrap", "no_markup", "default_cancel",
              "ellipsize")
    kwargs = argshelper(avargs, args, kwargs, question.__name__)
    r = _message(["--question"] + kwargshelper(kwargs))
    if r[0]:
        return r[0]
    elif r[0] == False:
        return r[0]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def warning(*args, **kwargs):
    """Display warning dialog"""
    avargs = ("text", "icon_name", "no_wrap", "no_markup", "ellipsize")
    kwargs = argshelper(avargs, args, kwargs, warning.__name__)
    r = _message(["--warning"] + kwargshelper(kwargs))
    if r[0]:
        return r[0]
    elif r[0] == False:
        return r[0]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def partial(p):
    try:
        lines_iterator = iter(p.stdout.readline, b"")

        while p.poll() is None:

            for line in lines_iterator:
                nline = line.rstrip()
                nline = nline.decode("utf-8", "ignore")
                yield int(nline)
    finally:

        if p.poll() is None:  # pragma: no cover
            p.kill()
    return


def scale(*args, **kwargs):
    """Display scale dialog"""
    avargs = ("text", "value", "min_value", "max_value", "step",
              "print_partial", "hide_value")
    kwargs = argshelper(avargs, args, kwargs, scale.__name__)
    if kwargs.get("print_partial"):
        p = _message(["--scale"] + kwargshelper(kwargs), True)
        return partial(p)
    r = _message(["--scale"] + kwargshelper(kwargs))
    if r[0]:
        return int(r[1])
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def text_info(*args, **kwargs):
    """Display text information dialog"""
    avargs = ("filename", "editable", "font", "checkbox", "html",
              "no_interaction", "url", "auto_scroll")
    kwargs = argshelper(avargs, args, kwargs, text_info.__name__)

    # thanks D V Sagar yad.py

    def update(text):
        """Call back function to update progress bar.

        Args:
            text (str) : append text to the text info.

        Returns:
            status : returncode of the proc
        """
        p.stdin.write(str(text))
        p.stdin.flush()
        return p.returncode

    if kwargs.get("auto_scroll"):
        p = subprocess.Popen(['zenity'] + ["--text-info"] + kwargshelper(kwargs),
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
        if kwargs.get("editable"):
            r = fake()
            r.update = update
            r.read = p.stdout.read
            return r
        return update
    r = _message(["--text-info"] + kwargshelper(kwargs))
    if kwargs.get("editable"):
        if r[0]:
            return r[1]
        else:
            return

    return r[0]


def color_selection(*args, **kwargs):
    """Display color selection dialog"""
    avargs = ("color", "show_palette")
    kwargs = argshelper(avargs, args, kwargs, color_selection.__name__)
    r = _message(["--color-selection"] + kwargshelper(kwargs))
    if r[0]:
        if r[1].startswith("rgba"):
            c = r[1][5:-1].split(",")
            return int(c[0]), int(c[1]), int(c[2]), float(c[3])
        elif r[1].startswith("rgb"):
            c = r[1][4:-1].split(",")
            return int(c[0]), int(c[1]), int(c[2])
        else:
            return
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


def password(*args, **kwargs):
    """Display password dialog"""
    avargs = ["username"]
    kwargs = argshelper(avargs, args, kwargs, password.__name__)
    r = _message(["--password"] + kwargshelper(kwargs))
    if r[0]:
        if kwargs.get("username"):
            # password and username cannot contain "|" use forms instead
            return r[1].split("|")[2]
        return r[1]
    elif r[1][:-1] == kwargs.get("extra_button"):
        return r[1][:-1]
    elif isinstance(kwargs.get("extra_button"), _list):
        for i in kwargs.get("extra_button"):
            if r[1][:-1] == str(i):
                return i


class form():
    def __init__(self):
        self.extra = []

    def add_entry(self, name="Enter:"):
        self.extra.append("--add-entry=" + name)

    def add_password(self, name="Password:"):
        self.extra.append("--add-password=" + name)

    def add_calendar(self, name="Date:"):
        self.extra.append("--add-calendar=" + name)

    def add_list(self, name="Choose:", columns=None, show_header=False):
        self.extra.append("--add-list=" + name)
        max_len = 0
        if columns:
            for i in columns:
                if len(i) > max_len:
                    max_len = len(i)
            for i in columns:
                while len(i) != max_len:
                    i.append(" ")
            column_values = ""
            for i in columns:
                column_values += str(i[0]) + "|"
            if len(column_values):
                column_values = column_values[:-1]
            self.extra.append("--column-values=" + column_values)
            if show_header:
                self.extra.append("--show-header")
            list_values = ""
            for item in range(len(columns[0])):
                if item == 0:
                    continue
                for i in columns:
                    list_values += str(i[item]) + "|"
            if len(list_values):
                list_values = list_values[:-1]
            self.extra.append("--list-values=" + list_values)

    def add_combo(self, name, values):
        self.extra.append("--add-combo=" + name)
        max_len = 0
        if values:
            combo_values = ""
            for i in values:
                combo_values += str(i) + "|"
            if len(combo_values):
                combo_values = combo_values[:-1]
            self.extra.append("--combo-values=" + combo_values)

    def show(self, *args, **kwargs):
        """Display forms dialog"""
        avargs = ("text", "separator")
        kwargs = argshelper(avargs, args, kwargs, "forms.show")
        r = _message(["--forms"] + kwargshelper(kwargs) + self.extra)
        if r[0]:
            retval = r[1].split(kwargs.get("separator", "|"))
            if retval != "":
                return retval
        elif r[1][:-1] == kwargs.get("extra_button"):
            return r[1][:-1]
        elif isinstance(kwargs.get("extra_button"), _list):
            for i in kwargs.get("extra_button"):
                if r[1][:-1] == str(i):
                    return i


alert = info

confirm = question

prompt = entry
