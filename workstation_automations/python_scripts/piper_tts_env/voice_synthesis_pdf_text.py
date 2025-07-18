import wave
import json # Still useful if you need to inspect config, but not strictly needed for PiperVoice.load()
from piper import PiperVoice
from piper import PiperConfig # Still useful for understanding structure, but not needed for load() directly

voice_location = "/home/ethenian/piper_voices/british-cori-high/en_GB-cori-high.onnx"
json_location = "/home/ethenian/piper_voices/british-cori-high/en_GB-cori-high.onnx.json"

# Removed as it's not used in the provided snippet
# voice_dictation_storage = ""

converted_text = "Saying that applications share a single network connection through multiplexing is not much of an explanation. How does the TCP/IP process determine the source and destination application for the contents of an arriving segment? The answer isthrough sockets. Sockets are the combination of IP address and TCP/UDP port number. Hosts use sockets to identify TCP connections and sort out UDP two client sockets as 192.168.10.79:14972 and 192.168.10.70:14973. So the sockets allow simultaneous file transfer sessions to the same client from the same FTP server. If the client sessions were distinguished only by IP address or port number, the server would have no way of uniquely identifying the client FTP process. And the FTP server’s socket address is accessed by all of the FTP client sat the same time without confusion Now consider the server shown in Figure 13.2. Here there is a server that has more than one TCP/IP interface for network access, and thus more than one IP"

def voice_synthesis(text):
    # 1. Load the voice model.
    # PiperVoice.load() is designed to automatically find and load the
    # associated .json configuration file if it's in the same directory
    # and named correctly (e.g., model.onnx and model.onnx.json).
    # You generally do NOT need to load the JSON separately and pass it via syn_config=config
    # unless you are overriding specific runtime synthesis parameters dynamically.
    try:
        voice = PiperVoice.load(voice_location) # Changed to .load_voice for clarity and consistency with newer API examples
    except Exception as e:
        print(f"Error loading Piper voice model from {voice_location}: {e}")
        # Consider adding sys.exit(1) or raising the error further if this is critical
        return # Exit the function if voice loading fails

    # The block below for loading PiperConfig is typically not necessary
    # when you just want to use the default configuration provided with the .onnx model.
    # PiperVoice.load_voice() handles this implicitly.
    # It would only be used if you intend to modify configuration parameters dynamically,
    # e.g., to adjust the speaking rate or noise scale at runtime, and then
    # pass that *modified* config to synthesize_wav.
    # For now, let's keep it minimal and rely on the automatic loading.

    # If you needed to modify config dynamically (e.g., adjust speaking speed):
    # try:
    #     with open(json_location,"r",encoding="utf-8") as config_file:
    #         config_dict = json.load(config_file)
    #     config = PiperConfig.from_dict(config_dict)
    #     config.speaker.noise_scale = 0.6 # Example modification
    # except Exception as e:
    #     print(f"Error loading or parsing Piper config JSON: {e}")
    #     return
    # # Then pass `syn_config=config` to synthesize_wav

    output_filename = "audiobook.wav" # Consistent filename
    try:
        with wave.open(output_filename, "wb") as wavefile:
            # For most cases, you don't need syn_config=config here if you're
            # using the default config loaded with the voice.
            # If you *did* load/modify a config, you'd pass it here.
            # However, the simpler .synthesize_wav(text, wavefile) is often enough.
            voice.synthesize_wav(text, wavefile) # Removed syn_config=config for simplicity
        print(f"Speech synthesized and saved to {output_filename}")
    except Exception as e:
        print(f"Error synthesizing speech or writing to WAV file: {e}")


# Main execution block
if __name__ == "__main__":
    voice_synthesis(converted_text)
