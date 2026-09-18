from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests


def translate_text(text, language):

    if not text or not text.strip():
        return ""

    segment_length = 1000

    segments = [
        text[i:i + segment_length]
        for i in range(0, len(text), segment_length)
    ]

    translations = []

    # Cria o tradutor apenas uma vez
    translator = GoogleTranslator(
        source="auto",
        target=language
    )

    for segment in segments:

        try:

            translation = translator.translate(
                segment
            )

            translations.append(
                translation
            )

        except TooManyRequests:

            print(
                "GoogleTranslator: limite de requisições atingido."
            )

            raise

        except Exception as e:

            print(
                f"Erro durante a tradução: {e}"
            )

            raise

    full_translation = " ".join(
        translations
    )

    return full_translation
