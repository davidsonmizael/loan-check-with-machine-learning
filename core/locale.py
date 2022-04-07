import os
import json
from threading import local

def get_locale_file_for_language(language):

    lang, country = language.split('-')

    file_name = f"{lang.lower()}-{country.upper()}.json"

    files_path = os.path.dirname(os.path.realpath(__file__)).split('core',1)[0] + 'config/locale/'
    with open(files_path + file_name) as f:
        return json.load(f)


def get_message(language, placeholder):
    locale_file =  get_locale_file_for_language(language)

    msg_placeholder = placeholder[1:-1].split('.')[1]

    return locale_file["messages"][msg_placeholder]


