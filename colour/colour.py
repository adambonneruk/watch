"""
https://stackoverflow.com/questions/2330245/python-change-text-color-in-shell
Use Curses or ANSI escape sequences. Before you start spouting escape sequences, you should check that stdout is a tty. You can do this with sys.stdout.isatty(). Here's a function pulled from a project of mine that prints output in red or green, depending on the status, using ANSI escape sequences:
"""
import sys

def colourise(string: str = "", fg_colour: str = "", bold: bool = False) -> str:
    attributes = []

    if fg_colour == "black":
        attributes.append('30')
    elif fg_colour == "red":
        attributes.append('31')
    elif fg_colour == "green":
        attributes.append('32')
    elif fg_colour == "yellow":
        attributes.append('33')
    elif fg_colour == "blue":
        attributes.append('34')
    elif fg_colour == "magenta":
        attributes.append('35')
    elif fg_colour == "cyan":
        attributes.append('36')
    elif fg_colour == "white":
        attributes.append('37')
    elif fg_colour == "grey":
        attributes.append('90')
    elif fg_colour == "light-red":
        attributes.append('91')
    elif fg_colour == "light-green":
        attributes.append('92')
    elif fg_colour == "light-yellow":
        attributes.append('93')
    elif fg_colour == "light-blue":
        attributes.append('94')
    elif fg_colour == "light-magenta":
        attributes.append('95')
    elif fg_colour == "light-cyan":
        attributes.append('96')
    elif fg_colour == "light-white":
        attributes.append('97')

    if bold:
        attributes.append("1")

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attributes), string)

def main():
    # Colours
    print("some " + colourise("Normal") + " text")
    print("some " + colourise("Black","black") + " text")
    print("some " + colourise("Red","red") + " text")
    print("some " + colourise("Green","green") + " text")
    print("some " + colourise("Yellow","yellow") + " text")
    print("some " + colourise("Blue","blue") + " text")
    print("some " + colourise("Magenta","magenta") + " text")
    print("some " + colourise("Cyan","cyan") + " text")
    print("some " + colourise("White","white") + " text")

    # Lighter Colours
    print("some " + colourise("Light-Grey","grey") + " text")
    print("some " + colourise("Light-Red","light-red") + " text")
    print("some " + colourise("Light-Green","light-green") + " text")
    print("some " + colourise("Light-Yellow","light-yellow") + " text")
    print("some " + colourise("Light-Blue","light-blue") + " text")
    print("some " + colourise("Light-Magenta","light-magenta") + " text")
    print("some " + colourise("Light-Cyan","light-cyan") + " text")
    print("some " + colourise("Light-White","light-white") + " text")

    # Bold Colours
    print("some " + colourise("Bold Normal","",True) + " text")
    print("some " + colourise("Bold Black","black",True) + " text")
    print("some " + colourise("Bold Red","red",True) + " text")
    print("some " + colourise("Bold Green","green",True) + " text")
    print("some " + colourise("Bold Yellow","yellow",True) + " text")
    print("some " + colourise("Bold Blue","blue",True) + " text")
    print("some " + colourise("Bold Magenta","magenta",True) + " text")
    print("some " + colourise("Bold Cyan","cyan",True) + " text")
    print("some " + colourise("Bold White","white",True) + " text")

    # Bold Lighter Colours
    print("some " + colourise("Bold Light-Grey","grey",True) + " text")
    print("some " + colourise("Bold Light-Red","light-red",True) + " text")
    print("some " + colourise("Bold Light-Green","light-green",True) + " text")
    print("some " + colourise("Bold Light-Yellow","light-yellow",True) + " text")
    print("some " + colourise("Bold Light-Blue","light-blue",True) + " text")
    print("some " + colourise("Bold Light-Magenta","light-magenta",True) + " text")
    print("some " + colourise("Bold Light-Cyan","light-cyan",True) + " text")
    print("some " + colourise("Bold Light-White","light-white",True) + " text")

if __name__ == "__main__":
    main()