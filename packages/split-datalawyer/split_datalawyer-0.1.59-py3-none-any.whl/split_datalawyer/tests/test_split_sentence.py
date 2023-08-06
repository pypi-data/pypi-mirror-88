import os
from split_datalawyer.sentences.sentence_split import SentenceSplit
from split_datalawyer.modules import *

# massive_avaliation = False
massive_avaliation = True

SPLIT_SEMICOLON = massive_avaliation

files_content = []
files_base = []

local_path = os.path.dirname(__file__)

if massive_avaliation:
    local_path = os.path.join(local_path, "massive_avaliation")

examples_dir = os.path.join(local_path, "examples")
base_splitted_dir = os.path.join(local_path, "base_splitted")
new_base_dir = os.path.join(local_path, "new_base")
files = os.listdir(examples_dir)

for file in files:
    example_name = ".".join(file.split(".")[0:-1])
    with open(os.path.join(examples_dir, file), "r", encoding="utf8") as fs:
        content = fs.read()
        files_content.append((file, content))

    base_file_name = example_name + ".base"
    base_file_path = os.path.join(base_splitted_dir, base_file_name)

    if os.path.exists(base_file_path):
        with open(base_file_path, "r", encoding="utf8") as fs:
            content = fs.readlines()
            files_base.append((file, content))
    else:
        files_base.append((file, ""))

sentence_spliter = SentenceSplit(debug_log=True,
                                 modules=[ForceDropDuplicatedModule(), ReplaceModule(), ReplaceLongWordsModule(),
                                          ReplaceConcatenatedDotModule()])

path_evaluation_file = os.path.join(local_path, "sentences_updated.txt")
if os.path.exists(path_evaluation_file):
    os.remove(path_evaluation_file)

for indice, file_content in enumerate(files_content):
    base = files_base[indice]
    assert base[0] == file_content[0]

    if base[0] == "0100314-53.2020.5.01.0501-2c75bd6.txt":
        stop_parar = ""

    text_splitted = sentence_spliter.get_sentences(file_content[1], split_by_semicolon=SPLIT_SEMICOLON)
    # Using stanza
    # text_splitted = sentence_spliter.get_sentences_with_stanza(file_content[1])

    file_name_writted = False
    generate_base = False

    if base[1] == "":
        file_name_writted = True
        generate_base = True

    if base[1] != "":
        for indice, sentence in enumerate(text_splitted):
            base_sentence = str(base[1][indice]).replace("\n", "")
            try:
                assert sentence == base_sentence
            except:
                fs = open(path_evaluation_file, mode="a", encoding='utf8')

                if not file_name_writted:
                    fs.write("\n" + file_content[0] + "\n")
                    file_name_writted = True

                fs.write("base:\n")
                fs.write(base_sentence + "\n")
                fs.write("new_base:\n")
                fs.write(sentence + "\n\n")
                break

    if file_name_writted:
        extension = ".new_base"
        if generate_base:
            extension = ".base"
        result_file = os.path.join(new_base_dir, file_content[0] + extension)

        with open(result_file, "w", encoding='utf8') as fs:
            for text in text_splitted:
                fs.write(text + "\n")

sentence_spliter.generate_log()
print("Test complete. Check 'new_base' directory for changes.")
