# SpeechFeatureExtraction
 This project focuses on the extraction and analysis of features from emotional speech. It involves recording and analyzing self-produced emotional speech as well as samples from the MSP-Podcast corpus. The primary goal is to extract various speech features such as pitch, intensity, speaking rate, jitter, shimmer, and Harmonics-to-Noise Ratio (HNR) using Praat software and the Parselmouth Python library.


# Methodologies
Feature Extraction
The features are extracted using Praat software commands through the Parselmouth library in Python. The following methodologies were used:
Pitch Extraction
Set pitch floor to 75Hz and pitch ceiling to 600Hz.
Jitter Extraction
Extracted local jitter with period floor of 0.0001s, period ceiling of 0.02s, and maximum period factor of 1.3.
Shimmer Extraction
Extracted local shimmer with period floor of 0.0001s, period ceiling of 0.02s, maximum period factor of 1.3, and maximum amplitude factor of 1.6.
Intensity Extraction
Set pitch floor to 100Hz and used the 'energy' averaging method to get mean intensity.
HNR Calculation
Extracted harmonicity (cc) with time step of 0.01, minimum pitch of 75Hz, silence threshold of 0.1, and number of periods per window to 1.0.
Speaking Rate
Approximated with #words/duration.

# Speech Recording
Recorded emotional speech (one sentence each) in a quiet room using a headset with a microphone. Trimmed leading and trailing silence. Emotions recorded: Happy, Angry, Sad, Afraid, Surprised, Disgusted, Neutral.

# Tech Stack
- Python
- Praat
- Parselmouth
  
# File Structure
- msp_features.csv: Feature values from MSP-Podcast corpus samples.
- my_features.csv: Feature values from self-recorded emotional speech.
- feature_extraction.py: Python script for feature extraction.
- responses.txt: Responses to the analysis questions.
- recordings: Folder containing the recorded emotional speech files (happy.wav, angry.wav, sad.wav, etc.).
- README.md: This file, explaining how to run the script and references.

# Running the Script
1) Ensure you have Praat and Parselmouth installed.
2) Place your recordings in the recordings folder.
3) Run the feature_extraction.py script to extract features and print them to my_features.csv and msp_features.csv.

# Example Command
bash
Copy code
python feature_extraction.py

# References
Praat Software: Praat
Parselmouth Library: Parselmouth
