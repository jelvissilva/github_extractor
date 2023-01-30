# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import requests

import Constants

def print_founded(found_dependencies):
    print("dependencias encontradas: ")
    for idx, dependencie in enumerate(found_dependencies):
        print(f"dependencia {idx}:")
        print(dependencie)

def execute_query():
    headers = {"Authorization": "token your_token"}

    def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
    query = Constants.QUERY_RATE_LIMIT

    result = run_query(query)  # Execute the query
    remaining_rate_limit = result["data"]["rateLimit"]["remaining"]  # Drill down the dictionary
    print("Remaining rate limit - {}".format(remaining_rate_limit))

    return run_query(Constants.QUERY_REPOS)


def find_file_by_name(file_name_requested, json_entry):
    is_directory = False
    text_found = None
    entry_name = json_entry['name']

    if file_name_requested.casefold() == entry_name.casefold():
        text_found = json_entry

    if 'entries' in json_entry['object']:
        is_directory = True

    return is_directory, text_found

# percorre a arvore de entries recursivamente
# Requesitos:
# 1.todos nós object da consultam precisam ter object blob com o atributo text,
# 2.todos nós object pai precisam ter tambem um objeto on Tree -> entries com o atributo name e path mapeado
# Ex:   Repository -> object -> on Tree -> entries[0] -> on Blob
#                               on Blob
#
def extract_text(requested_entries, requested_file_name):
    text_found = {}
    for entry in requested_entries:
        is_directory, requested_object_json = find_file_by_name(requested_file_name, entry)

        if is_directory:
            recursive_result = extract_text(entry['object']['entries'], requested_file_name)
            text_found.update(recursive_result)

        elif requested_object_json is not None:
            text_found[entry['path']] = requested_object_json['object']['text']

    return text_found


def find_dependencies(result):
    if result['data']['repository']['object'] is None or result['data']['repository']['object']['entries'] is None:
        print("repositorio sem nenhum arquivo/diretorio ")
        return

    root_entries = result['data']['repository']['object']['entries']

    found_dependencies = extract_text(root_entries, 'Podfile')
    # print_founded(found_dependencies)

    found_dependencies = extract_text(root_entries, 'build.gradle')
    print_founded(found_dependencies)
    print(json.dumps(found_dependencies, indent=4))

def execute_script():
    result = execute_query()
    # print(json.dumps(result, indent=4))

    find_dependencies(result)


if __name__ == '__main__':
    execute_script()
