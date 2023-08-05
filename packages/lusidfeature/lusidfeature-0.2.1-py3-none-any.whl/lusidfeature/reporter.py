import argparse

from lusidfeature.feature_extractor import extract_all_features_from_package
from lusidfeature.feature_file_writer import write_features_to_file


def extract_features_to_file(argv):
    ap = argparse.ArgumentParser(description="Get arguments from command line")
    ap.add_argument('-p', '--package', required=True, help='package name from the root folder sdk, not including the '
                                                           'root folder. Eg if root folder is "sdk", then package name '
                                                           'should be "tests.tutorials", not "sdk.tests.tutorials", '
                                                           'and also not "tutorials"')
    ap.add_argument('-o', '--outpath', required=True, help='Path and name of the features file to be created. Eg. '
                                                           '<path>/features.txt')
    ap.add_argument('-r', '--root', required=True, help='The path of root directory from which the decorator '
                                                                  'scanner should start traversing packages and '
                                                                  'modules. Recommended to be the root SDK folder or '
                                                                  'src folder rather than the base project path.')

    args = vars(ap.parse_args())
    package_name = args["package"]
    filepath = args["outpath"]
    root_dir = args["root"]

    feature_list = extract_all_features_from_package(package_name, root_dir)
    write_features_to_file(feature_list, filepath)
    print("File written to: " + filepath)
