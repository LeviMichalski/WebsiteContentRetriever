import yaml


def get_content_templates(file_name):
    print('Loading content templates: ')

    templates_file = open(file_name, 'r')
    templates = yaml.load(templates_file)
    templates_file.close()

    for template in templates:
        print(' - ' + template['name'])

    return templates
