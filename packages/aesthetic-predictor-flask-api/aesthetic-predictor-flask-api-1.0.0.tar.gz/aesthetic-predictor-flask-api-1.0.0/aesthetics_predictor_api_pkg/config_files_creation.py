import json
import argparse
import os

import wget as wget


def create_api_config_file(file_name, port):
    api_config_dict = {"predictorModulePath": "dotted.path.to.module.containing.predictor.class",
                       "predictorClassName": "className",
                       "port": port}
    with open(file_name, 'w+') as api_config_file:
        json.dump(api_config_dict, api_config_file, sort_keys=True, indent=4)


def create_gunicorn_config_file(file_name, port):
    gunicorn_config_text = "bind = \"0.0.0.0:" + str(
        port) + "\"\n" + "workers = 2\n" + "threads = 4\n" + "timeout = 120"
    with open(file_name, 'w+') as gunicorn_config_file:
        gunicorn_config_file.write(gunicorn_config_text)


# !!url has to be on one line for wget to fetch the templates
def create_dockerfile_template(port):
    conda_env = os.getenv('CONDA_DEFAULT_ENV')
    if conda_env is None:
        file_name = "Dockerfile_VirtualEnv_Template"
        url = "https://raw.githubusercontent.com/RibinMTC/DockerConfigShare/master/Dockerfile templates/Dockerfile_VirtualEnv_Template"
        __fetch_file_from_url(url, file_name)
    else:
        file_name = "Dockerfile_Conda_Template"
        url = "https://raw.githubusercontent.com/RibinMTC/DockerConfigShare/master/Dockerfile templates/Dockerfile_Conda_Template"
        __fetch_file_from_url(url, file_name)

    __modify_dockerfile_template(file_name, conda_env, port)


def __fetch_file_from_url(url, file_dest):
    print("Fetching " + file_dest)
    if os.path.exists(file_dest):
        os.remove(file_dest)
    wget.download(url, file_dest)


def __modify_dockerfile_template(file_name, conda_env, port):
    conda_key_word = "name_of_conda_env"
    port_keyword = "port_num_of_predictor"
    new_file_content = ""

    with open(file_name, 'r+') as dockerfile_template:
        for line in dockerfile_template:
            stripped_line = line.strip()
            if conda_env is not None and conda_key_word in stripped_line:
                stripped_line = stripped_line.replace(conda_key_word, str(conda_env))
            if port_keyword in line:
                stripped_line = stripped_line.replace(port_keyword, str(port))

            new_file_content += stripped_line + "\n"

    with open(file_name, 'w') as dockerfile_template:
        dockerfile_template.write(new_file_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--port', type=int, required=True,
                        help="The port on which the flask api runs")

    args = parser.parse_args()

    api_config_file_name = "api_config.json"
    gunicorn_config_file_name = "gunicorn_config.py"

    create_api_config_file(api_config_file_name, args.port)
    create_gunicorn_config_file(gunicorn_config_file_name, args.port)
    create_dockerfile_template(args.port)
