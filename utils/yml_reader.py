import yaml


def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'r')as file:
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    return yaml_data
