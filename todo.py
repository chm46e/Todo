#=============================================================================
# Imports
#=============================================================================

import os.path
import sys
import subprocess as sp
from colors import *


#=============================================================================
# Global variables
#=============================================================================

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


#=============================================================================
# Minifunctions
#=============================================================================

# Upgrade to the lasted from git to config folder 
def upgrade():
    os.system("rm ~/bin/todo")
    os.system("rm ~/.config/Wolfy-todo/todo.py")
    setup()

# Reads the group file and returns the lines
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

# Reads the note file and returns the lines
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

# Gets the output of a shell command
def output(cmd):
    return sp.getoutput(cmd)

# Runs a shell command
def run(cmd):
    return os.system(cmd)


#=============================================================================
# Main functions                                                            
#=============================================================================

# Setups the app to work out-of-the-box
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
        
    # Copyies the scripts to the config folder
    os.system("cp todo.py $HOME/.config/Wolfy-todo")
    os.system("cp colors.py $HOME/.config/Wolfy-todo")

    # Prints a neat message
    print(" ")
    print(cs.bold + cs.magenta + ":: All set!" + cs.quit + " \nEnjoy your note taking!")
    print("Type " + yellow("--help") + " for some tips!")
    print(blue("-"*54))
    print("")


# Lists all the notes
def list():
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

    # Goes through each line in the notefile
    counter = 0
    while counter != line_count:
        # Split's the line by the ; delimiter and put's them into variables
        lines = readnotefile()
        line = lines[counter].replace("\n", "")
        note, state, group = line.split(";")

        # Changes the color depending on the state
        if(state == "1"):
            color = cs.red
        elif(state == "2"):
            color = cs.yellow
        elif(state == "3"):
            color = cs.green
        elif(state == "black"):
            color = cs.black
        elif(state == "orange"):
            color = cs.orange
        elif(state == "blue"):
            color = cs.blue
        elif(state == "purple" or state == "magenta"):
            color = cs.magenta
        elif(state == "cyan"):
            color = cs.cyan
        elif(state == "pink"):
            color = cs.pink
        elif(state == "lcyan"):
            color = cs.pink

        # Creates the colored note
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

    # Build's the lines
    counter_alt = 0
    for a in ls_array:
        print(magenta(alphabet[counter_alt] + ")") + blue(a[0]) + ":")
        counter = 1
        for b in a[1]:
            print("      " + str(counter) + ". " + b)
            counter += 1
        counter_alt += 1

# Inserts a note to the end of a group
def insert():
    # Finds the group letter position from alphabet
    char_pos = alphabet.find(args[2])

    # Opens and reads the groups
    lines = readgroupfile()

    # Goes through the lines in the groupfile
    counter = 0
    for line in lines:
        # Checks if the group is correct
        if(counter == char_pos):
            group = line.replace("\n", "")

            # Appends the note to the end of the note file
            file = open(BASENOTES, "a")

            #Checks to see if there are more args and if so uses them
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

# Deletes a note
def delete():
    # Retrieves the group char and note number
    group_char = args[2][0]
    note_nr = args[2].replace(args[2][0], "")

    # Finds the group letter position from the alphabet
    char_pos = alphabet.find(group_char)

    # Opens and reads the groups
    group_lines = readgroupfile()

    # Translates the group_char to a group name
    group = group_lines[char_pos].replace("\n", "")

    # Opens and reads the notes
    note_lines = readnotefile()

    # Opens the note file in writing mode
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

# Edits a note's text
def edit():
    # Retrieves the group char and note number
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
                if(args_len >= 4):
                    counter_alt = 0
                    string = ""
                    while counter_alt != args_len - 2:
                        counter_alt+=1
                        string = string + args[counter_alt+2] + " "
                    file.write(string[:-1] + ";" + line_state + ";" + group + "\n")
                else:   
                    file.write(args[3] + ";1;" + group + "\n")
        else:
            file.write(line)
        line_counter += 1
    file.close()

# Makes a group
def makegroup():
    #Opens the groups file and appends the group to the end
    file = open(BASEGROUPS, "a")
    file.write(args[2] + "\n")
    file.close()

# Removes a group
def removegroup():
    #Checks if the group is used. If so exits.
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

    #Opens the groups file and rewrites the lines, without including the group
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

# Edits a note's group
def editgroup():
    #check if group exists and if not exits.
    exists = False
    lines = readgroupfile()
    for line in lines:
        if(line.replace("\n", "") == args[3]):
            exists = True

    if(exists == False):
        print(red("Error:"))
        print("Group does not exist.")
        sys.exit()

    # Retrieves the group char and the note number
    group_char = args[2][0]
    note_nr = args[2].replace(args[2][0], "")

    # Finds the group letter position from alphabet
    char_pos = alphabet.find(group_char)

    # Opens and reads the groups
    group_lines = readgroupfile()

    # Translates the group_char to a group name
    group = group_lines[char_pos].replace("\n", "")

    # Opens and reads the notes
    note_lines = readnotefile()

    # Opens the note file in writing mode
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

# Changes the state/color of a note
def changestate():
    color = "3" #Default color

    # Retrieves the group char and the note number
    group_char = args[2][0]
    note_nr = args[2].replace(args[2][0], "")

    # Finds the group letter position from alphabet
    char_pos = alphabet.find(group_char)

    # Opens and reads the groups
    group_lines = readgroupfile()

    # Translates the group_char to a group name
    group = group_lines[char_pos].replace("\n", "")

    # Opens and reads the notes
    note_lines = readnotefile()

    # Opens the note file in writing mode
    file = open(BASENOTES, "w")

    # Goes through the note file lines
    counter = 0
    line_counter = 0
    for line in note_lines:
        line_split = line.split(";")
        line_group = line_split[2].replace("\n", "")
        line_note = line_split[0]

        # Checks if group is correct
        if(line_group == group):
            counter += 1

            # Checks if count is correct
            if(note_nr == str(counter)):
                # Translates the name colors into integers
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

# Removes all done(green) notes
def removedone():
    # Reads the note file
    lines = readnotefile()

    # Open's the notes file in writing mode
    file = open(BASENOTES, "w")

    # Goes through the lines and rewrites them. Ignores the ones that have the third state.
    for line in lines:
        if(line.split(";")[1] != "3"):
            file.write(line)

    file.close()

# Prints the help function
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

# A function that builds the help arguments for each command
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


#=============================================================================
# Main
#=============================================================================

def main():
    helpin = False

    #Checks if no args were supplied
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
        try:
            if(args[2] == "-h" or args[2] == "--help"):
                helpin = True
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
        except:
            pass

        if(args_len < 3 and helpin == False):
            print(red("ERROR:"))
            print("Not enough arguments!")
            print("Use: todo insert -h for arguments")
            sys.exit()

        if(helpin == True):
            sys.exit()

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
        try:
            if(args[2] == "-h" or args[2] == "--help"):
                helpin = True
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
        except:
            pass

        if(args_len < 2 and helpin == False):
            print(red("ERROR:"))
            print("Not enough arguments!")
            print("Use: todo remove -h for arguments")
            sys.exit()

        if(helpin == True):
            sys.exit()

        delete()
        list()

    elif args[1] == "e" or args[1] == "edit":
        try:
            if(args[2] == "-h" or args[2] == "--help"):
                helpin = True
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
        except:
            pass

        if(args_len < 3 and helpin == False):
            print(red("ERROR:"))
            print("Not enough arguments!")
            print("Use: todo edit -h for arguments")
            sys.exit()

        if(helpin == True):
            sys.exit()

        edit()
        list()


    elif args[1] == "mg" or args[1] == "makegroup":
        try:
            if(args[2] == "-h" or args[2] == "--help"):
                helpin = True
                usage = [" todo makegroup <arg1>",
                         " todo mg <arg1>"
                ]
                arguments = ["  <arg1>    The group name"]
                examples = ["  todo makegroup School"]

                print(magenta(":: Makes a group"))
                print("")
                showargs(usage, arguments, examples)
        except:
            pass

        if(args_len < 2 and helpin == False):
            print(red("ERROR:"))
            print("Not enough arguments!")
            print("Use: todo makegroup -h for arguments")
            sys.exit()

        if(helpin == True):
            sys.exit()

        makegroup()
        list()

    elif args[1] == "rg" or args[1] == "removegroup":
        try:
            if(args[2] == "-h" or args[2] == "--help"):
                helpin = True
                usage = [" todo removegroup <arg1>",
                         " todo rg <arg1>"
                ]
                arguments = ["  <arg1>    The group name(Not the group char!)"]
                examples = ["  todo removegroup School"]

                print(magenta(":: Removes a group"))
                print("")
                showargs(usage, arguments, examples)
        except:
            pass

        if(args_len < 2 and helpin == False):
            print(red("ERROR:"))
            print("Not enough arguments!")
            print("Use: todo removegroup -h for arguments")
            sys.exit()

        if(helpin == True):
            sys.exit()

        removegroup()

    elif args[1] == "eg" or args[1] == "editgroup":
        try:
            if(args[2] == "-h" or args[2] == "--help"):
                helpin = True
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
        except:
            pass

        if(args_len < 3 and helpin == False):
            print(red("ERROR:"))
            print("Not enough arguments!")
            print("Use: todo editgroup -h for arguments")
            sys.exit()

        if(helpin == True):
            sys.exit()

        editgroup()
        list()

    elif args[1] == "s" or args[1] == "state":
        try:
            if(args[2] == "-h" or args[2] == "--help"):
                helpin = True
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
        except:
            pass

        if(args_len < 3 and helpin == False):
            print(red("ERROR:"))
            print("Not enough arguments!")
            print("Use: todo state -h for arguments")
            sys.exit()

        if(helpin == True):
            sys.exit()

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
            help()
        else:
            help()

    else:
        print("Command not found")


if __name__ == '__main__':
    main()
