from pocketsphinx import LiveSpeech

 
speech = LiveSpeech(keyphrase='start recording', kws_threshold=1e-200)

for phrase in speech:
    print(phrase.segments(detailed=True))
