import streamlit as st
import cv2
import os
from helper_functions import add_empty_lines, \
    add_time_stamp_to_frame, latex_format, subheader_format, \
    add_first_content_to_pdf, add_copied_and_new_content_to_pdf
from datetime import datetime
import webbrowser

# writing the heading
st.write('<h1 style = '
         '"background-color:MistyRose;'
         'color:SaddleBrown;'
         'text-align:center;'
         'font-family:Garamond;'
         'font-size:40px;'
         'font-style:italic;">'
         'Dairy Entry of the Day</h1>', unsafe_allow_html=True)

# adding two empty lines
add_empty_lines(2)

# =======================================================
# SECTION 01: INPUTTING AN IMAGE

# Divider and subheading
st.markdown("***")
st.write(subheader_format('Selecting an Image for the Day'),
         unsafe_allow_html=True)

# Creating an expander for uploading an image
with st.expander(latex_format("Upload an Image:")):
    # Upload an image
    uploaded_image = st.file_uploader(label="Upload an Image", label_visibility="hidden")
    # If an image is uploaded, then download the image
    if uploaded_image:
        # creating a file and then writing the image bytes into that file
        with open(os.path.join("", uploaded_image.name), "wb") as f:
            f.write(uploaded_image.getbuffer())

# OR
st.markdown('<p align="center" style="font-size:120%;font-family:Lucinda;"><i><b>[OR]</b></i></p>',
            unsafe_allow_html=True)

# Creating an expander for taking a picture
with st.expander(latex_format('Take a picture: ')):
        st.write(":red[" +
                 latex_format('Instructions: Click on the enter key to take a picture!', 'footnotesize')
                 + "]")
        button = st.button(":blue[" + latex_format("Start the Camera", 'footnotesize') + "]")
        if button:
            # Creating a video capture object (turn on camera)
            video = cv2.VideoCapture(0)
            # Creating a window
            frame_name = "Video Capture"
            cv2.namedWindow(frame_name)
            # Continuously reading frames
            while True:
                # read the current frame
                check, frame = video.read()
                # adding time stamp to frame
                add_time_stamp_to_frame(frame, frame_name)
                # show the frame
                cv2.imshow(frame_name, frame)
                # create a wait key for exiting
                key = cv2.waitKey(1)
                # exit when enter key is pressed or the window is closed
                if key == 13 or cv2.getWindowProperty(frame_name, cv2.WND_PROP_VISIBLE) <= 0:
                    if key == 13:
                        current_day = datetime.now().strftime(f"%B-%d-%Y")
                        # when enter key is pressed save the current frame
                        cv2.imwrite("today_image_" + current_day + '.jpg', frame)
                    break
            # destroy all windows and turn off the window
            cv2.destroyAllWindows()
            video.release()


        # Display the image
        current_day = datetime.now().strftime(f"%B-%d-%Y")
        if os.path.exists("today_image_" + current_day + '.jpg'):
            st.write(":green[" + latex_format("Last Image Taken:", 'footnotesize') + "]")
            st.image("today_image_" + current_day + '.jpg')
            st.info("If not satisfied with the image, take another picture.")

# =======================================================
# SECTION 02: INPUTTING DIARY ENTRY

st.markdown('***')
st.write(subheader_format('Thoughts for the Day:'), unsafe_allow_html=True)
text_input = st.text_area(latex_format('Diary Entry: '))

# =======================================================
# SECTION 03: FILE SELECTION AND PDF CREATION

st.markdown('***')
st.write(subheader_format('Obtain PDF Diary:'), unsafe_allow_html=True)
name = st.text_input(latex_format("Provide your name to find your file:"))
add_entry_button = st.button(latex_format("Add Entry",'footnotesize'))
see_pdf_button = st.button(latex_format("See diary entries so far", 'footnotesize'))

filename = name + '.pdf'

if see_pdf_button:
    if os.path.exists(filename):
        webbrowser.open_new(filename)
        st.info("If you are not seeing earlier diary entries, "
                "try to sign in with another name and apply your diary entry")
    else:
        st.warning('No pdf on your name, '
                   'please try another name or '
                   'provide a diary entry so that a fresh diary can be created for you')
if add_entry_button:
    # if the diary input is also provided
    if text_input != "":
        current_day = datetime.now().strftime(f"%B-%d-%Y")
        # Getting the image provided(if there is an image)
        image_name = None
        if uploaded_image:
            image_name = uploaded_image.name
        elif os.path.exists("today_image_" + current_day + '.jpg'):
            image_name = "today_image_" + current_day + '.jpg'
        else:
            st.warning("Enter an image!")

        if image_name:
            if not os.path.exists(filename):
                add_first_content_to_pdf(filename, image_name, text_input, name)
            else:
                # add the content of updated diary to the selected pdf
                add_copied_and_new_content_to_pdf(filename, image_name, text_input, name)
    else:
        # if no diary content is provided
        st.warning("Please give your diary entry for the day!")



