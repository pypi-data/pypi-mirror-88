from typing import get_type_hints

from dataclasses_json import dataclass_json

from grebble_flow.managment.processor import find_all_processors


def get_processors_info():
    result = []
    processors = find_all_processors()
    for processor in processors:
        item = {"name": processor.name}
        if hasattr(processor, "attributes"):
            item['attributes_schema'] = get_type_hints(processor.attributes)
            for key in item['attributes_schema']:
                item['attributes_schema'][key] = {
                    "type": item['attributes_schema'][key].__name__,
                }
        result.append(item)
    return result


def generate_package_info():
    result = {"processors": get_processors_info()}
    return result
