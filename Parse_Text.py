import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load('en_core_web_sm')

# This will take the on screen text and get the usable information
def parse_onscreen_text():

    # Text phrase to test on
    text = 'This Stock is Going Parabolic 🔥🚀🙌 Sundial Growers $SNDL •Up nearly 100% today•Up nearly 200% weekly' \
           'New Company Hitting the Stock Market... $NGAC $2 Billion Deal Class 6-8 EV Trucks ✅ Proprietary Battery ✅' \
           'UPS  HINO Loomis Dickenson #1 Trading Community Recent MJ announcements have sent this industry flying- now ' \
           'backed by WSB. Can see $SNDL hitting $4.20 easily (seriously). All of these hype stocks are gambles so invest at your own risk 🔥'


    # Create the doc from the text phrase
    doc = nlp(text)

    for entity in doc.ents:

        if entity.label_ == 'ORG' or entity.label_ == 'MONEY':
            print(entity.text)



parse_onscreen_text()