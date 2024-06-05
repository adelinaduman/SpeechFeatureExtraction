
The initial phase — transformation of audio speech into written text, which was achieved through the deployment of the Vosk speech-to-text framework. I downloaded the model from here - https://alphacephei.com/vosk/models. 
Then  I used the following tutorial  https://singerlinks.com/2021/07/how-to-convert-speech-to-text-using-python-and-vosk/ and transcribed mono WAV audio to text. This procedure involved opening the audio file, initializing both the model and recognizer, and processing the audio frames through the recognizer, which subsequently outputs the transcription in JSON format.
Speaking Rate calculated as words per minute

Post-transcription, the speech rate for each audio was manually . This was determined by computing the word count via Python's len() function on the transcribed text and applying the formula: speaking_rate = word_count / duration_minutes. The audio's duration, converted to minutes, was derived from its frame rate and total frames.

Acoustic Features extracted: 
Using Parselmouth, I extracted critical acoustic features – pitch, intensity, jitter, shimmer, and the harmonics-to-noise ratio (HNR)

The final function is a script focused on processing audio files both podcast and my audios, each encapsulating all emotions (e.g., happy, sad, afraid). The process_audio_files function sequentially transcribed the speech using Vosk, computed the speaking rate, and extracted acoustic features.
Upon completion of processing all designated audio files, it the assembles DataFrame which gets converted to a CSV file, msp_features.csv and my_features.csv, showing the script's output 



Transcripts: 


Emotion: Happy
Transcribed Text: we have two eyes in two years and fingernails and i'm like oh my gosh that's so adore
Word Count: 18
Words Per Minute: 245.45

Emotion: Angry
Transcribed Text: this process that i walked this path with her as she came out
Word Count: 13
Words Per Minute: 193.85

Emotion: Sad
Transcribed Text: our producer keith had family issues and then thing just kind of kept on fallen apart
Word Count: 16
Words Per Minute: 130.23

Emotion: Surprised
Transcribed Text: and i'm watching people go wait a minute you mean me doctor carson is
Word Count: 14
Words Per Minute: 186.81


Emotion: Afraid
Transcribed Text: and i i think about about trump if he gets power if he actually gets elected i fear for this country's future i fear for the future of human liberty
Word Count: 30
Words Per Minute: 169.76


Emotion: Disgusted
Transcribed Text: i mean the more politician speak the more i want to turn it off because they're all a bunch of liars and thieves and crooks
Word Count: 25
Words Per Minute: 257.11


Emotion: Neutral
Transcribed Text: wincing more than two hundred footnotes and thirty classic texts
Word Count: 10
Words Per Minute: 174.93
