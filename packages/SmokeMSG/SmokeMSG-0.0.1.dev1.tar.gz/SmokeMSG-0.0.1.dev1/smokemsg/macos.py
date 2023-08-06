import sys
import subprocess
import time


def test_call(*args, **kwargs):
    try:
        subprocess.check_output(*args, **kwargs)
        return True
    except Exception:
        return False


def check_output(*args, **kwargs):
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.STDOUT

    p = subprocess.Popen(*args, **kwargs)

    try:
        while p.poll() is None:
            time.sleep(0.002)
        return p.poll(), p.stdout.read().decode("utf-8", "ignore")
    finally:
        if p.poll() is None:  # pragma: no cover
            p.kill()


def _message(title, message, *more):
    message = message.replace('"', u"\u201C").replace("'", u"\u2018")
    if sys.version_info[0] == 2:
        message = message.encode("utf-8")
    t = "tell app (path to frontmost application as text) "
    t += 'to display dialog "%s" with title "%s"'
    t += " " + " ".join(more)
    retcode, res = check_output(["osascript", "-e", t % (message, title)])
    resmap = {
        "no": False,
        "cancel": False,
        "ok": True,
        "retry": True,
        "yes": True
    }
    return resmap.get(res.strip().split(":")[-1].lower(), None)


if not test_call(["osascript", "-e", 'return "hi"']):
    raise ImportError


def alert(text='All updates are complete.', title='Information', icon='note'):
    icon = icon.replace('info', 'note').replace('warning', 'caution').replace(
        'question', 'caution').replace('error', 'stop')
    return _message(title, text, "with icon " + icon, 'buttons {"OK"}')


def confirm(text='Are you sure you want to proceed?',
            title='Question',
            icon='caution'):
    icon = icon.replace('info', 'note').replace('warning', 'caution').replace(
        'question', 'caution').replace('error', 'stop')
    return _message(title, text, "with icon " + icon, 'buttons {"Yes", "No"}')


def prompt(message='Enter new text:', title='Add a new entry'):
    raise NotImplementedError
