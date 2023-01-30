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


def execute_query(user_query, variables):
    headers = {"Authorization": "token your token"}

    def run_query(query,variables):  # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables},
                                headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
    query = Constants.QUERY_RATE_LIMIT

    result = run_query(query, "")  # Execute the query
    remaining_rate_limit = result["data"]["rateLimit"]["remaining"]  # Drill down the dictionary
    print("Remaining rate limit - {}".format(remaining_rate_limit))

    return run_query(user_query, variables)


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


def find_dependencies(repository_query_result,default_repository_name):
    generated_rows = []
    if repository_query_result['data']['repository']['object'] is None or \
            repository_query_result['data']['repository']['object']['entries'] is None:
        print("repositorio sem nenhum arquivo/diretorio ")
        return

    root_entries = repository_query_result['data']['repository']['object']['entries']

    found_dependencies = extract_text(root_entries, 'Podfile')
    # print_founded(found_dependencies)
    generated_rows.extend(generate_rows(found_dependencies,default_repository_name))

    found_dependencies = extract_text(root_entries, 'build.gradle')
    # print_founded(found_dependencies)
    # print(json.dumps(found_dependencies, indent=4))

    generated_rows.extend(generate_rows(found_dependencies,default_repository_name))

    # export_to_excel(generated_rows)

def generate_rows(found_dependencies, default_repository_name):
    generated_rows = []
    rows_module_name = []
    rows_file_content = []
    for path_to_file, file_content in found_dependencies.items():
        current_row = []
        module_name = default_repository_name
        path_splited = path_to_file.split("/")
        if len(path_splited) > 1:
            module_name = path_splited[(len(path_splited) - 2)]  # recupera o diretorio 1 nivel acima do arquivo

        rows_module_name.append(module_name)
        rows_file_content.append(file_content)
        current_row.append(module_name)
        current_row.append(file_content)
        generated_rows.append( current_row )

    # print(generated_rows)
    return generated_rows
#
# def export_to_excel(rows):
#     #   TODO

def execute_script():
    selected_repo = "androidskilltest2"
    owner = "jelvissilva"
    variables = {
        "selected_repo": selected_repo,
        "owner": owner
    }

    repository_query_result = execute_query(Constants.QUERY_REPOS, variables)
    # print(json.dumps(repository_query_result, indent=4))

    find_dependencies(repository_query_result,selected_repo)



if __name__ == '__main__':
    execute_script()
