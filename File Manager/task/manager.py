import os
import math
import shutil
from pathlib import Path

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    # s = round(size_bytes / p, 2)
    s = int(size_bytes / p)
    return f"{s}{size_names[i]}"


def mv_action(command):
    if command == "mv":
        print("Specify the current name of the file or directory and the new location and/or name")
        return

    if command.startswith("mv "):
        parts = command.split()

        if len(parts) == 3:
            source = parts[1]
            dest_name = parts[2]

            if source.startswith("."):
                list_files = os.listdir(os.getcwd())
                files_to_move = []
                for file in list_files:
                    if file.endswith(source):
                        files_to_move.append(file)
                if len(files_to_move) == 0:
                    print(f'File extension {source} not found in this directory')
                    return
                else:
                    for file in files_to_move:
                        dir_path = Path(dest_name)
                        file_path = dir_path / file

                        if os.path.isdir(dest_name):
                            shutil.move(file, dest_name)
                            continue

                        while file_path.is_file():
                            print(f'{file} already exists in this directory. Replace? (y/n)')
                            answer = input()
                            print(answer)
                            if answer == "y":
                                file_path.replace(file_path)
                                break
                            elif answer == "n":
                                break


            elif os.path.isdir(dest_name):
                shutil.move(source, dest_name)

            elif os.path.isfile(source) or os.path.isdir(source):
                if os.path.isdir(dest_name) or os.path.isfile(dest_name):
                    print("The file or directory already exists")
                else:
                    try:
                        os.rename(source, dest_name)
                    except OSError:
                        print("The file or directory already exists")
            else:
                print("No such file or directory")
        else:
            print("Specify the current name of the file or directory and the new location and/or name")


def rm_action(command):
    if command == "rm":
        print("Specify the file or directory")
        return
    if command.startswith("rm "):
        args = command.split(" ", 2)[1]
        # why is the "and" passing but not "or" needs to be researched
        if os.path.isfile(args) and os.path.isdir(args):
            os.remove(args)
        elif args.startswith("."):
            extension = args
            list_files = os.listdir(os.getcwd())
            files_to_remove = []
            for file in list_files:
                if extension in file:
                    files_to_remove.append(file)
            if len(files_to_remove) == 0:
                print(f"File extension {extension} not found in this directory")
                return
            else:
                for file in files_to_remove:
                    os.remove(file)
        else:
            print("No such file or directory")


def cd_action(command):
    if command == "cd ..":
        os.chdir(os.path.dirname(os.getcwd()))
        print(os.path.basename(os.getcwd()))

    elif command.startswith("cd "):
        path = command.split(" ", 1)[1]
        try:
            os.chdir(path)
            print(os.path.basename(os.getcwd()))
        except OSError:
            print("Invalid command")


def ls_action(command):
    if command.endswith("-l"):
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_dir():
                    print(entry.name)
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.name, os.stat(entry).st_size)
    elif command.endswith(" -lh"):
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_dir():
                    print(entry.name)
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.name, convert_size(os.stat(entry).st_size))
    elif command == "ls":
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_dir():
                    print(entry.name)
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.name)


def mkdir_action(command):
    parts = command.split()
    if len(parts) == 2:
        new_directory = parts[1]
        if not os.path.isdir(new_directory):
            os.mkdir(new_directory)
        else:
            print("The directory already exists")
    else:
        print("Specify the name of the directory to be made")


def cp_action(command):
    parts = command.split()
    if len(parts) == 1:
        print("Specify the file")
    elif len(parts) > 3:
        print("Specify the current name of the file or directory and the new location and/or name")
    elif len(parts) == 3:
        source = parts[1]
        destination = parts[2]

        if os.path.isdir(destination) and os.path.isfile(source):
            destination = os.path.join(destination, os.path.basename(source))
            try:
                shutil.copyfile(source, destination)
            except shutil.SameFileError:
                print(f"{os.path.basename(source)} already exists in this directory")
                # print(f"1: Copied {source} to {destination}")
        elif source.startswith("."):
            list_files = os.listdir(os.getcwd())
            files_to_copy = []
            for file in list_files:
                if file.endswith(source):
                    files_to_copy.append(file)
            if len(files_to_copy) == 0:
                print(f"File extension {source} not found in this directory")
                return
            else:
                if os.path.isdir(destination):
                    destination = os.path.join(destination)
                    for file in files_to_copy:
                        dir_path = Path(destination)
                        file_path = dir_path / file
                        try:
                            shutil.copy(file, destination)
                        except shutil.SameFileError:
                            while True:
                                print(f"{file} already exists in this directory. Replace? (y/n)")
                                answer = input()
                                if answer == 'y':
                                    src = Path(source).resolve()
                                    dst = Path(destination).resolve()
                                    src.replace(dst)
                                    break
                                elif answer == "n":
                                    break

        elif not os.path.exists(source):
            print("No such file or directory")


def main():
    print("Input the command")

    while True:
        command = input()
        if command == "quit":
            exit()
        elif command == "pwd":
            print(os.getcwd())
        elif command.startswith("cd"):
            cd_action(command)
        elif command.startswith("rm"):
            rm_action(command)
        elif command.startswith("mv"):
            mv_action(command)
        elif command.startswith("ls"):
            ls_action(command)
        elif command.startswith("mkdir"):
            mkdir_action(command)
        elif command.startswith("cp"):
            cp_action(command)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
