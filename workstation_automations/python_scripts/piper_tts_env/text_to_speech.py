import os
import wave 
import json
from piper import PiperVoice
from piper import PiperConfig
from PyPDF2 import PdfReader


# file directories listing
voice_location = "/home/ethenian/piper_voices/british-cori-high/en_GB-cori-high.onnx"
json_location = "/home/ethenian/piper_voices/british-cori-high/en_GB-cori-high.onnx.json"
synthesised_dictation_storage = "/home/ethenian/voiced_pdf_text_audiobooks"



# converts pdf to text and has various customs such as starting page, ending page for selective text output
def pdf_convertion_to_text(file_path):
    start_page = input('Enter the starting page: ')
    end_page = input('Enter the ending page: ')
    current_page = 0
    accumulated_converted_pdf_text = ""
    
    reader = PdfReader('/home/ethenian/'+ file_path)
    while current_page < int(end_page):
        if current_page == 0:
            current_page = int(start_page)
    
        page = reader.pages[current_page]
        accumulated_converted_pdf_text += page.extract_text()
        current_page += 1

    return accumulated_converted_pdf_text 


# Voice synthesis of presented input as text
def voice_synthesis(text,audio_name,group_name):
    synthesised_audio_name = f"{audio_name}.wav"
    path_to_place_synthesised_audio = f"{synthesised_dictation_storage}/{group_name}/{synthesised_audio_name}"
   


    # check if directories in path_to place_synthesised_audio exists if not make it
    directory_path = os.path.dirname(path_to_place_synthesised_audio)
    
    if directory_path:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Ensured directory {directory_path} exists")

    else:
        print(f"Directory {directory_path} already exists and we'll use that")



    #Load the downloaded voice from its location
    try:
        voice = PiperVoice.load(voice_location)
    except Exception as e:
        print(f"Error loading Piper voice model from : {voice_location} : {e}")
        return 

    #customize the voice_synthesized
    #with open(json_location,"r",encoding="utf-8") as config_file:
    #    config_dict = json.load(config_file)
    #    config = PiperConfig.from_dict(config_dict)


    # Write the synthesized text to audio
    try:
        with wave.open(path_to_place_synthesised_audio,"wb") as wavefile:
            voice.synthesize_wav(text, wavefile) #syn_config=config
            print("Speech synthesised")
    except Exception as e:
        print(f"Error synthesising speech or writing to WAV file: {e}")




# Main function orchestrating everything
def main():

    # various inputs for customized synthesised voice
    file_type = input("Propensity of file, Type 1 for pdf file OR Type 2 for text file: ")
    file = input("File path continue from this /home/ethenian/: ")
    audio_name = input("What should this created audio file be called? ")
    group_placement = input("Which group in the voice dictation directory should this be placed ?")
    #voice_speed = input("What speed would you like cori to have less is more: ")

    try:

        if int(file_type) == 1:
            text_extracted = pdf_convertion_to_text(file)
            voice_synthesis(text_extracted,audio_name,group_placement)

        elif int(file_type) == 2:
            with open(file_type, "r") as textfile_txt:
                voice_synthesis(textfile_txt,audio_name,group_placement)

        else:
            print(f"Invalid selection :{file_type}")
            print("Try Again")
            main(file_type, file)

    except Exception as e:
        print(f"Error in main component : {e}")


main()

