import pandas as pd
import os
import re
import html

import stanza

from split_datalawyer.modules.modules_types import ModulesType
from split_datalawyer.sentences.split_utils import split_by_sentence, split_by_break
from split_datalawyer.utils import ABBREVIATION_LIST, CONTINUATION_TERMS, get_stop_patterns

__ENDING_PUNCTUATION_TUPLE__ = tuple([".", ";", ":", "\"", "!", "?", ")"])
__REGEX_SECTION_NUMBERS__ = [re.compile(r"^[0-9]{1,}(\.[0-9]+)?(\.|\.-)$"),  # "1.0.", "4.2.", "02.-"
                             re.compile(r"^([MDCLXVI]{1,3}\.|[MDCLXVI]{1,3}\-)$")]  # "I.", "II."


class SentenceSplit():

    def __init__(self, stop_patterns_path=None, debug_log=False, modules=[]):
        self._list_stop_patterns = get_stop_patterns(stop_patterns_path)
        self._list_abbreviations = ABBREVIATION_LIST
        self._stanza_model = None
        self._debug_log = debug_log
        self._debug_messages = []
        self._modules = modules

    def _log(self, message):
        if self._debug_log:
            self._debug_messages.append(message)

    def _get_models_by_type(self, module_type):
        modules = []

        for module in self._modules:
            if module.get_type() == module_type:
                modules.append(module)

        return modules

    def _must_remove_duplicated(self, remove_duplicated, document_sentences):
        if remove_duplicated:
            return remove_duplicated

        must_remove = False
        conditional_modules = self._get_models_by_type(ModulesType.DUPLICATED_CONDITION)

        for module in conditional_modules:
            must_remove = must_remove and module.evaluate(document_sentences)

        return must_remove

    def generate_log(self):
        if self._debug_log:
            with open("sentence_split_log.txt", mode='w', encoding='utf8') as log_file:
                for message in self._debug_messages:
                    log_file.write(message + "\n")

    def _parenthesis_is_closed(self, phrase):
        if phrase != "":
            if phrase.count("(") > phrase.count(")") or phrase.rfind(")") < phrase.rfind("("):
                return False

        return True

    def _end_with_abbreviation(self, text: str):
        if text.startswith(tuple(["(", "\""])):
            text = text[1:]
        return text.strip().lower() in self._list_abbreviations

    def _end_with_continuation(self, text: str):
        return any(len(regex.findall(text)) > 0 for regex in CONTINUATION_TERMS)

    def _concat_inverted_phrases(self, df):
        df = df[df['final_text'] != ""]
        df = df.sort_values('index').reset_index(drop=True)

        for i in range(1, len(df['final_text'])):
            previous_text = df['final_text'][i - 1]
            current_text = df['final_text'][i]

            if current_text != "":
                if i + 1 < len(df['final_text']):
                    next_text = df['final_text'][i + 1]

                    previous_has_end = previous_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    current_text_starts_lower = current_text[0].islower()
                    current_text_has_end = current_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    next_has_not_end = not next_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    next_text_is_not_option = re.match(r"^\w\)", next_text) is None
                    next_is_not_all_upper = not (next_text.isupper() and len(next_text) > 1)

                    if current_text_starts_lower and \
                            current_text_has_end and \
                            previous_has_end and \
                            next_has_not_end and \
                            next_text_is_not_option and next_is_not_all_upper:
                        df.at[i + 1, 'final_text'] = next_text + " " + current_text
                        df.at[i, 'final_text'] = ""
                        self._log("_concat_inverted_phrases: " + next_text + " " + current_text)

        return df

    def _concat_broken_phrases(self, df):
        df['final_text'] = df['text']
        last_index_with_text = None

        for i in range(len(df['final_text'])):
            current_text = df['final_text'][i].strip()

            if current_text == "":
                continue

            if last_index_with_text is not None:
                last_text_processed = df['final_text'][last_index_with_text]

                last_text_end_punctuation = last_text_processed.endswith(__ENDING_PUNCTUATION_TUPLE__)
                starts_money_simbol = current_text.startswith("R$") and last_text_end_punctuation
                starts_with_parentese = current_text.startswith("(") and last_text_end_punctuation

                is_section_number = any(regex.match(last_text_processed) for regex in __REGEX_SECTION_NUMBERS__)

                if starts_money_simbol or starts_with_parentese or is_section_number:
                    current_text = " ".join([last_text_processed, current_text])
                    df.at[i, 'final_text'] = current_text
                    df.at[last_index_with_text, 'final_text'] = ""

            end_with_punctuation = current_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
            current_text_end_with_abbreviation = self._end_with_abbreviation(current_text.split()[-1])
            all_text_upper = current_text.isupper() and len(current_text) > 1
            parenthesis_not_closed = not self._parenthesis_is_closed(current_text)
            search_phrase_continuation = (not end_with_punctuation and not all_text_upper) or \
                                         (parenthesis_not_closed and (not end_with_punctuation) or \
                                          current_text_end_with_abbreviation)
            phrase_has_continuation = False

            if search_phrase_continuation:
                phrases_parts_index = []
                previous_phrase_index = 1
                waiting_close_parenthesis = parenthesis_not_closed

                for j in range(i + 1, len(df['final_text'])):
                    next_text = df['final_text'][j]
                    next_text_was_duplicated = bool(df['duplicated'][j])

                    if next_text == "" or next_text_was_duplicated:
                        previous_phrase_index = previous_phrase_index + 1
                        if next_text_was_duplicated:
                            self._log("_concat_broken_phrases: next_text_was_duplicated: " + next_text)
                        continue

                    previous_ends_with_continuation = False
                    previous_text_end_with_abbreviation = False

                    if j - previous_phrase_index >= 0:
                        previous_text = df['final_text'][j - previous_phrase_index]
                        if previous_text is not "":
                            previous_end = previous_text.split()[-1]

                            previous_ends_with_continuation = self._end_with_continuation(previous_text)
                            previous_text_end_with_abbreviation = self._end_with_abbreviation(previous_end)

                    # Not allow concatenate parts with high difference distance.
                    parts_not_too_long_distance = ((len(phrases_parts_index) > 0) and
                                                   max(phrases_parts_index) - j <= 5) \
                                                  or (j - i <= 5)

                    if (next_text.split()[0][0].islower() or
                        previous_ends_with_continuation or
                        previous_text_end_with_abbreviation or
                        waiting_close_parenthesis) and parts_not_too_long_distance:

                        phrases_parts_index.append(j)
                        next_text_end_not_with_abbreviation = not self._end_with_abbreviation(next_text.split()[-1])

                        waiting_close_parenthesis = not self._parenthesis_is_closed(next_text)

                        if next_text.endswith(__ENDING_PUNCTUATION_TUPLE__) and \
                                next_text_end_not_with_abbreviation and \
                                waiting_close_parenthesis:
                            self._log("waiting_close_parenthesis: " + df['final_text'][j])

                        # go_concatenate = next_text.endswith(__ENDING_PUNCTUATION_TUPLE__) and next_text_end_not_with_abbreviation and (not waiting_close_parenthesis)
                        go_concatenate = next_text.endswith(
                            __ENDING_PUNCTUATION_TUPLE__) and next_text_end_not_with_abbreviation
                        if go_concatenate:
                            phrase_has_continuation = True
                            break
                    else:
                        if len(phrases_parts_index) > 0:
                            phrase_parts_log = [df['final_text'][index] for index in phrases_parts_index]
                            phrase_parts_log = "[" + "| ".join(phrase_parts_log) + "]"

                            if (len(phrases_parts_index) >= 3) or parenthesis_not_closed:
                                phrase_has_continuation = True
                                self._log("_concat_broken_phrases: threshold pass: " + phrase_parts_log)
                            else:
                                self._log(
                                    "_concat_broken_phrases: ignored_parts: " + phrase_parts_log + " next_text: " + next_text)

                        break

                end_of_phrase = ""
                if phrase_has_continuation:
                    for part_index in phrases_parts_index:
                        phrase_part = df['final_text'][part_index]
                        end_of_phrase = end_of_phrase + " " + phrase_part
                        df.at[part_index, 'final_text'] = ""

                    if end_of_phrase != "":
                        df.at[i, 'final_text'] = current_text + " " + end_of_phrase.strip()

            last_index_with_text = i

        return df

    def _remove_small_phrases(self, df, minimium_word_count=3):
        if minimium_word_count > 0:
            df['final_text'] = df['text']

            for i in range(len(df['final_text'])):
                phrase_is_small = len(df['final_text'][i].split()) < minimium_word_count

                if phrase_is_small:
                    df.at[i, 'final_text'] = ""

        return df

    def _remove_stop_phrases(self, df):
        if df.empty:
            return None

        for i, row in df.iterrows():
            current_value = row['text']
            is_number_page = current_value.isdigit()
            if is_number_page:
                self._log("is_number_page: " + current_value)
            is_stop_phrase = any(regex.match(current_value) for regex in self._list_stop_patterns)
            remove_text = is_number_page or is_stop_phrase
            if remove_text:
                df.at[i, 'text'] = ""
        df = df[df['text'] != ""].reset_index(drop=True, inplace=False)
        return df

    def _remove_duplicates(self, df):
        df = df[df['text'] != ""]
        df = df.sort_values(['text', 'index']).reset_index(drop=True)
        duplicated_phrases = list(df[df['duplicated']]['text'])
        self._log("_remove_duplicates: duplicated_phrases: [" + '| '.join(duplicated_phrases) + "]")

        previous_value = ""
        phrases_count = len(df['text'])
        for i in range(phrases_count):
            reserve_index = phrases_count - i - 1
            current_value = df['text'][reserve_index]

            both_equals = previous_value == current_value

            if both_equals:
                df.at[reserve_index, 'text'] = ""

            if df['text'][reserve_index] != "":
                previous_value = df['text'][reserve_index]

        df = df[df['text'] != ""]
        df = df.sort_values('index').reset_index(drop=True)

        return df

    def _split_by_punctuation(self, df, split_by_semicolon):
        column_name = 'text'

        if "final_text" in df.columns:
            column_name = 'final_text'

        df = df[df[column_name] != ""].reset_index(drop=True, inplace=False)

        phrase_list = []

        for index, row in df.iterrows():
            text = row[column_name]
            duplicated = row['duplicated']
            phrases = split_by_sentence(text, split_by_semicolon)
            phrase_list.extend([{"duplicated": duplicated, "text": phrase} for phrase in phrases])

        temp_object_list = [
            {'index': index, 'text': phrase_list[index]["text"], 'duplicated': phrase_list[index]["duplicated"]}
            for index in range(len(phrase_list))]

        df_splited = pd.DataFrame(temp_object_list)

        return df_splited

    def get_sentences(self, text, remove_duplicated=True, concat_phrases=True, concat_inverted_phrases=True,
                      remove_stop_phrases=True, minimium_word_count=0, split_by_semicolon=True):
        if (text is None) or text == "":
            return None

        df = self.get_sentences_with_index(text,
                                           remove_duplicated=remove_duplicated,
                                           concat_phrases=concat_phrases,
                                           concat_inverted_phrases=concat_inverted_phrases,
                                           remove_stop_phrases=remove_stop_phrases,
                                           minimum_word_count=minimium_word_count,
                                           split_by_semicolon=split_by_semicolon)

        if df is not None:
            column_name = 'text'

            if "final_text" in df.columns:
                column_name = 'final_text'

            df = df[df[column_name] != ""].reset_index(drop=True, inplace=False)
            sentences = list(df[column_name])

            return sentences

        return []

    def _process_df_pipeline(self, df, pipeline_functions):
        for func_step in pipeline_functions:
            if df is None or df.empty:
                return None
            df = func_step(df)

        return df

    def _mark_duplicated_text(self, df):
        df['duplicated'] = df['text'].duplicated(False)
        return df

    def _remove_empty_rows(self, df):
        df = df[df['text'] != ""].reset_index(drop=True, inplace=False)
        return df

    def _create_sentences_data_frame(self, text):
        text = self._preprocessing_text(text)

        if (text is None) or text == "":
            return None

        sentence_list = split_by_break(text)
        temp_object_list = [{'index': index, 'text': sentence_list[index]}
                            for index in range(len(sentence_list))]

        return pd.DataFrame(temp_object_list)

    def get_sentences_with_index(self, text, remove_duplicated=True, concat_phrases=True, concat_inverted_phrases=True,
                                 remove_stop_phrases=True, minimum_word_count=0, split_by_semicolon=True):

        df = self._create_sentences_data_frame(text)
        if df is None:
            return None

        pipeline_df_funcions = [self._remove_empty_rows, self._mark_duplicated_text]
        if remove_stop_phrases:
            pipeline_df_funcions.append(self._remove_stop_phrases)
        if self._must_remove_duplicated(remove_duplicated, df['text']):
            pipeline_df_funcions.append(self._remove_duplicates)

        df = self._process_df_pipeline(df, pipeline_df_funcions)

        if df is None:
            return None

        df = self._split_by_punctuation(df, split_by_semicolon)

        if concat_phrases:
            df = self._concat_broken_phrases(df)

            if concat_inverted_phrases:
                df = self._concat_inverted_phrases(df)

        if minimum_word_count > 0:
            df = self._remove_small_phrases(df, minimum_word_count)

        df = self._remove_empty_rows(df)
        df = df.sort_values('index').reset_index(drop=True)
        df['index'] = df.index

        return df

    def get_sentences_with_stanza(self, text):
        if (text is None) or text == "":
            return None

        if self._stanza_model is None:
            stanza.download('pt')

            self._stanza_model = stanza.Pipeline('pt', processors='tokenize')

        text = re.sub("\x0C", "\n", text)
        text = text.replace("\n", " ")

        sentences_result = []

        if text != "":
            doc = self._stanza_model(text)

            sentence_to_add = ""
            for i, sentence_obj in enumerate(doc.sentences):
                sentence = sentence_obj.text

                end_with_abbreviation = self._end_with_abbreviation(sentence.split()[-1])

                if end_with_abbreviation:
                    sentence_to_add = sentence + " "
                else:
                    sentence_to_add = sentence_to_add + sentence

                if not end_with_abbreviation:
                    sentences_result.append(sentence_to_add)
                    sentence_to_add = ""

        return sentences_result

    def _preprocessing_text(self, text):
        if (text is None) or text == "":
            return None
        text = html.unescape(text)
        replace_modules = self._get_models_by_type(ModulesType.REPLACE)
        for module in replace_modules:
            text = module.transform(text)
        return text
