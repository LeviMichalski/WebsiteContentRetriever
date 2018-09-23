import utils


def welcome():
    print()
    print('Website Content Retriever 1.0')
    print(' - Authors: Levi Michalski, Tim Michalski')
    print()


def setup():
    print('Loading content templates: ')
    templates = utils.read_yaml('templates.yaml')

    for template in templates:
        print(' - ' + template['name'])
