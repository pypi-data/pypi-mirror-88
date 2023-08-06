import sys, ctypes

MB_OK = 0x0
MB_OKCANCEL = 0x1
MB_ABORTRETRYIGNORE = 0x2
MB_YESNOCANCEL = 0x3
MB_YESNO = 0x4
MB_RETRYCANCEL = 0x5
MB_CANCELTRYCONTINUE = 0x6

NO_ICON = 0
STOP = MB_ICONHAND = MB_ICONSTOP = MB_ICONERRPR = 0x10
QUESTION = MB_ICONQUESTION = 0x20
WARNING = MB_ICONEXCLAIMATION = 0x30
INFO = MB_ICONASTERISK = MB_ICONINFOMRAITON = 0x40

MB_DEFAULTBUTTON1 = 0x0
MB_DEFAULTBUTTON2 = 0x100
MB_DEFAULTBUTTON3 = 0x200
MB_DEFAULTBUTTON4 = 0x300

MB_SETFOREGROUND = 0x10000
MB_TOPMOST = 0x40000

IDABORT = 0x3
IDCANCEL = 0x2
IDCONTINUE = 0x11
IDIGNORE = 0x5
IDNO = 0x7
IDOK = 0x1
IDRETRY = 0x4
IDTRYAGAIN = 0x10
IDYES = 0x6

py2 = sys.version_info[0] == 2
if py2:
    messageBoxFunc = ctypes.windll.user32.MessageBoxA
else:  # Python 3 functions.
    messageBoxFunc = ctypes.windll.user32.MessageBoxW


def alert(text='All updates are complete.', title='Alert', icon=INFO):
    return messageBoxFunc(0, text, title,
                   MB_OK | MB_SETFOREGROUND | MB_TOPMOST | icon)


def confirm(text='Are you sure you want to proceed?',
            title='Question',
            icon=QUESTION):
    return messageBoxFunc(0, text, title, MB_YESNO | MB_SETFOREGROUND
                          | MB_TOPMOST | icon) == IDYES


def prompt(*args, **kwargs):
    raise NotImplementedError
