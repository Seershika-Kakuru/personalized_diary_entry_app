import webbrowser
from datetime import datetime
import cv2
import streamlit as st
from fpdf import FPDF
from pypdf import PdfReader
import re


def add_empty_lines(num):
    for i in range(num):
        st.write("\n")


def add_time_stamp_to_frame(numpy_frame, frame_name):
    current_day = datetime.now().strftime(f"%B %d, %Y")
    current_day_in_week = datetime.now().strftime("%A, %X")
    cv2.putText(img=numpy_frame,
                text=current_day_in_week,
                org=(420, 440),
                fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                fontScale=1,
                color=(233,150,122),
                thickness=1,
                lineType=cv2.LINE_AA)
    cv2.putText(img=numpy_frame,
                text=current_day,
                org=(420, 460),
                fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                fontScale=1,
                color=(233,150,122),
                thickness=1,
                lineType=cv2.LINE_AA)


def latex_format(string, format="normalsize"):
    return '${\\' + format + '\\textbf{\\textit{' + string + '}}}$'

def subheader_format(string):
    return '<h2 align = "center" style=color:Pink;' \
           'font-family:Georgia;font-size:20px;' \
           'font-style:italic;>' \
           '<u style="text-decoration-color:Plum;">' \
           f'{string}</u></h2>'


def add_copied_and_new_content_to_pdf(filename, image_name, diary_entry, name_of_person):
    pdf_instance = FPDF(orientation='P', unit='mm', format='A4')

    # create a pdf reader
    reader = PdfReader(filename)

    # create list of all images and create a text string
    images_list = []
    text = ''

    # for each page in the reader
    for page in reader.pages:
        # extract text in page and append to the text string
        text += page.extract_text()
        for image in page.images:
            with open(image.name, "wb") as fp:
                fp.write(image.data)
                images_list.append(image.name)

    individual_texts = text.split("DAY")
    individual_texts = individual_texts[1:]
    individual_texts = ["DAY " + text for text in individual_texts]
    last_index = 0
    for index, text in enumerate(individual_texts):
        last_index += 1
        curr_image = images_list[index]
        before_dear_diary, after_dear_diary = text.split('Dear Diary,')
        results = re.split(r"DAY\s+[0-9]", before_dear_diary)
        pdf_instance.add_page()
        pdf_instance.set_font(family="Courier", style="B", size=12)
        pdf_instance.set_text_color(220, 20, 60)
        pdf_instance.set_fill_color(253, 223, 223)
        pdf_instance.cell(0, 5, f"DAY {last_index}", True, 1, 'C', True)
        pdf_instance.ln(10)
        pdf_instance.set_font(family="Courier", style="I", size=12)
        pdf_instance.set_text_color(76, 187, 23)
        pdf_instance.multi_cell(0, 5, results[1].strip().encode('utf-8').decode('latin-1'))
        pdf_instance.ln(10)
        pdf_instance.image(curr_image, x=60, w=100, h=100)
        pdf_instance.ln(10)
        pdf_instance.set_font(family="Courier", style="I", size=12)
        pdf_instance.set_text_color(252, 106, 3)
        pdf_instance.multi_cell(0, 5, str('Dear Diary,').encode('utf-8').decode('latin-1'))
        pdf_instance.ln(10)
        content, name = after_dear_diary.split("Yours,")
        pdf_instance.set_font(family="Courier", style="I", size=12)
        pdf_instance.set_text_color(252, 106, 3)
        pdf_instance.multi_cell(0, 5, content.strip().encode('utf-8').decode('latin-1'))
        pdf_instance.ln(10)
        pdf_instance.set_font(family="Courier", style="I", size=12)
        pdf_instance.set_text_color(252, 106, 3)
        pdf_instance.multi_cell(0, 5, str("Yours,\n").strip().encode('utf-8').decode('latin-1'))
        pdf_instance.set_font(family="Courier", style="I", size=12)
        pdf_instance.set_text_color(252, 106, 3)
        pdf_instance.multi_cell(0, 5, name.strip().encode('utf-8').decode('latin-1'))
        pdf_instance.ln(10)
    add_new_content(pdf_instance, last_index + 1, image_name, diary_entry, name_of_person)
    pdf_instance.output(filename)


def write_time():
    date = datetime.now().strftime(f"%dth %b, %Y")
    day = datetime.now().strftime("%A")
    time = datetime.now().strftime("%H:%M %p")
    return date + "\n" + day + "\n" + time + "\n"


def add_first_content_to_pdf(filename, image_name, diary_entry, name_of_person):
    pdf_instance = FPDF(orientation='P', unit='mm', format='A4')
    pdf_instance.add_page()
    pdf_instance.set_fill_color(253, 223, 223)
    pdf_instance.set_font(family="Courier", style="B", size=12)
    pdf_instance.set_text_color(220, 20, 60)
    pdf_instance.cell(0, 5, 'DAY 1', True, 1, 'C', True)
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(76, 187, 23)
    pdf_instance.multi_cell(0, 5, write_time().encode('utf-8').decode('latin-1'))
    pdf_instance.ln(10)
    if image_name:
        pdf_instance.image(image_name, x=60, w=100, h=100)
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(252, 106, 3)
    pdf_instance.multi_cell(0, 5, str('Dear Diary,\n').encode('utf-8').decode('latin-1'))
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(252, 106, 3)
    pdf_instance.multi_cell(0, 5, diary_entry.strip().encode('utf-8').decode('latin-1'))
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(252, 106, 3)
    pdf_instance.multi_cell(0, 5, str("Yours,\n" + name_of_person.title() + ".").encode('utf-8').decode('latin-1'))
    pdf_instance.output(filename)


def add_new_content(pdf_instance, day_number, image_name, diary_entry, name_of_person):
    pdf_instance.add_page()
    pdf_instance.set_font(family="Courier", style="B", size=12)
    pdf_instance.set_text_color(220, 20, 60)
    pdf_instance.set_fill_color(253, 223, 223)
    pdf_instance.cell(0, 5, f'DAY {day_number}', True, 1, 'C', True)
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(76, 187, 23)
    pdf_instance.multi_cell(0, 5, write_time().encode('utf-8').decode('latin-1'))
    pdf_instance.ln(10)
    if image_name:
        pdf_instance.image(image_name, x=60, w=100, h=100)
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(252, 106, 3)
    pdf_instance.multi_cell(0, 5, str('Dear Diary,\n').encode('utf-8').decode('latin-1'))
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(252, 106, 3)
    pdf_instance.multi_cell(0, 5, diary_entry.strip().encode('utf-8').decode('latin-1'))
    pdf_instance.ln(10)
    pdf_instance.set_font(family="Courier", style="I", size=12)
    pdf_instance.set_text_color(252, 106, 3)
    pdf_instance.multi_cell(0, 5, str("Yours,\n" + name_of_person.title() + ".").encode('utf-8').decode('latin-1'))


if __name__ == "__main__":
    add_first_content_to_pdf('ap.png', '''A flower, sometimes known as a bloom or blossom, is the reproductive structure found in flowering plants (plants of the division Angiospermae). Flowers produce gametophytes, which in flowering plants consist of a few haploid cells which produce gametes. The "male" gametophyte, which produces non-motile sperm, is enclosed within pollen grains; the "female" gametophyte is contained within the ovule. When pollen from the anther of a flower is deposited on the stigma, this is called pollination. Some flowers may self-pollinate, producing seed using pollen from the same flower or a different flower of the same plant, but others have mechanisms to prevent self-pollination and rely on cross-pollination, when pollen is transferred from the anther of one flower to the stigma of another flower on a different individual of the same species.

Self-pollination happens in flowers where the stamen and carpel mature at the same time, and are positioned so that the pollen can land on the flower's stigma. This pollination does not require an investment from the plant to provide nectar and pollen as food for pollinators.[1]

Some flowers produce diaspores without fertilization (parthenocarpy). Flowers contain sporangia and are the site where gametophytes develop.''', "chinnu")
    add_copied_and_new_content_to_pdf('bn.png', "Hello", "chinnu")
    add_copied_and_new_content_to_pdf('bn.png', 'Bye', 'Lucky')
