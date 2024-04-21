import subprocess
import string


def checkout(cmd: str, text: str, find_words_mode: bool = False) -> bool:

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    print(result.stdout)

    if find_words_mode:
        translation_table = str.maketrans('', '', string.punctuation)
        output_without_punctuation = result.stdout.translate(translation_table).split()
        return text in output_without_punctuation
    else:
        return text in result.stdout

