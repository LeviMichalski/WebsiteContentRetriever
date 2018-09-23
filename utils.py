import yaml


# Opens a YAML file and returns the Python object
def read_yaml(file_name):
    templates_file = open(file_name, 'r')
    templates = yaml.load(templates_file)
    templates_file.close()
    return templates
