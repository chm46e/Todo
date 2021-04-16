import os.path
import sys
import subprocess as sp
from colors import *

# Ideas;
#  remove all green state notes #Green notes are good for other who will work on the code later

# Global variables
args = sys.argv
args_len = len(args) - 1

noteFile = "notes"
groupFile = "groups"
launcher = "todo"
USERBIN: str = os.path.expanduser("~/bin")
LAUNCHER: str = os.path.join(USERBIN, launcher)
BASEFOLDER: str = os.path.expanduser("~/.config/Wolfy-todo/")
BASENOTES: str = os.path.join(BASEFOLDER, noteFile)
BASEGROUPS: str = os.path.join(BASEFOLDER, groupFile)
HOMEFOLDER: str = sp.getoutput("echo $HOME")

alphabet = "abcdefghijklmonpqrstuvwxyz"

# define the access rights
access_rights = 0o755

# Create target Directory and files if they don't exist
def setup():
    red_prompt = red(">>")
    green_prompt = green(">>")
    created = magenta(" created!")
    exists = green(" exists!")

    # Configuring todo app
    print("")
    print(blue("-"*54))
    print(cs.bold + magenta(":: TODO App initial configuration\n"))

    # Test if main folder exists and creates it
    if not os.path.exists(BASEFOLDER):
        os.makedirs(BASEFOLDER, access_rights)
        print(red_prompt, " Folder   ", BASEFOLDER.replace(HOMEFOLDER, "~"), " "*5, created)
    else:
        print(green_prompt," Folder   ", BASEFOLDER.replace(HOMEFOLDER, "~"), " "*6, exists)

    # Test if note file exist and create it
    if not os.path.isfile(BASENOTES):
        with open(BASENOTES, "w") as file:
            file.write("This is a 'not started' state note.;1;Notes\nThis is a 'started/doing' state note.;2;Notes\nThis is a 'Done' state note.;3;Notes\n")
        print(red_prompt," Groups   ", BASENOTES.replace(HOMEFOLDER, "~") + " ", created)
    else:
        print(green_prompt," Groups   ", BASENOTES.replace(HOMEFOLDER, "~") + " "*2, exists)

    # Test if group file exist and create it
    if not os.path.isfile(BASEGROUPS):
        with open(BASEGROUPS, "w") as file:
            file.write("Notes\n")
        print(red_prompt," Notes    ", BASEGROUPS.replace(HOMEFOLDER, "~"), created)
    else:
        print(green_prompt," Notes    ", BASEGROUPS.replace(HOMEFOLDER, "~") + " ", exists)

    # Adding launcher
    if not os.path.isfile(LAUNCHER):
        with open(LAUNCHER, "w") as file:
            file.write("#!/bin/sh \npython3 ~/.config/Wolfy-todo/todo.py $*")
        os.chmod(LAUNCHER, access_rights)
        print(red_prompt," Launcher ", LAUNCHER.replace(HOMEFOLDER, "~"), " "*16, created)
    else:
        print(green_prompt," Launcher ", LAUNCHER.replace(HOMEFOLDER, "~"), " "*17, exists)
        
    # Copy script to config folder
    os.system("cp todo.py $HOME/.config/Wolfy-todo")
    os.system("cp colors.py $HOME/.config/Wolfy-todo")

    print(" ")
    print(cs.bold + cs.magenta + ":: All set!" + cs.quit + " \nEnjoy your note taking!")
    print("Type " + yellow("--help") + " for some tips!")
    print(blue("-"*54))
    print("")

# Upgrade to the lasted from git to config folder 
def upgrade():
    os.system("rm ~/bin/todo")
    os.system("rm ~/.config/Wolfy-todo/todo.py")
    setup()

# Minifunctions
def readgroupfile():
    try:
        file = open(BASEGROUPS, "r")
    except:
        print(magenta("Groupfile") + " missing:")
        print(green("Running setup:"))
        setup()
        sys.exit()
    lines = file.readlines()
    file.close()
    return lines


def readnotefile():
    try:
        file = open(BASENOTES, "r")
    except:
        print(magenta("Notefile") + " missing:")
        print(red("Running setup:"))
        setup()
        sys.exit()
    lines = file.readlines()
    file.close()
    return lines

def output(cmd):
    return sp.getoutput(cmd)

def run(cmd):
    return os.system(cmd)


# Functions
def list():
    # todo l

    group_id = 0
    color = "red"  # The default color
    ls_array = []
    group_array = []

    # Add group names to ls_array and group array
    lines = readgroupfile()
    for line in lines:
        clean_line = line.replace("\n", "")
        ls_array.append([clean_line, []])
        group_array.append(clean_line)

    # Get's the note count
    line_count = len(readnotefile())

    counter = 0
    while counter != line_count:
        # Split's the line by the space delimiter and put's them into variables
        lines = readnotefile()
        line = lines[counter].replace("\n", "")
        note, state, group = line.split(";")

        # Change the color depending on the state
        if(state == "1"):
            color = cs.red
        elif(state == "2"):
            color = cs.yellow
        elif(state == "3"):
            color = cs.green

        # Create the colored note
        colored_note = color + note + cs.quit

        # Tries to find a group match(group array and line group)
        group_counter = 0
        for gr_group in group_array:
            if(gr_group == group):
                group_id = group_counter
                break
            group_counter += 1

        # Append's the note to the right group_array(dependent on the group_id)
        ls_array[group_id][1].append(colored_note)

        counter += 1

    # Print's/Build's the lines
    counter_alt = 0
    for a in ls_array:
        print(green(alphabet[counter_alt] + ")") + blue(a[0]) + ":")
        counter = 1
        for b in a[1]:
            print("      " + str(counter) + ". " + b)
            counter += 1
        counter_alt += 1


def insert():
    # todo i <group_char> <note>

    #Check's if the note contains a ;
    if(args[3].find(";") != -1):
        print(red("Error:"))
        print("Having a -> " + red(";") + " in your note is " + red("forbidden!"))
        sys.exit()

    # Find's the group letter position from alphabet
    char_pos = alphabet.find(args[2])

    # Open's and read's the groups
    lines = readgroupfile()

    counter = 0
    for line in lines:
        if(counter == char_pos):
            group = line.replace("\n", "")

            # Append's the note to the end of the note file
            file = open(BASENOTES, "a")
            file.write(args[3] + ";1;" + group + "\n")
            file.close()

            break
        counter += 1


def delete():
    # todo d <group_char + note_nr>

    group_char = args[2][0]
    note_nr = args[2].replace(args[2][0], "")

    # Find's the group letter position from alphabet
    char_pos = alphabet.find(group_char)

    # Open's and read's the groups
    group_lines = readgroupfile()

    # Translates the group_char to a group name
    group = group_lines[char_pos].replace("\n", "")

    # Open's and read's the notes
    note_lines = readnotefile()

    # Open the note file in writing mode
    file = open(BASENOTES, "w")

    counter = 0
    line_counter = 0
    for line in note_lines:
        line_group = line.split(";")[2].replace("\n", "")

        # Check's if group is correct
        if(line_group == group):
            counter += 1

            # Check's if count is not correct
            if(note_nr != str(counter)):
                file.write(line)
        else:
            file.write(line)
        line_counter += 1
    file.close()


def edit():
    # todo e <group_char + note_nr> <note> <group>

    group_char = args[2][0]
    note_nr = args[2].replace(args[2][0], "")

    # Find's the group letter position from alphabet
    char_pos = alphabet.find(group_char)

    # Open's and read's the groups
    group_lines = readgroupfile()

    # Translates the group_char to a group name
    group = group_lines[char_pos].replace("\n", "")

    # Open's and read's the notes
    note_lines = readnotefile()

    # Open the note file in writing mode
    file = open(BASENOTES, "w")

    counter = 0
    line_counter = 0
    for line in note_lines:
        line_split = line.split(";")
        line_group = line_split[2].replace("\n", "")
        line_state = line_split[1]

        # Check's if group is correct
        if(line_group == group):
            counter += 1

            # Check's if count is not correct
            if(note_nr != str(counter)):
                file.write(line)
            else:
                if(args_len == 4):
                    file.write(args[3] + ";" + line_state +
                               ";" + args[4] + "\n")
                else:
                    file.write(args[3] + ";" + line_state + ";" + group + "\n")
        else:
            file.write(line)
        line_counter += 1
    file.close()


def makegroup():
    file = open(BASEGROUPS, "a")
    file.write(args[2] + "\n")
    file.close()


def removegroup():
    group_exist = False
    lines = readnotefile()
    for line in lines:
        if(line.split(";")[2].replace("\n", "") == args[2]):
            group_exist = True
            break
    if(group_exist == True):
        print(red("Error:"))
        print("Cannot delete group:")
        print("Group " + magenta("not empty."))
        return 1

    with open(BASEGROUPS, "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        counter = 0
        for line in new_f:
            counter += 1
            if args[2] != line.replace("\n", ""):
                f.write(line)
        f.truncate()

    list()


def changestate():
    # todo s <group_char + note_nr> <state>

    color = "3" #Default color

    group_char = args[2][0]
    note_nr = args[2].replace(args[2][0], "")

    # Find's the group letter position from alphabet
    char_pos = alphabet.find(group_char)

    # Open's and read's the groups
    group_lines = readgroupfile()

    # Translates the group_char to a group name
    group = group_lines[char_pos].replace("\n", "")

    # Open's and read's the notes
    note_lines = readnotefile()

    # Open the note file in writing mode
    file = open(BASENOTES, "w")

    counter = 0
    line_counter = 0
    for line in note_lines:
        line_split = line.split(";")
        line_group = line_split[2].replace("\n", "")
        line_note = line_split[0]

        # Check's if group is correct
        if(line_group == group):
            counter += 1

            # Check's if count is correct
            if(note_nr == str(counter)):
                if(args[3] == "red"):
                    color = "1"
                elif(args[3] == "yellow"):
                    color = "2"
                elif(args[3] == "green"):
                    color = "3"
                else:
                    color = args[3]

                file.write(line_note + ";" + color + ";" + group + "\n")
            else:
                file.write(line)
        else:
            file.write(line)
        line_counter += 1
    file.close()


def removedone():
    # todo rd

    lines = readnotefile()

    file = open(BASENOTES, "w")

    for line in lines:
        if(line.split(";")[1] != "3"):
            file.write(line)

    file.close()

def help():
    green_prompt = green("  >>")
    grey_mod = lgrey("  --")

    print("")
    print(blue("-"*54))
    print(cs.bold + magenta(":: Simplistic todo terminal application created in Python3"))
    print(lcyan("States:"))
    print("  1.",red("Red entry"),red("    -> Not started"))
    print("  2.",yellow("Yellow entry"),yellow(" -> Doing"))
    print("  3.",green("Green entry"),green("  -> Done\n"))

    print("")
    print(lcyan("Usage") + ": todo <cmd> <arg1> ...")
    print(lcyan("Commands and args:"))
    print(green_prompt,"  l or list -> Print all the notes")
    print(grey_mod,"    No parameters")
    print("")
    print(green_prompt,"  i or insert -> Insert a note")
    print(grey_mod,"    <group_char> <note>")
    print("")
    print(green_prompt,"  r or remove -> Remove a note")
    print(grey_mod,"    <group_char><note_nr>")
    print("")
    print(green_prompt,"  e or edit -> Edit a note's text")
    print(grey_mod,"    <group_char><note_nr> <note>")
    print("")
    print(green_prompt,"  mg or makegroup -> Make a group")
    print(grey_mod,"    <group_name>")
    print("")
    print(green_prompt,"  rg or removegroup -> Remove a group")
    print(grey_mod,"    <group_name>")
    print("")
    print(green_prompt,"  s or state -> Change the state of a note")
    print(grey_mod,"    <group_char><note_nr> <state>")
    print("")
    print(green_prompt,"  rd or removedone -> Remove all done(green state) notes")
    print(grey_mod,"    No parameters")
    print("")
    print("Examples:")
    print("Inserting a note 'Homework!' into the first group(School group):")
    print(green_prompt,"  todo i a Homework!")
    print("")
    print("Removing the eleventh note from the second group:")
    print(green_prompt,"  todo r b11")
    print("")
    print("List all the notes:")
    print(green_prompt,"  todo")
    print("")
    print("Edit the first note from second group to show 'Hello!':")
    print(green_prompt,"  todo e b1 Hello!")
    print("")
    print("Change the state of first group, third note to done(green):")
    print(green_prompt,"  todo s a3 3")
    print("")
    print("Made by: Mr.Wolfy and Tux-Code")
    print("")

def main():

    if args_len == 0:
        list()

    elif args[1] == "setup":
        # todo setup
        setup()
    
    elif args[1] == "upgrade":
        # todo setup
        upgrade()

    elif args[1] == "i" or args[1] == "insert":
        # todo i <note> <group>
        insert()
        list()

    elif args[1] == "l" or args[1] == "list":
        # todo l
        list()

    elif args[1] == "d" or args[1] == "delete" or args[1] == "r" or args[1] == "remove":
        # todo d <group> <note_nr>
        delete()
        list()

    elif args[1] == "e" or args[1] == "edit":
        edit()
        list()

    elif args[1] == "mg" or args[1] == "makegroup":
        makegroup()
        list()

    elif args[1] == "rg" or args[1] == "removegroup":
        removegroup()

    elif args[1] == "s" or args[1] == "state":
        changestate()
        list()

    elif args[1] == "rd" or args[1] == "removedone":
        removedone()
        list()

    elif args[1] == "quit":
        # todo setup
        sys.exit()

    elif args[1] == "-h" or args[1] == "--help" or args[1] == "h" or args[1] == "help":
        # show help
        help()

    else:
        print("Command not found")


if __name__ == '__main__':
    main()
