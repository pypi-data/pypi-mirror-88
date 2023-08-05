from docstring_parser import parse

from grebble_flow.managment.processor import find_all_processors


def get_processors_info():
    result = []
    processors = find_all_processors()
    for processor in processors:
       # doc = parse(base.execute.__doc__)
        result.append({"name": processor.name})
    return result


def generate_package_info():
    result = {"processors": get_processors_info()}
    return result
