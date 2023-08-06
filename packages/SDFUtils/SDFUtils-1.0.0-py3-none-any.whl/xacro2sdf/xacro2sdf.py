import os
import re
import sys
import math
from types import FunctionType

from xml.dom import minidom

XACRO_NS = "http://xacro"

def try_convert_to_number(value):
    try:
        return float(value)
    except:
        return value

class converter():
    def __init__(self):
        self.__root_doc = None
        self.__doc = None
        self.__properties = self.__init_properties()
        self.__macros = {}
        self.__file_dir = ""

    def __init_properties(self):
        return {
            "PI": math.pi
        }

    def run(self, input_file, output_file):
        self.__output_file = output_file
        # file_dir for relative include file
        self.__file_dir = os.path.dirname(input_file)
        self.__load(input_file, root=True)
        
        self.__save()

    def __load(self, file_name, root=False):
        doc = minidom.parse(file_name).documentElement
        if root:
            self.__root_doc = doc
        self.__run(doc)
        

    def __run(self, node):
        for e in node.childNodes:
            if e.nodeType == minidom.Node.ELEMENT_NODE:
                if "xacro:" in e.tagName:
                    cmd = e.tagName[6:]
                    if cmd == "macro":
                        self.__load_macros(e)
                    elif cmd == "property":
                        self.__load_properties(e)
                    elif cmd == "python": 
                        self.__load_python(e)
                    elif cmd == "include":
                        self.__load_includes(e)
                    else:
                        self.__run_macro(e, cmd)
                else:
                    for k, v in e.attributes.items():
                        replace , value = self.__eval_text(v)
                        if replace:
                            e.setAttribute(k, value)
            if e.nodeType == minidom.Node.TEXT_NODE:
                if len(e.nodeValue.strip()) > 0:
                    replace , value = self.__eval_text(e.nodeValue)
                    e.nodeValue = value

            if e.nodeType == minidom.Node.ELEMENT_NODE:
                if "xacro:" not in e.tagName:
                    self.__run(e)

    def __run_macro(self, node, cmd):
        kwargs = {}
        for k,v in node.attributes.items():
            _, kwargs[k] = self.__eval_text(v)
        for k,v in kwargs.items():
            kwargs[k] = try_convert_to_number(v)
        data = self.__macros[cmd](**kwargs)
        _, data = self.__eval_text(data, kwargs)
        parent = node.parentNode
        parent.removeChild(node)
        # add root tag for valid parse
        data = f"<macro xmlns:xacro='{XACRO_NS}'>" + data  + "</macro>"
        inner = minidom.parseString(data).documentElement
        for e in list(inner.childNodes):
            if e.nodeType == minidom.Node.ELEMENT_NODE:
                parent.appendChild(e)
                
        

    def __inner_xml(self, node):
        data = []
        for e in node.childNodes:
            if e.nodeType == minidom.Node.ELEMENT_NODE:
                data.append(e.toxml())#.replace("\n", "").replace(" ",""))
        result = "".join(data)
        return result

    def __load_macros(self, node):
        name = node.getAttribute("name")
        params = node.getAttribute("params")
        
        params_list = (",".join(params.strip().split()))
        f_body = self.__inner_xml(node)
        f_func_string = f'def {name}({params_list}): return """{f_body}"""'
        f_code = compile(f_func_string, "<string>", "exec")
        f_func = FunctionType(f_code.co_consts[0], globals(), name)
        self.__macros[name] = f_func
        parent = node.parentNode
        parent.removeChild(node)

    def __load_python(self, node): 
        # get node cdata - the text starts at the second child node.
        py_string = node.childNodes[1].nodeValue
        py_code = compile(py_string, "<string>", "exec")
        loc = {} # dict storing all the local varibales generated inside the py_code
        exec(py_code, globals(), loc)
        # loc['return_values'] needs to be a dictionary containing the name and property values wanting to be inserted to self.properties dict
        # append values to property dict
        for k in loc['return_values']: 
            self.__properties[k] = loc['return_values'][k]
        # print(loc['return_values'])

        parent = node.parentNode
        parent.removeChild(node)

    def __load_includes(self, node):
        # elements = node.getElementsByTagNameNS(XACRO_NS, "include")
        # for node in elements:
        if not node.hasAttribute("uri"):
            raise Exception("include uri not declare")
        package_path = os.path.join(os.path.dirname(__file__), "helpers")
        for prefix, source_dir in [
            (r'file://(.*?)', self.__file_dir),
            (r'package://(.*?)', package_path)
            ]:
            pattern = re.compile(prefix, re.S)
            match = pattern.search(node.getAttribute("uri"))
            if match:
                _, start = match.span()
                new_value = node.getAttribute("uri")[start:]
                file_name = os.path.join(source_dir, new_value)
                break

        parent = node.parentNode
        parent.removeChild(node)
        self.__load(file_name)

    def __load_properties(self, node):
        name = node.getAttribute("name")
        value = node.getAttribute("value")
        self.__properties[name] = try_convert_to_number(value)
        parent = node.parentNode
        parent.removeChild(node)
        
    def __eval_text(self, value, kwargs={}):
        subsitute = lambda o: str(eval(o.group(1), self.__properties, kwargs))
        pattern = re.compile(r'[$][{](.*?)[}]', re.S)
        new_value = re.sub(pattern, subsitute, value)
        return new_value!=value, new_value

    def __save(self):
        with (open(self.__output_file, "w")) as f:
            data = self.__root_doc.toxml()
            data = data.replace(f'xmlns:xacro="{XACRO_NS}"', "")
            f.writelines(data)

def main():
    """
    parse arguments and 
    """
    args_no = len(sys.argv)
    if args_no >= 2:
        inputfile = sys.argv[1]
        outputfile = os.path.splitext(inputfile)[0]
        if args_no == 3:
            outputfile = sys.argv[2]
        print(inputfile, outputfile)
        if args_no >= 4: 
            raise Exception("usage is: python3 xacro2sdf.xacro2sdf input_file output_file")
    else:
        dir_name = os.path.dirname(__file__)
        inputfile = os.path.join(dir_name, "../examples")
        inputfile = os.path.join(inputfile, "rrbot.sdf.xacro")
        outputfile = os.path.join(dir_name, "../output")
        outputfile = os.path.join(outputfile, "model.sdf")
        outputfile = "/home/user/projects/gazebo/models/rrbot/model.sdf"
        con = converter()
        con.run(inputfile, outputfile)

if __name__ == "__main__":
    main()