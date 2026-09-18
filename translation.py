import os

from google.cloud import translate_v2 as translate


def translate_text(text, language):

    if not text or not text.strip():
        return ""

    # Cria o cliente da API do Google Cloud
    client = translate.Client()

    result = client.translate(
        text,
        target_language=language
    )

    return result["translatedText"]
