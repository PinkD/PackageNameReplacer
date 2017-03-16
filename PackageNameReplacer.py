import os

import re


class PackageNameReplacer:
    def __init__(self, src_pkg_name, dst_pkg_name, project_dir=".", debug=False):
        self.src_parts = src_pkg_name.split(".")
        self.dst_parts = dst_pkg_name.split(".")
        self.src_pkg_name = src_pkg_name
        self.src_dir_name = src_pkg_name.replace(".", "\\")
        self.dst_pkg_name = dst_pkg_name
        self.dst_dir_name = dst_pkg_name.replace(".", "\\")
        self.project_dir = project_dir
        self.debug = debug

    def process(self):
        for abs_dir, child_dirs, files in os.walk(self.project_dir):
            # self.__process_files(abs_dir, files)
            self.__process_dir(abs_dir, child_dirs)

    def __process_dir(self, abs_dir, child_dirs):
        for _dir in child_dirs:
            if (abs_dir + "\\" + _dir).endswith(self.src_dir_name):
                print(abs_dir + "\\" + _dir)
                os.chdir(abs_dir)
                if self.debug:
                    print("cd", abs_dir)
                while self.src_parts.__len__() > 0:
                    src_part = self.src_parts.pop()
                    dst_part = self.dst_parts.pop()
                    os.rename(src_part, dst_part)
                    os.chdir("..")
                    if self.debug:
                        print('rename/mv', src_part, dst_part)
                        print("cd ..")

    def __process_files(self, path, files):
        for file in files:
            self.__process_file(path + "\\" + file)

    def __process_file(self, file):
        if self.debug:
            print("reading -->  " + file)
        try:
            with open(file, mode='r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if re.findall(self.src_pkg_name.replace(".", "\.") + "[^\\w]", line).__len__() > 0:
                        print(file)
                        lines.__setitem__(lines.index(line), line.replace(self.src_pkg_name, self.dst_pkg_name))
                        print(line)
                        with open(file, mode='w', encoding='utf-8') as f:
                            f.writelines(lines)

        except UnicodeDecodeError as e:
            if self.debug:
                print(e)
                print("----------> may be bin file")
            pass
        pass

    pass
