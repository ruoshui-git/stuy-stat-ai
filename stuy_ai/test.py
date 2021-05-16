from subprocess import Popen

def display(*args: str):
    try:
        p = Popen('imdisplay ' + ' '.join(args))
    except FileNotFoundError as e:
        p = Popen('display '  + ' '.join(args))

    p.communicate()


def convert(*args: str):
    try:
        p = Popen('magick ' + ' '.join(args))
    except FileNotFoundError:
        p = Popen('convert ' + ' '.join(args))

    p.communicate()

convert('img.ppm', 'img.gif')