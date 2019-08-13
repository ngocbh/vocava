import json
from pytesseract import image_to_string, Output
import pytesseract
import time
import random
from spellchecker import SpellChecker
from .utils import *
from PIL import Image

class ScanText:
    def __init__(self):
        self.spell = SpellChecker()
        self.limit_shape = 0
        # find those words that may be misspelled

    def process_word(self, word):
        rmv_char = '0123456789“”~@#$%^&*()_+{}:"?><,./;\'[]\"=`\n'
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
        return word

    def get_text(self, path):
        raw_text = ''

        st = time.time()
        json_text = {}
        # pytesseract.pytesseract.tesseract_cmd = 'pytesseract'
        if check_file(path) == 0:
            print("[INFO] File Image")
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
                cv2.rectangle(img, (x, y), (x + w, y + h), (random.randint(0, 150), random.randint(0, 50), random.randint(0, 100)), 2)
                cv2.putText(img, word,
                            (x + 8, y + h),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 0, 0),
                            1)

                if word in json_text:
                    json_text[word].append((x, y, w, h))
                else:
                    json_text[word] = []
                    json_text[word].append((x, y, w, h))
            cv2.imwrite('Text_output___.jpg', img)
            # print(json_text)
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

