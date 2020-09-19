import sys
import yaml

print('Yaml file: ' + sys.argv[1])
with open(sys.argv[1], 'r') as stream:
    try:
        data_loaded = yaml.safe_load(stream)
        print(data_loaded)
        print("-----")
    except yaml.YAMLError as exc:
        print(exc)