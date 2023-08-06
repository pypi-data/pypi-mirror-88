from json import loads
from pathlib import Path
import re
from typing import List, Dict, Union


class PyMdDoc:
    """
    Generate Markdown documentation for your Python scripts.

    ```python
    from py_md_doc import PyMdDoc
    from pathlib import Path

    # Generates the documentation for the py_md_doc module.
    md = PyMdDoc(input_directory=Path("."), files=["py_md_doc.py"], metadata_path="metadata.json")
    md.get_docs(output_directory=Path("../doc"))
    ```

    """

    """:class_var
    This is a test class variable. It doesn't do anything in this code other than test that the documentation generates correctly.
    """
    CLASS_VAR: int = 0

    def __init__(self, input_directory: Union[Path, str], files: List[str],
                 metadata_path: Union[Path, str] = None):
        """
        :param input_directory: The path to the root input directory for the Python scripts. Can be a `Path` or `str`.
        :param files: A list of Python script filenames relative to `input_directory`. This script will generate documentation only for these files.
        :param metadata_path: The path to the metadata file. Can be None. See the README for how to format this file.
        """

        if isinstance(input_directory, Path):
            pass
        elif isinstance(input_directory, str):
            input_directory = Path(input_directory)
        else:
            raise Exception("Invalid type: input_directory must be of type str or Path.")

        """:field
        A list of paths to each Python script file as `Path` objects.
        """
        self.files: List[Path] = list()
        for f in files:
            filepath = input_directory.joinpath(f)
            assert filepath.exists(), f"File not found: {filepath}"
            self.files.append(filepath)

        # Load the metadata.
        if metadata_path is None:
            """:field
            The metadata dictionary loaded from the metadata file. If there is no metadata file, this is empty.
            """
            self.metadata = dict()
        if metadata_path is not None:
            if isinstance(metadata_path, Path):
                pass
            elif isinstance(metadata_path, str):
                metadata_path = Path(metadata_path)
            else:
                raise Exception("Invalid type: categories_path must be of type str or Path.")
            self.metadata = loads(metadata_path.read_text(encoding="utf-8"))
        """:field
        The expected name of the root import name, derived the input directory.
        
        ```python
        from py_md_doc import PyMdDoc
        from pathlib import Path

        # Generates the documentation for the py_md_doc module.
        md = PyMdDoc(input_directory=Path("my_module"), files=["my_file.py"])
        print(md.root_import_name) # my_module
        ```
        """
        self.root_import_name = input_directory.name

        """:field
        A list of special import statements from `__init__.py`
        """
        self.special_imports: List[str] = list()

        init_path = input_directory.joinpath("__init__.py")
        if init_path.exists():
            init_txt = init_path.read_text(encoding="utf-8")
            for line in init_txt.split("\n"):
                special_import_match = re.match(r"from \.(.*) import (.*)", line)
                if special_import_match is not None:
                    self.special_imports.append(special_import_match.group(2))

    def get_docs(self, output_directory: Union[Path, str]) -> None:
        """
        Generate documents for all of the Python files and write them to disk.

        :param output_directory: The path to the output directory. Can be of type `Path` or `str`.
        """

        if isinstance(output_directory, Path):
            pass
        elif isinstance(output_directory, str):
            output_directory = Path(output_directory)
        else:
            raise Exception("Invalid type: output_directory must be of type str or Path.")

        if not output_directory.exists():
            output_directory.mkdir(parents=True)

        for f in self.files:
            # Create the documentation.
            doc = self.get_doc(f)
            # Name the document based on the name of the Python script. Write it to disk.
            output_directory.joinpath(f.name[:-3] + ".md").write_text(doc)

    def get_doc(self, file: Path) -> str:
        """
        Create a document from a Python file with the API for each class. Returns the document as a string.

        :param file: The path to the Python script.
        """

        # Create the header.
        doc = ""

        file_txt = file.read_text(encoding="utf-8")
        lines: List[str] = file_txt.split("\n")

        class_name = ""
        functions_by_categories = {"": []}

        for i in range(len(lines)):
            # Create a class description.
            if lines[i].startswith("class"):
                # Skip private classes.
                match = re.search("class _(.*):", lines[i])
                if match is not None:
                    continue
                # Add the name of the class
                class_name = re.search("class (.*):", lines[i]).group(1)
                class_header = re.sub(r"(.*)\((.*)\)", r"\1", class_name)

                functions_by_categories.clear()

                doc += f"# {class_header}\n\n"

                # Add an example import statement.
                if class_header in self.special_imports:
                    import_example = f"`from {self.root_import_name} import {class_header}`"
                else:
                    import_example = f"`from {self.root_import_name}.{file.name[:-3]} import {class_header}`"
                doc += import_example + "\n\n"
                doc += PyMdDoc.get_class_description(file_txt)
                # Parse an enum.
                if re.search(r"class (.*)\(Enum\):", lines[i]) is not None:
                    doc += "\n\n" + PyMdDoc.get_enum_values(lines, i)
                else:
                    doc += "\n\n***\n\n"
                # Get class variables.
                class_variables = PyMdDoc.get_class_variables(lines, i)
                if class_variables != "":
                    doc += f"## Class Variables\n\n{class_variables}\n\n***\n\n"
            # Create a function description.
            elif lines[i].strip().startswith("def "):
                # Skip private functions.
                match = re.search("def _(.*)", lines[i])
                if match is not None and "__init__" not in lines[i]:
                    continue
                if "__init__" in lines[i]:
                    field_documentation = PyMdDoc.get_fields(lines, i)
                    if field_documentation != "":
                        doc += f"## Fields\n\n{field_documentation}\n\n***\n\n## Functions\n\n"

                # Append the function description.
                function_documentation = PyMdDoc.get_function_documentation(lines, i, class_name) + "\n\n"
                function_name = re.search("#### (.*)", function_documentation).group(1).replace("\\_", "_")

                # Categorize the functions.
                function_category = ""
                if class_name in self.metadata:
                    for category in self.metadata[class_name]:
                        if function_name in self.metadata[class_name][category]["functions"]:
                            function_category = category
                            break
                    if function_category == "":
                        print(f"Warning: Uncategorized function {class_name}.{function_name}()")
                if function_category == "":
                    doc += function_documentation
                # Add this later.
                else:
                    if function_category not in functions_by_categories:
                        functions_by_categories[function_category] = list()
                    functions_by_categories[function_category].append(function_documentation)
        if class_name in self.metadata:
            for category in self.metadata[class_name]:
                if category != "Constructor":
                    doc += f"### {category}\n\n"
                    if self.metadata[class_name][category]["description"] != "":
                        doc += f'_{self.metadata[class_name][category]["description"]}_\n\n'
                for function in functions_by_categories[category]:
                    doc += function
                doc += "***\n\n"

        return doc

    @staticmethod
    def get_class_variables(lines: List[str], start_index: int) -> str:
        """
        :param lines: All of the lines of the file.
        :param start_index: Start looking for fields at this line.

        :return: A table of class variables as a string.
        """

        txt = ""
        for i in range(start_index, len(lines)):
            # We assume that all class variables are declared before the constructor.
            if "def __init__" in lines[i]:
                break
            txt += lines[i] + "\n"
        # Parse all lines that have class variable documentation.
        class_var_lines = re.findall(r'""":class_var(((.*)+[\n]+)+?[\s]+)"""\n[\s]+(.*)=', txt, flags=re.MULTILINE)
        if len(class_var_lines) <= 0:
            return ""
        # Create a table.
        class_vars = "| Variable | Type | Description |\n| --- | --- | --- |\n"
        for lines in class_var_lines:
            desc = lines[0].strip()
            var_split = lines[-1].split(":")
            var = var_split[0]
            if len(var_split) > 1:
                var_type = var_split[1].strip()
            else:
                var_type = ""
            class_vars += f"| `{var}` | {var_type} | {desc} |\n"
        return class_vars.strip()

    @staticmethod
    def get_fields(lines: List[str], start_index: int) -> str:
        """
        Get the field descriptions for this class.

        :param lines: All of the lines of the file.
        :param start_index: Start looking for fields at this line.

        :return: A string of field documentation.
        """

        init_txt = lines[start_index]
        match = re.search(r"def (.*)\):", init_txt, flags=re.MULTILINE)
        count = 1
        while match is None:
            init_txt += lines[start_index + count].strip()
            match = re.search(r"def (.*)\):", init_txt, flags=re.MULTILINE)
            count += 1
        init_func = ""
        for i in range(start_index + count, len(lines)):
            if "def " in lines[i]:
                break
            init_func += lines[i] + "\n"

        fields = ""
        got_fields = True
        while got_fields:
            # Find field tags for each field.
            field_match = re.search(r'""":field(((.*)+[\n]+)+?[\s]+)"""\n[\s]+self\.(.*)', init_func, flags=re.MULTILINE)
            if field_match is not None:
                # Reduce whitespace.
                field_desc = field_match.group(1).strip()
                field_desc = re.sub(r"(\A *\d+\. *|^ {0,8})", r"", field_desc, flags=re.MULTILINE)
                # Get the field name.
                field_name = field_match.group(4).split(":")[0].split("=")[0].strip()

                fields += f"- `{field_name}` " + field_desc + "\n\n"
                init_func = init_func.replace(field_match.group(0), "")
            else:
                got_fields = False
        return fields.strip()

    @staticmethod
    def get_class_description(file_txt: str) -> str:
        """
        Parses a file starting at a line defined by start_index to get the class name and description.
        This assumes that the class has a triple quote description.

        :param file_txt: All of the text of the file.
        """

        class_desc = re.search(r'class (.*):\n[\s]+"""\n([\s]+((.*)+[\n]+)+?[\s]+)"""', file_txt,
                               flags=re.MULTILINE).group(2)
        class_desc = re.sub(r"(\A *\d+\. *|^ {0,4})", r"", class_desc, flags=re.MULTILINE)
        # Remove trailing new lines.
        class_desc = class_desc.strip()
        return class_desc

    @staticmethod
    def get_function_documentation(lines: List[str], start_index: int, class_name: str) -> str:
        """
        Create documentation for a function and its parameters.

        :param lines: The lines of the Python script.
        :param start_index: Start at this line to search for function documentation.
        :param class_name: The name of the class. Used for static function documentation.

        :return: The function documentation string.
        """

        began_desc = False
        function = ""

        txt = lines[start_index][:]
        # Get the definition string across multiple lines.
        if "__init__" in lines[start_index]:
            match = re.search(r"def (.*)\):", txt, flags=re.MULTILINE)
            count = 1
            while match is None:
                txt += lines[start_index + count]
                match = re.search(r"def (.*)\):", txt, flags=re.MULTILINE)
                count += 1
            def_str = match.group(1)
            def_str = " ".join(def_str.split()) + ")"
        else:
            match = re.search(r"def (.*) -> (.*):", txt, flags=re.MULTILINE)
            count = 1
            while match is None:
                txt += lines[start_index + count]
                match = re.search(r"def (.*) -> (.*):", txt, flags=re.MULTILINE)
                count += 1
            def_str = match.group(1) + " -> " + match.group(2)
            def_str = " ".join(def_str.split())
        # Used the shortened def string for the header.
        shortened_def_str = def_str.split("(")[0].replace("__", "\\_\\_")

        is_static = lines[start_index - 1].strip() == "@staticmethod"

        parameters: Dict[str, str] = {}
        return_description = ""
        func_desc = ""
        for i in range(start_index + 1, len(lines)):
            line = lines[i].strip()
            if '"""' in line:
                # Found the terminating triple quote.
                if began_desc:
                    break
                # Found the beginning triple quote.
                else:
                    began_desc = True
                    continue
            elif began_desc:
                # Get a parameter.
                if line.startswith(":param"):
                    param_name = line[7:].split(":")[0]
                    param_desc = line.replace(":param " + param_name + ": ", "").strip()
                    parameters.update({param_name: param_desc})
                elif line == "":
                    func_desc += "\n"
                # Get the return description
                elif line.startswith(":return:"):
                    return_description = line[8:]
                # Get the overview description of the function.
                else:
                    func_desc += line + "\n"
        def_str = def_str.replace("\\ ", "")

        # Get some example code.
        if is_static:
            example_call = f"{class_name}.{shortened_def_str}("
        else:
            if shortened_def_str == "\\_\\_init\\_\\_":
                example_call = f"{class_name.split('(')[0]}("
            else:
                example_call = f"self.{shortened_def_str}("
        for parameter in parameters:
            example_call += parameter + ", "
        if example_call.endswith(", "):
            example_call = example_call[:-2]
        example_call += ")"

        function += f"#### {shortened_def_str}\n\n**`{example_call}`**\n\n"
        if is_static:
            function += "_This is a static function._\n\n"
        function += func_desc

        if function[-1] == "\n":
            function = function[:-1]
        # Add the paramter table.
        if len(parameters) > 0:
            function += "\n| Parameter | Type | Description |\n| --- | --- | --- |\n"
            for parameter in parameters:
                # Get the parameter type from the def string.
                param_type = re.search(parameter + r":(.*?)[:|=|\)]", def_str)
                if param_type is None:
                    param_type = ""
                else:
                    param_type = param_type.group(1)
                    if "]" in param_type:
                        param_type = param_type.split("]")[0] + "]"
                    else:
                        param_type = param_type.split(",")[0]
                function += f"| {parameter} | {param_type} | {parameters[parameter]} |\n"
            function += "\n"
        # Remove trailing new lines.
        while function[-1] == "\n":
            function = function[:-1]
        # Add the return value.
        if return_description != "":
            function += "\n\n_Returns:_ " + return_description
        return function

    @staticmethod
    def get_enum_values(lines: List[str], start_index: int) -> str:
        """
        Returns a list of enum values.

        :param lines: The lines in the document.
        :param start_index: The line of the class defintion.
        """

        enum_desc = "| Value | Description |\n| --- | --- |\n"
        began_class_desc = False
        end_class_desc = False
        for i in range(start_index + 1, len(lines)):
            if "class " in lines[i]:
                break
            if lines[i] == "":
                continue
            if '"""' in lines[i]:
                if not began_class_desc:
                    began_class_desc = True
                else:
                    end_class_desc = True
                continue
            if not end_class_desc:
                continue
            line_split = lines[i].strip().split(" = ")
            val = f"`{line_split[0]}`"
            desc_split = lines[i].strip().split("#")
            if len(desc_split) > 1:
                desc = desc_split[1].strip()
            else:
                desc = ""
            enum_desc += f"| {val} | {desc} |\n"
        return enum_desc.strip()


if __name__ == "__main__":
    md = PyMdDoc(input_directory=Path("."), files=["py_md_doc.py"], metadata_path="metadata.json")
    md.get_docs(output_directory=Path("../docs"))
