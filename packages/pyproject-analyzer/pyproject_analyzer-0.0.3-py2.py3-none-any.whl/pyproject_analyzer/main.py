"""
"""
# Native import
import os
import re
import time
import argparse

# Local import
import pyproject_analyzer.formaters as formaters

# Improvement ideas: compute all relative_path, identified public/not_recommended_access/private
# Factorize REGEX detection
# if docstring not alimented, having option to create it from model (default description)
# Detect line which start with code:   ^(([a-z]|[A-Z]){1,}.*?)$

__version__ = "0.0.3"


class PyProjectAnalyzer(object):
    """
    """

    dict_formaters = {"JSON": formaters.JSON}

    def __init__(self, project_path, formater="JSON", output_file=None, req_file=None,
                 stats_only=False):
        """
        """
        self.project_path = os.path.normpath(project_path)
        self.formater = formater
        self.output_file = output_file
        self.req_file = req_file
        self.stats_only = stats_only

        self.dict_project_analyze = dict()
        self.dict_project_analyze["PROJECT"] = dict()
        self.dict_project_analyze["PROJECT"]["STATS"] = dict()
        self.dict_project_analyze["PKGS"] = dict()
        self.dict_project_analyze["MODULES"] = dict()

        self.list_folders = list()
        self.list_files = list()
        self.list_imports = list()
        self.analyze_duration = 0
        self.dict_project_formated = None
        self.found_starting_lines = list()

        self.dict_project_analyze["PROJECT"]["ABS_PATH"] = self.project_path
        self.dict_project_analyze["PROJECT"]["REQ_LIST"] = list()
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS_PEP420"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_MODULES"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_FUNCTIONS"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_CLASSES"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_METHODS"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_IMPORTS"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_REQS"] = 0

    def launch_and_report_analyze(self):
        """
        Launch complete analyze then export it on terminal, or in files
        """
        self.launch_analyze()
        self.__print_result()

    def launch_analyze(self):
        """
        Allows to chain the different step in the right order to complete project analyze
        """
        if self.project_path:
            start = time.time()

            self.__get_content_list()
            self.__get_py_modules_list()
            self.__get_py_packages_list()
            self.__get_py_modules_content()
            self.__generate_req_file()

            stop = time.time()
            self.analyze_duration = stop - start

            if self.formater:
                try:
                    formater_choice_obj = PyProjectAnalyzer.dict_formaters[self.formater]()
                    self.dict_project_formated = formater_choice_obj.format_dict(
                        self.dict_project_analyze)
                except Exception:
                    raise AttributeError("The given value for report output file is not valid. "
                                         "Please check it.")
            else:
                self.dict_project_formated = self.dict_project_analyze

            if isinstance(self.output_file, str):
                try:
                    with open(self.output_file, "w") as output_file:
                        output_file.write(self.dict_project_formated)
                except Exception:
                    raise AttributeError("The given value for report output file is not valid. "
                                         "Please check it.")

            if isinstance(self.req_file, str):
                try:
                    with open(self.output_file, "w") as output_file:
                        for element in self.list_imports:
                            output_file.write(element)
                except Exception:
                    raise AttributeError("The given value for requirement file is not valid. "
                                         "Please check it.")
        else:
            raise AttributeError("The given value for project path to analyze is not valid. "
                                 "Please check it.")

    def __generate_req_file(self):
        req_list = list()
        for key in self.dict_project_analyze["MODULES"].keys():
            req_list.extend(self.dict_project_analyze["MODULES"][key]["IMPORTS"])

        req_list = sorted(list(set(req_list)))

        self.dict_project_analyze["PROJECT"]["REQ_LIST"] = req_list
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_REQS"] = len(req_list)

    def __print_result(self):
        """
        Simply export analyze in terminal or in files
        """
        if self.project_path:
            if self.stats_only:
                print("\n****************** STATS ******************")
                print("Project analyzed in {} seconds".format(self.analyze_duration))
                print("number of pkg non PEP420: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS"]))
                print("number of pkg PEP420: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS_PEP420"]))
                print("number of modules: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_MODULES"]))
                print("number of functions: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_FUNCTIONS"]))
                print("number of classes: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_CLASSES"]))
                print("number of methods: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_METHODS"]))
                print("number of imports: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_IMPORTS"]))
                print("number of requirements: {}".format(
                    self.dict_project_analyze["PROJECT"]["STATS"]["NB_REQS"]))
            else:
                print(self.dict_project_formated)

    def __get_content_list(self):
        """
        Allows to list all folders, subfolders and files identified in given path
        """
        for folder, subfolders, filenames in os.walk(self.project_path):
            if not folder.endswith("__pycache__"):
                self.list_folders.append(folder)
                for filename in filenames:
                    self.list_files.append(os.path.join(folder, filename))

    def __get_py_modules_list(self):
        """
        Allows to identify python modules (.py extension only) and start
        to supply project dictionary
        """
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_MODULES"] = 0

        pythonfile_list = [filename for filename in self.list_files if
                           filename.split(".")[-1].lower() == "py"]
        for filepath in pythonfile_list:
            relpath = os.path.relpath(filepath, self.project_path)
            self.dict_project_analyze["MODULES"][relpath] = dict()
            self.dict_project_analyze["MODULES"][relpath]["ABS_PATH"] = filepath
            self.dict_project_analyze["MODULES"][relpath]["NAME"] = os.path.splitext(
                os.path.basename(filepath))[0]
            self.dict_project_analyze["MODULES"][relpath]["FUNCTIONS"] = dict()
            self.dict_project_analyze["MODULES"][relpath]["CLASSES"] = dict()
            self.dict_project_analyze["MODULES"][relpath]["IMPORTS"] = dict()

            value = self.dict_project_analyze["PROJECT"]["STATS"]["NB_MODULES"]
            self.dict_project_analyze["PROJECT"]["STATS"]["NB_MODULES"] = value + 1

    def __get_py_packages_list(self):
        """
        Allows to list package in given path.
        Supply two different dictionnaries: one with __init__ file,
        one without __init__ file (PEP420 compliance)
        """
        modules_list = [self.dict_project_analyze["MODULES"][module]["ABS_PATH"] for module in
                        self.dict_project_analyze["MODULES"].keys()]
        packages_list = set([os.path.abspath(os.path.dirname(filename)) for
                             filename in modules_list])
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS_PEP420"] = 0

        for pkg_path in packages_list:
            # Why RELPATH as key?
            # Because we can have several pkg/module/classes/methods/functions with same name
            # inside a project
            relpath = os.path.relpath(pkg_path, self.project_path)

            if os.path.join(pkg_path, "__init__.py") in modules_list:
                pep_420 = False
                value = self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS"]
                self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS"] = value + 1
            else:
                pep_420 = True
                value = self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS_PEP420"]
                self.dict_project_analyze["PROJECT"]["STATS"]["NB_PKGS_PEP420"] = value + 1

            self.dict_project_analyze["PKGS"][relpath] = dict()
            self.dict_project_analyze["PKGS"][relpath]["NAME"] = dict()
            self.dict_project_analyze["PKGS"][relpath]["ABS_PATH"] = pkg_path
            self.dict_project_analyze["PKGS"][relpath]["SUB_PKGS"] = dict()
            self.dict_project_analyze["PKGS"][relpath]["MODULES"] = dict()
            self.dict_project_analyze["PKGS"][relpath]["PEP_420"] = pep_420

    def __get_py_modules_content(self):
        """
        Allows to analyze the content of each identified Python module and extract
        functions, classes, methods and imports
        """
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_FUNCTIONS"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_CLASSES"] = 0
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_METHODS"] = 0

        modules_list = [self.dict_project_analyze["MODULES"][module]["ABS_PATH"] for module in
                        self.dict_project_analyze["MODULES"].keys()]

        for filepath in modules_list:
            # todo add security on file size
            relpath = os.path.relpath(filepath, self.project_path)
            with open(filepath, "r") as filename:
                file_content = filename.read()

            # First, we identify the lines which start at 0 index
            found_starting_lines = self.__identify_starting_lines(file_content)

            # We search for functions only. We get only the line with def
            self.__supply_functions(relpath, file_content, found_starting_lines)

            # We search for class only. We get only the line with class then we supply methods
            self.__supply_classes(relpath, file_content, found_starting_lines)

            # We search for methods class only.
            self.__supply_methods(relpath, file_content, found_starting_lines)

            # We search for imports to list the libs name
            self.__supply_imports(relpath, file_content, found_starting_lines)

    def __identify_starting_lines(self, file_content):
        """
        Identify all lines in file, starting by a letter (so code without indent)
        """
        found_start_docstrings = re.findall(r"^(\"\"\"[\S\s]*?\"\"\")", file_content, re.MULTILINE)

        file_content_copy = file_content

        for docstr in found_start_docstrings:
            file_content_copy = file_content_copy.replace(docstr, "")

        found_start_lines = re.findall(r"(^(([a-z]|[A-Z]|[_]){1,}.*?)$)", file_content_copy,
                                          re.MULTILINE)
        found_start_lines = [elmt[0] for elmt in found_start_lines]
        found_starting_lines = [(elmt, file_content.find(elmt)) for elmt in found_start_lines]

        return found_starting_lines

    def __supply_functions(self, relpath, file_content, found_starting_lines):
        """
        Private function to identify the functions in a given module
        """
        # We search for functions only
        # First we get only the line with def
        found_refs_list = re.findall(r"(^(def )(.+?)\((.*?)\):$)", file_content, re.MULTILINE)
        fct_to_search = [elmt[0] for elmt in found_refs_list]
        tmp_list = [element[0] for element in found_refs_list]
        # Then we delete the "def " start line
        tmp_list = [tmp.split("def ")[1] for tmp in tmp_list]
        functions_names_list = [tmp.split("(")[0] for tmp in tmp_list]
        functions_arguments_list = [tmp.split("(")[1].replace("):", "") for tmp in tmp_list]

        for idx, function_name in enumerate(functions_names_list):
            value = self.dict_project_analyze["PROJECT"]["STATS"]["NB_FUNCTIONS"]
            self.dict_project_analyze["PROJECT"]["STATS"]["NB_FUNCTIONS"] = value + 1

            self.dict_project_analyze["MODULES"][relpath]["FUNCTIONS"][function_name] = dict()
            self.dict_project_analyze["MODULES"][relpath]["FUNCTIONS"][function_name]["ARGS"] = \
                functions_arguments_list[idx]

    def __supply_classes(self, relpath, file_content, found_starting_lines):
        """
        Private function to identify the classes in a given module
        """
        found_refs_list = re.findall(r"(^((class ){1}(.){1,}(\):){1})$)", file_content,
                                     re.MULTILINE)
        class_to_search = [elmt[0] for elmt in found_refs_list]
        tmp_list = [element[0] for element in found_refs_list]
        tmp_list = [tmp.split("class ")[1] for tmp in tmp_list]
        classes_names_list = [tmp.split("(")[0] for tmp in tmp_list]
        # inherit_list = [tmp.split("(")[1].replace("):", "") for tmp in tmp_list]

        for idx, class_name in enumerate(classes_names_list):
            value = self.dict_project_analyze["PROJECT"]["STATS"]["NB_CLASSES"]
            self.dict_project_analyze["PROJECT"]["STATS"]["NB_CLASSES"] = value + 1

            self.dict_project_analyze["MODULES"][relpath]["CLASSES"][class_name] = dict()
            self.dict_project_analyze["MODULES"][relpath]["CLASSES"][class_name]["INHERIT"] = list()
            self.dict_project_analyze["MODULES"][relpath]["CLASSES"][class_name]["ARGS"] = dict()
            self.dict_project_analyze["MODULES"][relpath]["CLASSES"][class_name]["METHODS"] = dict()

    def __supply_methods(self, relpath, file_content, found_starting_lines):
        """
        Private function to identify the classes's methods in a given module
        """
        classes_list = list(self.dict_project_analyze["MODULES"][relpath]["CLASSES"].keys())
        idx_list = [element[1] for element in found_starting_lines]

        for class_name in classes_list:
            class_prototype = "class {}".format(class_name)
            class_idx = file_content.find(class_prototype)
            if class_idx != idx_list[-1]:
                idx_sup = [element for element in idx_list if element > class_idx][0]
            else:
                idx_sup = len(file_content)
            file_extract = file_content[class_idx:idx_sup + 1]

            found_def_list = re.findall(r"(^([ ]{4}|[\t]{1})(def ){1}.*(:){1}$)", file_extract,
                                        re.MULTILINE)
            tmp_list = [element[0] for element in found_def_list]
            tmp_list = [tmp.split("def ")[1] for tmp in tmp_list]
            methods_names_list = [tmp.split("(")[0] for tmp in tmp_list]
            methods_arguments_list = [tmp.split("(")[1].replace("):", "") for tmp in tmp_list]

            dict_tmp_method = \
                self.dict_project_analyze["MODULES"][relpath]["CLASSES"][class_name]["METHODS"]
            for method_idx, method_name in enumerate(methods_names_list):
                value = self.dict_project_analyze["PROJECT"]["STATS"]["NB_METHODS"]
                self.dict_project_analyze["PROJECT"]["STATS"]["NB_METHODS"] = value + 1

                dict_tmp_method[method_name] = dict()
                dict_tmp_method[method_name]["ARGS"] = methods_arguments_list

    def __supply_imports(self, relpath, file_content, found_starting_lines):
        """
        Private function to identify the imports in a given module
        """
        list_import = list()

        # Found all docstrings & replace them by ""
        found_start_docstrings = re.findall(r"(\"\"\"[\S\s]*?\"\"\")", file_content, re.MULTILINE)

        file_content_copy = file_content

        for docstr in found_start_docstrings:
            file_content_copy = file_content_copy.replace(docstr, "")

        # Found all single comments & replace them by ""
        found_single_comments = re.findall(r"((#){1,}(.)*)", file_content_copy, re.MULTILINE)
        found_single_comments = [elmt[0] for elmt in found_single_comments]

        for comment in found_single_comments:
            file_content_copy = file_content_copy.replace(comment, "")

        # detect all import from...import... type
        # TODO REGEX to review
        found_from_imports = re.findall(r"^(([ ]{4}|[\t])*(from ){1}(.){1,}( ){1}(import){1}(.){1,})",
                                        file_content_copy, re.MULTILINE)
        found_from_imports = [elmt[0] for elmt in found_from_imports]

        for idx, from_import in enumerate(found_from_imports):
            tmp = from_import.split("import")[0]
            tmp = tmp.replace("from ", "")
            tmp = tmp.split(".")[0]
            found_from_imports[idx] = tmp.strip()

        found_from_imports = list(set(found_from_imports))

        list_import.extend(found_from_imports)

        # detect all import... type
        # line starts with import and ends with letter or number => one line without alias
        # only one import per line
        found_imports = re.findall(r"^(([ ]{4}|[\t])*(import ){1}([a-z]|[A-Z]|_|-|\.)*?)$",
                                        file_content_copy, re.MULTILINE)
        found_imports = [elmt for elmt in found_from_imports]

        # only one import per line with alias
        tmp_imports = re.findall(r"^(([ ]{4}|[\t])*(import ){1}(([a-z]|[A-Z]|[0-9]_|-|\.)*?" +
                                 r"( as ){1}([a-z]|[A-Z]|[0-9]|_|-|\.){1,}){1})$",
                                 file_content_copy, re.MULTILINE)
        tmp_imports = [elmt[0] for elmt in tmp_imports]
        for idx, importlib in enumerate(tmp_imports):
            tmp = importlib.split("as")[0]
            tmp = tmp.replace("import ", "")
            tmp = tmp.split(".")[0]
            tmp_imports[idx] = tmp.strip()

        tmp_imports = list(set(tmp_imports))
        found_imports.extend(tmp_imports)

        # several imports per line
        # TODO Regex to use for several lines import: ^(([ ]{4}|[\t])*(import ){1}(.*(\\){1}(\s)*){1,}.*)$
        # TODO Regex to use for mono lines import: ^(([ ]{4}|[\t])*(import ){1}.*[^\\])$
        # found_imports = re.findall(r"^(([ ]{4}|[\t])*(import ){1}([a-z]|[A-Z]|_|-|\.| )*?(,){1}([a-z]|[A-Z]|_|-|\.| )*?)$",
        #                            file_content_copy, re.MULTILINE)
        # tmp_list = [elmt[0] for elmt in found_imports]
        # if len(tmp_list):
        #     print(tmp_list)
        # for element in tmp_list:
        #     tmp = element.split(",")
        #     found_imports.extend([element.strip() for element in tmp])

        # line starts with import and ends with letter or number => one line with alias
        # tmp_imports = re.findall(r"^(([ ]{4}|[\t])*(import ){1}([a-z]|[A-Z]|_|-|\.)*?( as ){1}.{1,})$",
        #                          file_content_copy, re.MULTILINE)
        # found_imports.extend([elmt[0] for elmt in tmp_imports])

        # line starts with import and ends with "," => several lines
        # tmp_imports = re.findall(r"^(([ ]{4}|[\t])*(import ){1}([a-z]|[A-Z]|_|-|\.)*?( as ){1}.{1,})$",
        #                            file_content_copy, re.MULTILINE)
        # found_imports.extend([elmt[0] for elmt in tmp_imports])

        # line starts with import and ends with "\" => several lines
        # tmp_imports = re.findall(r"^(([ ]{4}|[\t])*(import ){1}([a-z]|[A-Z]|_|-|\.)*?( as ){1}.{1,})$",
        #                          file_content_copy, re.MULTILINE)
        # found_imports.extend([elmt[0] for elmt in tmp_imports])

        list_import.extend(found_imports)

        # We set all the import in unic list
        list_import = list(set(list_import))
        self.dict_project_analyze["MODULES"][relpath]["IMPORTS"] = list_import

        tmp = self.dict_project_analyze["PROJECT"]["STATS"]["NB_IMPORTS"]
        self.dict_project_analyze["PROJECT"]["STATS"]["NB_IMPORTS"] = tmp + len(list_import)


if __name__ == "__main__":
    pj_desc = "**************************** PyProject_analyzer ****************************" + \
              "\n\n                          Designed by A. GALODE" + \
              "\n                                MIT Licence" + \
              "\nGit Repository: https://bitbucket.org/deusyss/pyproject-analyzer/src/master/" + \
              "\n\n****************************************************************************"
    parser = argparse.ArgumentParser(description=pj_desc,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-p", "--path", dest="project_path", default=None,
                        help="Path of the code to analyze", action="store")
    parser.add_argument("-o", "--output_file", dest="output_report_file", default=None,
                        help="The path of the output file if file (Default: Terminal)",
                        action="store")
    parser.add_argument("-f", "--formater", dest="formater", default="JSON",
                        help="The formater to use (Default: JSON)", action="store")
    parser.add_argument("-r", "--req_file", dest="req_file", default=None,
                        help="The path of the requirement file to create", action="store")
    parser.add_argument("-s", "--stats-only", dest="stats_only", default=None, const=True,
                        help="Allow to analyze and only display the stats part to estimate "
                             "volumetry", action="store", nargs='?')
    parser.add_argument("-v", "--version", action="version",
                        version='PyProject-Analyze V{}'.format(__version__))

    args = parser.parse_args()

    tmp = PyProjectAnalyzer(args.project_path, args.formater, args.output_report_file,
                            args.req_file, args.stats_only)
    tmp.launch_and_report_analyze()

    tmp.dict_project_analyze["PROJECT"]["REQ_LIST"]
