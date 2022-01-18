
import streamlit as st
import translate
import sentiment
import synthesize

# App Config
st.set_page_config(page_title='Azure Cognitive Services Demo', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# Statefulness    
states = {
    'language_index':18,
    'input_text':'',
    'translation_show_results':False,
    'translation_response':'',
    'translation_text':'',
    'sentiment_response':'',
    'sentiment_score':'',
    'sentiment_result':'',
    'synthesize_source_audio_response':'',
    'synthesize_target_audio_response':'',
    'synthesize_show_results':False
}

for k, v in states.items():
    if k not in st.session_state:
        st.session_state[k] = v


def load_sample_callback(sample):
    if sample == 'en-tr':
        st.session_state.input_text = 'Hello, i created this demonstration to show you how this service works.'
        st.session_state.language_index = 18
    elif sample == 'tr-en':
        st.session_state.input_text = 'Merhaba, ben bu gosteriyi size bu servisin nasil calistigini gostermek icin yarattim.'
        st.session_state.language_index = 5

st.button("Load English-Turkish Sample", on_click=load_sample_callback, args=('en-tr',))
st.button("Load Turkish-English Sample", on_click=load_sample_callback, args=('tr-en',))


def translate_callback():
    st.session_state.translation_response = translate.get_translation(st.session_state.translation_input, st.session_state.translation_language)        
    st.session_state.translation_text = st.session_state.translation_response[0]['translations'][0]['text']
    
    st.session_state.sentiment_response = sentiment.get_sentiment(st.session_state.translation_text, st.session_state.translation_language)
    st.session_state.sentiment_score = st.session_state.sentiment_response['documents'][0]['score']
    st.session_state.sentiment_result = 'Positive' if st.session_state.sentiment_score > 0.666 else 'Negative' if st.session_state.sentiment_score < 0.333 else 'Neutral'   

    st.session_state.translation_show_results = True
    st.session_state.synthesize_show_results = False


st.header('Translate')

language_options = {
    'ar':'Arabic',
    'ca':'Catalan',
    'zh-Hans':'Chinese (Simplified)',
    'zh-Hant':'Chinese (Traditional)',
    'hr':'Croatian',
    'en':'English',
    'fr':'French',
    'de':'German',
    'el':'Greek',
    'he':'Hebrew',
    'hi':'Hindi',
    'it':'Italian',
    'ja':'Japanese',
    'ko':'Korean',
    'pt':'Portuguese',
    'ru':'Russian',
    'es':'Spanish',
    'th':'Thai',
    'tr':'Turkish',
    'vi':'Vietnamese'
}
    

col1, col2 = st.columns(2)

input_text = col1.text_area('Translate:', key="translation_input", value=st.session_state.input_text, height=250)
col1.selectbox('Target Language:', key="translation_language", options=language_options.keys(), index=st.session_state.language_index, format_func=lambda x: language_options[x])
col2.text_area('Translation:', key="translation_result", value=st.session_state.translation_text, disabled=True, height=250)
col2.write('Sentiment:')
col2.write(f'{st.session_state.sentiment_result} ({st.session_state.sentiment_score})')
# col2.write()
st.button('Translate', on_click=translate_callback)

    
if st.session_state.translation_show_results:
    translate_result_col1, translate_result_col2 = st.columns(2)
    translate_result_col1.subheader('Translate API Response:')
    translate_result_col1.json(st.session_state.translation_response)

    translate_result_col2.subheader('Sentiment API Response:')
    translate_result_col2.write(st.session_state.sentiment_response)    
    

voice_options = {
    "(en-AU, NatashaNeural)":"en-AU Female NatashaNeural)",
    "(en-AU, WilliamNeural)":"en-AU Male WilliamNeural)",
    "(tr-TR, EmelNeural)":"tr-TR Female Emel Neural",
    "(tr-TR, AhmetNeural)":"tr-TR Male Ahmet Neural",
}

def synthesize_callback():
    tts = synthesize.TextToSpeech(st.session_state.translation_input, st.session_state.synthesize_source_voice)
    tts.get_token()
    st.session_state.synthesize_source_audio_response = tts.save_audio()
    
    tts = synthesize.TextToSpeech(st.session_state.translation_text, st.session_state.synthesize_target_voice)
    tts.get_token()
    st.session_state.synthesize_target_audio_response = tts.save_audio()
    
    st.session_state.synthesize_show_results=True


st.header('Synthesize')
synthesize_col1, synthesize_col2 = st.columns(2)
synthesize_col1.selectbox('Source Language Voice', key="synthesize_source_voice", options=voice_options.keys(), index=1, format_func=lambda x: voice_options[x])
synthesize_col2.selectbox('Target Language Voice', key="synthesize_target_voice", options=voice_options.keys(), index=3, format_func=lambda x: voice_options[x])

st.button('Synthesize', on_click=synthesize_callback)

if st.session_state.synthesize_show_results:
    synthesize_col1.audio(st.session_state.synthesize_source_audio_response)
    synthesize_col2.audio(st.session_state.synthesize_target_audio_response)