import sys
import os
import json

import cv2
import pytesseract
from pytesseract import Output
from pandas import DataFrame
from numpy import dtype

def extract_data(image_path):
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSARACT_PATH")
    print("[INFO] loading image...")
    img = cv2.imread(image_path)

    print("[INFO] processing image...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()
    # out = DataFrame(
    #     index=["level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"], 
    #     columns=["level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"],
    #     dtype=["int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "object"]
    #     )

    # out = DataFrame({
    #     "level": dtype("int64"),
    #     "page_num": dtype("int64"),
    #     "block_num": dtype("int64"),
    #     "par_num": dtype("int64"),
    #     "line_num": dtype("int64"),
    #     "word_num": dtype("int64"),
    #     "left": dtype("int64"),
    #     "top": dtype("int64"),
    #     "width": dtype("int64"),
    #     "height": dtype("int64"),
    #     "conf": dtype("int64"),
    #     "text": dtype("object"),
    # })
    out = DataFrame()
    for idx, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)

        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cropped = im2[y:y + h, x:x + w]

        print("[INFO] reading text...")
        text = pytesseract.image_to_data(
            cropped, output_type=Output.DATAFRAME, pandas_config={"keep_default_na": False, "skip_blank_lines": True})

        if (out.empty):
            out = DataFrame(text)
        else:
            out.append(text)
    return out

