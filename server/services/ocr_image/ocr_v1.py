import json
from pytesseract import image_to_string, Output
import pytesseract
import time
import threading
import random
from spellchecker import SpellChecker
from PIL import Image
from nltk.stem import WordNetLemmatizer, SnowballStemmer
import csv

# lemmatizer = WordNetLemmatizer()
# print(lemmatizer.lemmatize("spoken"))

import re
from .utils import *
from ...databases.mongo_models import *

class ScanText:
    def __init__(self, preprocess=False):
        self.spell = SpellChecker()
        self.limit_shape = 0
        self.lemmatizer = WordNetLemmatizer()
        self.preprocess = preprocess
        self.dic_irregular_verb = dict()

        with open('server/services/ocr_image/most-common-verbs-english.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                for idx in range(1, len(row), 1):
                    if (len(row[idx]) < 2) or (not row[idx][0].isalpha()):
                        continue
                    self.dic_irregular_verb[row[idx]] = row[0].strip()
        # find those words that may be misspelled

    def process_word(self, word):
        rmv_char = '’‘0123456789“”~@#$%^&*()_+{}:"?><,.!/;\'[]\"=`\n'
        word = word.strip()
        word = word.lower()

        for ch in rmv_char:
            word = word.replace(ch, "")
        if len(word) < 3:
            return ""

        if '-' in word:
            return word

        # if self.spell._word_frequency[word] < 1:
        #     misspelled = self.spell.unknown([word])
        #     if word in misspelled:
            #         # print("Wrong : " , word)
        #         word = self.spell.correction(word)
        #         # print("Fix to : ", word)

        if self.spell._word_frequency[word] < 5:
            word = ""
        else:
            word = self.lemmatizer.lemmatize(word)
            if word in self.dic_irregular_verb:
                word = self.dic_irregular_verb[word]
        return word

    def get_text(self, path):
        raw_text = ''

        st = time.time()
        json_text = {}
        # pytesseract.pytesseract.tesseract_cmd = 'pytesseract'
        if check_file(path) == 0:
            print("[INFO] File Image")

            if self.preprocess:
                gray = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
                img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            else:
                img = cv2.imread(path)

            print("Size : ", img.shape)
            max_size = max(img.shape)
            if max_size > self.limit_shape and self.limit_shape:
                scale_ratio = 1.0 * self.limit_shape / max_size
                img = resize_image(img, scale_ratio, scale_ratio)

            print("[INFO] Converting...")
            d = pytesseract.image_to_data(img, output_type=Output.DICT)
            n_boxes = len(d['level'])
            for i in range(n_boxes):
                word = self.process_word(d['text'][i])
                if word == '':
                    continue
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # cv2.rectangle(img, (x, y), (x + w, y + h), (random.randint(0, 150), random.randint(0, 50), random.randint(0, 100)), 2)
                # cv2.putText(img, word,
                #             (x + 8, y + h),
                #             cv2.FONT_HERSHEY_SIMPLEX,
                #             0.7,
                #             (255, 0, 0),
                #             1)

                if word in json_text:
                    json_text[word].append((x, y, w, h))
                else:
                    json_text[word] = []
                    json_text[word].append((x, y, w, h))
            # cv2.imwrite('Text_output___.jpg', img)
            # print(json_text)
            parag_analyse = threading.Thread(target=self.save_sentence_to_dtb, args=(path,), name="Thread-a", daemon=True)
            parag_analyse.start()

            return json.dumps(json_text)

        if check_file(path) == 1:
            print("[INFO] File pdf")
            print("[INFO] Converting...")
            raw_text = pdf2text(path)
            words = raw_text.split(' ')

        if check_file(path) == 2:
            print("[INFO] file doc")
            print("[INFO] Converting...")
            raw_text = doc2text(path)

        print("Process in {}s".format(time.time() - st))
        return raw_text

    def get_paragraph(self, path):
        text = pytesseract.image_to_string(Image.open(path))
        return text

    def save_sentence_to_dtb(self, path):
        parag = pytesseract.image_to_string(Image.open(path), lang='eng')
        parag = parag.replace('’', '')
        parag = parag.replace('”', '')
        parag = parag.replace('\'', '')
        parag = parag.replace('\"', '')
        # re.split('; |, ', str)
        sentences_1 = [sentence for sentence in parag.split('.') if sentence.strip() != '']
        sentences_2 = []
        for sentence1 in sentences_1:
            sentences_2.extend([sentence for sentence in sentence1.split('!') if sentence.strip() != ''])
        sentences_3 = []
        for sentence2 in sentences_2:
            sentences_3.extend([sentence for sentence in sentence2.split('?') if sentence.strip() != ''])
        sentences_4 = []
        for sentence3 in sentences_3:
            sentences_4.extend([sentence for sentence in sentence3.split('\n\n') if sentence.strip() != ''])

        print("______________")
        user = User.objects().get(index=1)

        for idx, sentence in enumerate(sentences_4):
            sentence = sentence.strip()
            if sentence[-1] != '.':
                sentence += '.'

            if len(sentence.split(' ')) > 10:
                user.sentences.append(sentence)
        user.save()
        print("Finish update User.sentences")

# upbkup@up-co.vn