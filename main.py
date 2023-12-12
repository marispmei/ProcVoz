from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import speech_recognition as sr
import os
import spacy
from googletrans import Translator

def speak(text, lang, name):
    tts = gTTS(text=text, lang=lang)
    filename = name + ".mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_audio():
    r = sr.Recognizer()
    
    max_attempts = 3

    for _ in range(max_attempts):
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5)
                said = r.recognize_google(audio, language='pt-BR')
                print("Você disse:", said)
                return said
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio. Tente novamente.")
        except sr.RequestError as e:
            print(f"Erro na solicitação ao serviço de reconhecimento de fala: {e}")
            print("Verifique sua conexão com a Internet ou tente novamente mais tarde.")

    print("Falha nas tentativas de reconhecimento de fala. Encerrando o programa.")
    return ""

def extract_entities(text, lang):
    if lang == 'en':
        nlp = spacy.load('en_core_web_sm')
    elif lang == 'pt':
        nlp = spacy.load('pt_core_news_sm')
    else:
        print(f"Modelo SpaCy não suportado para o idioma {lang}")

    doc = nlp(text)
    entities = [ent.text for ent in doc if ent.ent_type_]
    return entities

def generate_contextual_response(entities, lang):
    # Adicione lógica para gerar uma resposta contextual com base nas entidades identificadas
    # Aqui, estamos apenas imprimindo as entidades reconhecidas
    print("Entidades identificadas:", entities)
    response = "Eu ouvi algo interessante!"
    return response

def translate_and_interact(text, source_lang, target_lang):
    translator = Translator()
    
    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        translated_text = translation.text
        print("Traduzido para {}: {}".format(target_lang, translated_text))
        
        if not translated_text:
            print("A tradução falhou ou o texto traduzido está vazio.")
            return None, target_lang

        # Extraia entidades do texto original
        entities = extract_entities(text, source_lang)

        # Gere uma resposta contextual com base nas entidades identificadas
        response = generate_contextual_response(entities, source_lang)
        print("Resposta contextual:", response)

        return translated_text, target_lang

    except Exception as e:
        print("Erro durante a tradução:", str(e))
        return None, target_lang


language_to_translate = "en"
linguas = {"en": "pt", "pt": "en"}

i = 0
while True:
    print("Fale em:", linguas[language_to_translate])
    spoken_text = get_audio()
    
    translated_text, language_to_translate = translate_and_interact(spoken_text, linguas[language_to_translate], language_to_translate)
    
    filename = "voice" + str(i)
    speak(translated_text, language_to_translate, filename)
    
    # Atualize o idioma para o próximo ciclo
    language_to_translate = linguas[language_to_translate]
    i += 1

