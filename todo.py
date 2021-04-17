import os.path
import sys
import subprocess as sp
from colors import *

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

    if(args_len >= 3):
        if(args[3].find(";") != -1):
            print(red("Error:"))
            print("Having a -> " + red(";") + " in your note is " + red("forbidden!"))
            sys.exit()
    else:
        print(red("Error:"))
        print("Not enough arguments supplied.")
        print("Use 'todo insert -h' for help.")
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
            if(args_len >= 4):
                counter_alt = 0
                string = ""
                while counter_alt != args_len - 2:
                    counter_alt+=1

                    string = string + args[counter_alt+2] + " "
                file.write(string[:-1] + ";1;" + group + "\n")
            else:
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

def editgroup():
    #check if group exists
    exists = False
    lines = readgroupfile()
    for line in lines:
        if(line.replace("\n", "") == args[3]):
            exists = True

    if(exists == False):
        print(red("Error:"))
        print("Group does not exist.")
        sys.exit()

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
        line_note = line_split[0]

        # Check's if group is correct
        if(line_group == group):
            counter += 1

            # Check's if count is not correct
            if(note_nr != str(counter)):
                file.write(line)
            else:
                file.write(line_note + ";" + line_state + ";" + args[3] + "\n")
        else:
            file.write(line)
        line_counter += 1
    file.close()


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

    #print("")
    #print(blue("-"*54))
    print(cs.bold + magenta(":: Simplistic todo terminal application created in Python3"))
    print("")
    print(lcyan("USAGE:") + " " + yellow("todo") + " <cmd> " + "<arg1> <arg2> ...")
    print("")
    print(lcyan("CORE COMMANDS:"))
    print(green_prompt + "  list:" + "        Lists all the notes")
    print(green_prompt + "  insert:" + "      Inserts a note")
    print(green_prompt + "  remove:" + "      Removes a note")
    print(green_prompt + "  edit:" + "        Edits a note's text")
    print(green_prompt + "  makegroup:" + "   Makes a group")
    print(green_prompt + "  removegroup:" + " Removes a group")
    print(green_prompt + "  editgroup:" + "   Edits a note's group")
    print(green_prompt + "  state:" + "       Changes the state of a note")
    print(green_prompt + "  removedone:" + "  Removes all " + green("done") + " notes")
    print("")
    print(lcyan("ADDITIONAL COMMANDS:"))
    print(green_prompt + "  setup:       Runs the todo application setup")
    print(green_prompt + "  upgrade:     Upgrades to the last version")
    print(green_prompt + "  help:        Displays the help message")
    print("")
    print(lcyan("FLAGS:"))
    print(green_prompt + "  -h:          Displays the help message")
    print(green_prompt + "  --help:      Displays the help message")
    print("")
    print(lcyan("EXAMPLES:"))
    print(green_prompt + "  todo i a Homework!")
    print(green_prompt + "  todo r b11")
    print(green_prompt + "  todo e b1 Hello!")
    print(green_prompt + "  todo s a3 3")
    print("")
    print(lcyan("LEARN MORE:"))
    print(blue("  States:"))
    print("    1.",red("Red entry") + "     -> " + red("Not started"))
    print("    2.",yellow("Yellow entry") + "  -> " + yellow("Doing"))
    print("    3.",green("Green entry") + "   -> " + green("Done"))
    print("")
    print(blue("  Use:") + green(" '") + yellow("todo") + " <cmd> " + "-h" + green("'") + " for " + cs.bold + magenta("<args>"))
    print("")
    print(blue("  GitHub:") + yellow(" https://github.com/x3F-x3F/Todo "))
    print("    Feel free to open an issue!")

def showargs(usage_array, args_array, ex_array):
    green_prompt = green("  >>")

    counter = 0
    while counter != len(usage_array):
        print(lcyan("USAGE:") +  usage_array[counter])
        counter+=1
    print("")

    print(lcyan("ARGUMENTS:"))
    counter = 0
    while counter != len(args_array):
        print(green_prompt + args_array[counter])
        counter+=1
    print("")

    print(lcyan("EXAMPLES:"))
    counter = 0
    while counter != len(ex_array):
        print(green_prompt + ex_array[counter])
        counter+=1
    sys.exit()


def main():

    if args_len == 0:
        help()

    elif args[1] == "setup":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                print("No help for setup defined.")
            else:
                setup()
        else:
            setup()
    
    elif args[1] == "upgrade":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                print("No help for upgrade defined.")
            else:
                upgrade()
        else:
            upgrade()

    elif args[1] == "i" or args[1] == "insert":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo insert <arg1> <arg2>", 
                         " todo i <arg1> <arg2>"
                        ]
                arguments = ["  <arg1>    The group character(a-z)",
                             "  <arg2>    The note('Homework!')"
                            ]
                examples = ["  todo i a \"Help me!\"", 
                            "  todo i c Work"
                           ]

                print(magenta(":: Inserts a note"))
                print("")
                showargs(usage, arguments, examples)
            insert()
            list()
        else:
            insert()
            list()

    elif args[1] == "l" or args[1] == "list":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo list",
                         " todo l",
                ]
                arguments = ["  No arguments"]
                examples = ["  todo list"]

                print(magenta(":: Lists all the notes"))
                print("")
                showargs(usage, arguments, examples)
            # todo l
            list()
        else:
            list()

    elif args[1] == "d" or args[1] == "delete" or args[1] == "r" or args[1] == "remove":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo remove <arg1>",
                         " todo r <arg1>",
                         " todo delete <arg1>",
                         " todo d <arg1>"
                ]
                arguments = ["  <arg1>    The group char and note id combined(b3, a11)"]
                examples = ["  todo remove a7",
                            "  todo d c5"
                ]

                print(magenta(":: Removes a note"))
                print("")
                showargs(usage, arguments, examples)
            # todo d <group> <note_nr>
            delete()
            list()
        else:
            delete()
            list()

    elif args[1] == "e" or args[1] == "edit":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo edit <arg1> <arg2>",
                         " todo e <arg1> <arg2>"
                ]
                arguments = ["  <arg1>    The group char and note id combined(b3, a7)",
                             "  <arg2>    The new note"
                ]
                examples = ["  todo edit a3 Homework",
                            "  todo e b5 Chicken"]

                print(magenta(":: Edits a note's text"))
                print("")
                showargs(usage, arguments, examples)
            edit()
            list()
        else:
            edit()
            list()

    elif args[1] == "mg" or args[1] == "makegroup":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo makegroup <arg1>",
                         " todo mg <arg1>"
                ]
                arguments = ["  <arg1>    The group name"]
                examples = ["  todo makegroup School"]

                print(magenta(":: Makes a group"))
                print("")
                showargs(usage, arguments, examples)
            makegroup()
            list()
        else:
            makegroup()
            list()

    elif args[1] == "rg" or args[1] == "removegroup":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo removegroup <arg1>",
                         " todo rg <arg1>"
                ]
                arguments = ["  <arg1>    The group name(Not the group char!)"]
                examples = ["  todo removegroup School"]

                print(magenta(":: Removes a group"))
                print("")
                showargs(usage, arguments, examples)
            removegroup()
        else:
            removegroup()

    elif args[1] == "eg" or args[1] == "editgroup":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo editgroup <arg1> <arg2>", 
                         " todo eg <arg1> <arg2>"
                ]
                arguments = ["  <arg1>    The group char and note id combined(b3, a7)",
                             "  <arg2>    The group name(Not the group char!)"
                ]
                examples = ["  todo editgroup b4 School",
                            "  todo eg a7 Work"
                ]

                print(magenta(":: Edits a note's group"))
                print("")
                showargs(usage, arguments, examples)
            editgroup()
        else:
            editgroup()

    elif args[1] == "s" or args[1] == "state":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo state <arg1> <arg2>",
                         " todo s <arg1> <arg2>"
                ]
                arguments = ["  <arg1>    The group char and note id combined(b2, a6)",
                             "  <arg2>    The state(red(1), yellow(2), green(3)"
                ]
                examples = ["  todo s b2 green",
                            "  todo state a5 2"
                ]

                print(magenta(":: Changes the state of a note"))
                print("")
                showargs(usage, arguments, examples)
            changestate()
            list()
        else:
            changestate()
            list()

    elif args[1] == "rd" or args[1] == "removedone":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo removedone", " todo rd"]
                arguments = ["  No arguments"]
                examples = ["  todo rd"]

                print(magenta(":: Removes all done notes"))
                print("")
                showargs(usage, arguments, examples)
            removedone()
            list()
        else:
            removedone()
            list()

    elif args[1] == "quit":
        # todo setup
        sys.exit()

    elif args[1] == "-h" or args[1] == "--help" or args[1] == "h" or args[1] == "help":
        if(args_len >= 2):
            if(args[2] == "-h" or args[2] == "--help"):
                usage = [" todo help", " todo h", " todo -h", " todo --help"]
                arguments = ["  No arguments"]
                examples = ["  todo -h"]

                print(magenta(":: Displays the help message"))
                print("")
                showargs(usage, arguments, examples)
            # show help
            help()
        else:
            help()

    else:
        print("Command not found")


if __name__ == '__main__':
    main()
