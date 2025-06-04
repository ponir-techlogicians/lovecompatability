# Stroke dictionary for each letter
import unicodedata

from django.utils.translation import get_language
GLOBAL_STROKE_DICT = {
    'en': {
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3
    },
    'es':{
        'A': 3, 'Á': 4,
        'B': 3,
        'C': 1,
        'D': 2,
        'E': 3, 'É': 4,
        'F': 2,
        'G': 2,
        'H': 3,
        'I': 1, 'Í': 2,
        'J': 2,
        'K': 3,
        'L': 2,
        'M': 4,
        'N': 3, 'Ñ': 4,
        'O': 1, 'Ó': 2,
        'P': 2,
        'Q': 2,
        'R': 3,
        'S': 4,
        'T': 2,
        'U': 3, 'Ú': 4, 'Ü': 3,  # Ü typically adds diaeresis, ~1 extra stroke
        'V': 2,
        'W': 4,
        'X': 2,
        'Y': 3,
        'Z': 3
    },
    'fr':{
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Accented vowels (adds 1 stroke per accent or diacritic)
        'À': 4, 'Â': 4, 'Ä': 4,
        'Ç': 2,  # C with cedilla, ~1 extra stroke
        'É': 4, 'È': 4, 'Ê': 4, 'Ë': 4,
        'Î': 2, 'Ï': 2,
        'Ô': 2, 'Ö': 2,
        'Ù': 4, 'Û': 4, 'Ü': 4,
        'Ÿ': 4,

        # Ligatures
        'Œ': 4
    },
    'de':{
        'A': 3, 'Ä': 4,  # A + umlaut
        'B': 3,
        'C': 1,
        'D': 2,
        'E': 3,
        'F': 2,
        'G': 2,
        'H': 3,
        'I': 1,
        'J': 2,
        'K': 3,
        'L': 2,
        'M': 4,
        'N': 3,
        'O': 1, 'Ö': 2,  # O + umlaut
        'P': 2,
        'Q': 2,
        'R': 3,
        'S': 4,
        'T': 2,
        'U': 3, 'Ü': 4,  # U + umlaut
        'V': 2,
        'W': 4,
        'X': 2,
        'Y': 3,
        'Z': 3,
        'ß': 3  # Eszett (roughly "B-like S", 3 strokes)
    },
    'ru':{
        'А': 3, 'Б': 3, 'В': 3, 'Г': 2, 'Д': 3, 'Е': 3, 'Ё': 4, 'Ж': 4, 'З': 3,
        'И': 3, 'Й': 4, 'К': 3, 'Л': 2, 'М': 4, 'Н': 3, 'О': 1, 'П': 2, 'Р': 2,
        'С': 1, 'Т': 2, 'У': 2, 'Ф': 4, 'Х': 2, 'Ц': 3, 'Ч': 2, 'Ш': 4, 'Щ': 5,
        'Ъ': 3, 'Ы': 3, 'Ь': 2, 'Э': 2, 'Ю': 4, 'Я': 3
    },
    'it':{
        'A': 3, 'À': 4,
        'B': 3,
        'C': 1,
        'D': 2,
        'E': 3, 'È': 4, 'É': 4,
        'F': 2,
        'G': 2,
        'H': 3,
        'I': 1, 'Ì': 2,
        'J': 2,  # foreign
        'K': 3,  # foreign
        'L': 2,
        'M': 4,
        'N': 3,
        'O': 1, 'Ò': 2,
        'P': 2,
        'Q': 2,
        'R': 3,
        'S': 4,
        'T': 2,
        'U': 3, 'Ù': 4,
        'V': 2,
        'W': 4,  # foreign
        'X': 2,  # foreign
        'Y': 3,  # foreign
        'Z': 3
    },
    'sv':{
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Extra Swedish letters
        'Å': 4,  # A + small circle = 3 + 1
        'Ä': 4,  # A + two dots = 3 + 1
        'Ö': 3   # O + two dots = 1 + 2
    },
    'pt':{
        # Basic Latin
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Accented vowels (add ~1 stroke per diacritic)
        'Á': 4, 'À': 4, 'Â': 4, 'Ã': 4,
        'É': 4, 'Ê': 4,
        'Í': 2,
        'Ó': 2, 'Ô': 2, 'Õ': 3,
        'Ú': 4,

        # Cedilla
        'Ç': 2  # C + cedilla
    },
    'nl':{
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3
    },
    'no':{
        # Standard Latin (A–Z)
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Norwegian-specific characters
        'Æ': 4,  # Usually written as A + E ligature (~4 strokes)
        'Ø': 2,  # O with a diagonal stroke (~2 strokes)
        'Å': 4   # A + ring on top (~3 + 1)
    },
    'da':{
        # Standard Latin letters (A–Z)
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Danish-specific characters
        'Æ': 4,  # Ligature of A and E
        'Ø': 2,  # O with a diagonal slash
        'Å': 4   # A with a small circle above
    },
    'cs':{
        # Basic Latin
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Letters with diacritics (add 1 stroke per accent)
        'Á': 4,  # A + acute
        'Č': 2,  # C + caron (háček)
        'Ď': 3,  # D + caron
        'É': 4,
        'Ě': 4,  # E + caron
        'Í': 2,
        'Ň': 4,
        'Ó': 2,
        'Ř': 4,
        'Š': 5,
        'Ť': 3,
        'Ú': 4,
        'Ů': 4,  # U + ring
        'Ý': 4,
        'Ž': 4
    },
    'hu':{
        # Basic Latin letters
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Accented vowels (typically add 1–2 strokes)
        'Á': 4, 'É': 4, 'Í': 2, 'Ó': 2,
        'Ö': 3, 'Ő': 3,
        'Ú': 4, 'Ü': 4, 'Ű': 4,

        # Digraphs as letters (approximated as sum of base components)
        'CS': 5,     # C + S
        'DZ': 4,     # D + Z
        'DZS': 7,    # D + Z + S
        'GY': 5,     # G + Y
        'LY': 5,     # L + Y
        'NY': 6,     # N + Y
        'SZ': 7,     # S + Z
        'TY': 5,     # T + Y
        'ZS': 7      # Z + S
    },
    'fi':{
        # Basic Latin letters
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Finnish-specific letters
        'Å': 4,  # A + small ring above = 3 + 1
        'Ä': 4,  # A + two dots = 3 + 1
        'Ö': 3   # O + two dots = 1 + 2
    },
    'ro':{
        # Latin letters A–Z
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3,

        # Romanian diacritic letters
        'Ă': 4,  # A + breve (curved accent) → 3 + 1
        'Â': 4,  # A + circumflex → 3 + 1
        'Î': 2,  # I + circumflex → 1 + 1
        'Ș': 5,  # S + comma below → 4 + 1
        'Ț': 3   # T + comma below → 2 + 1
    },
    'el':{
        'Α': 3,  # like Latin A
        'Β': 3,  # like Latin B
        'Γ': 2,
        'Δ': 3,
        'Ε': 3,
        'Ζ': 3,
        'Η': 3,
        'Θ': 2,  # O + horizontal line
        'Ι': 1,
        'Κ': 3,
        'Λ': 2,
        'Μ': 4,
        'Ν': 3,
        'Ξ': 3,  # three horizontal lines and a vertical connector
        'Ο': 1,
        'Π': 2,
        'Ρ': 2,
        'Σ': 3,
        'Τ': 2,
        'Υ': 3,
        'Φ': 3,  # O with vertical line
        'Χ': 2,
        'Ψ': 3,
        'Ω': 3
    },
    'pl':{
        # Base Latin letters used in Polish
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'R': 3, 'S': 4, 'T': 2, 'U': 3, 'W': 4, 'Y': 3, 'Z': 3,

        # Diacritic letters (base + 1 stroke)
        'Ą': 4,  # A + tail
        'Ć': 2,  # C + acute
        'Ę': 4,  # E + tail
        'Ł': 3,  # L + diagonal stroke
        'Ń': 4,  # N + acute
        'Ó': 2,  # O + acute
        'Ś': 5,  # S + acute
        'Ź': 4,  # Z + acute
        'Ż': 4   # Z + dot
    },
    'ms':{
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3
    },
    'ko':{
        # Consonants
        'ㄱ': 2, 'ㄴ': 2, 'ㄷ': 3, 'ㄹ': 5, 'ㅁ': 4, 'ㅂ': 4, 'ㅅ': 2,
        'ㅇ': 1, 'ㅈ': 3, 'ㅊ': 4, 'ㅋ': 3, 'ㅌ': 4, 'ㅍ': 4, 'ㅎ': 3,

        # Vowels
        'ㅏ': 2, 'ㅑ': 3, 'ㅓ': 2, 'ㅕ': 3, 'ㅗ': 2, 'ㅛ': 3,
        'ㅜ': 2, 'ㅠ': 3, 'ㅡ': 1, 'ㅣ': 1,

        # Compound Consonants (used in syllables)
        'ㄲ': 4, 'ㄸ': 6, 'ㅃ': 6, 'ㅆ': 4, 'ㅉ': 6,

        # Compound Vowels
        'ㅐ': 3, 'ㅒ': 4, 'ㅔ': 3, 'ㅖ': 4, 'ㅘ': 4, 'ㅙ': 5, 'ㅚ': 3,
        'ㅝ': 4, 'ㅞ': 5, 'ㅟ': 3, 'ㅢ': 2
    },
    'hi':{
        # Vowels
        'अ': 2, 'आ': 3, 'इ': 2, 'ई': 3, 'उ': 2, 'ऊ': 3,
        'ऋ': 4, 'ए': 3, 'ऐ': 4, 'ओ': 3, 'औ': 4, 'अं': 3, 'अः': 3,
        # Consonants
        'क': 2, 'ख': 3, 'ग': 2, 'घ': 3, 'ङ': 2,
        'च': 2, 'छ': 3, 'ज': 2, 'झ': 3, 'ञ': 3,
        'ट': 2, 'ठ': 3, 'ड': 2, 'ढ': 3, 'ण': 3,
        'त': 2, 'थ': 3, 'द': 2, 'ध': 3, 'न': 2,
        'प': 2, 'फ': 3, 'ब': 2, 'भ': 3, 'म': 2,
        'य': 2, 'र': 2, 'ल': 2, 'व': 2,
        'श': 3, 'ष': 3, 'स': 3, 'ह': 3,
        # Matras and Diacritics
        'ा': 1, 'ि': 1, 'ी': 2, 'ु': 1, 'ू': 2, 'े': 1,
        'ै': 2, 'ो': 1, 'ौ': 2, 'ं': 1, 'ः': 1, 'ँ': 1,
        '़': 1, '्': 1
    },
    'ur':{
        'ا': 1, 'ب': 2, 'پ': 3, 'ت': 2, 'ٹ': 3, 'ث': 3,
        'ج': 2, 'چ': 3, 'ح': 2, 'خ': 3,
        'د': 1, 'ڈ': 2, 'ذ': 2, 'ر': 1, 'ڑ': 2, 'ز': 1, 'ژ': 2,
        'س': 3, 'ش': 4, 'ص': 3, 'ض': 4, 'ط': 3, 'ظ': 4,
        'ع': 3, 'غ': 4,
        'ف': 3, 'ق': 3,
        'ک': 2, 'گ': 3, 'ل': 2, 'م': 3, 'ن': 2,
        'و': 1, 'ہ': 2, 'ء': 1, 'ی': 2, 'ے': 2,

        # Optional Urdu-specific signs
        'ٓ': 1,  # Madd
        'ٔ': 1,  # Hamza
        'ً': 1, 'ٌ': 1, 'ٍ': 1  # Tanween (Arabic)
    },
    'ar':{
        'ا': 1, 'ب': 2, 'ت': 2, 'ث': 3,
        'ج': 2, 'ح': 2, 'خ': 3,
        'د': 1, 'ذ': 2, 'ر': 1, 'ز': 2,
        'س': 3, 'ش': 4, 'ص': 3, 'ض': 4,
        'ط': 3, 'ظ': 4, 'ع': 3, 'غ': 4,
        'ف': 3, 'ق': 3,
        'ك': 2, 'ل': 2, 'م': 3, 'ن': 2,
        'ه': 2, 'و': 1, 'ي': 2,

        # Hamza and diacritical components
        'ء': 1, 'أ': 2, 'إ': 2, 'ؤ': 2, 'ئ': 2, 'آ': 3,

        # Optional tashkeel (vowel marks)
        'َ': 1,  # Fatha
        'ِ': 1,  # Kasra
        'ُ': 1,  # Damma
        'ّ': 1,  # Shadda
        'ْ': 1,  # Sukun
        'ً': 1, 'ٍ': 1, 'ٌ': 1  # Tanween
    },
    'id':{
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
        'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
        'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
        'Y': 3, 'Z': 3
    },
    'tr':{
        # Basic Latin letters (Turkish version)
        'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2,
        'H': 3, 'I': 1, 'İ': 2,  # İ has a dot, I does not
        'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1,
        'P': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2,
        'Y': 3, 'Z': 3,

        # Turkish-specific letters with diacritics
        'Ç': 2,  # C + cedilla
        'Ğ': 3,  # G with breve, adds ~1 stroke
        'Ö': 3,  # O + diaeresis
        'Ş': 5,  # S + cedilla
        'Ü': 4   # U + diaeresis
    },
    'th':{  # combine all parts into one dictionary
        # consonants + vowels + marks from above
        'ก': 2, 'ข': 3, 'ฃ': 3, 'ค': 3, 'ฅ': 3, 'ฆ': 4,
        'ง': 2, 'จ': 2, 'ฉ': 3, 'ช': 3, 'ซ': 4, 'ฌ': 5,
        'ญ': 3, 'ฎ': 2, 'ฏ': 2, 'ฐ': 4, 'ฑ': 4, 'ฒ': 5,
        'ณ': 3, 'ด': 2, 'ต': 2, 'ถ': 3, 'ท': 3, 'ธ': 4,
        'น': 2, 'บ': 2, 'ป': 2, 'ผ': 3, 'ฝ': 3, 'พ': 3,
        'ฟ': 3, 'ภ': 4, 'ม': 2, 'ย': 2, 'ร': 2, 'ฤ': 3,
        'ล': 2, 'ฦ': 4, 'ว': 2, 'ศ': 3, 'ษ': 3, 'ส': 3,
        'ห': 3, 'ฬ': 4, 'อ': 2, 'ฮ': 3,
        'ะ': 1, 'า': 1, 'ิ': 1, 'ี': 2, 'ึ': 1, 'ื': 2,
        'ุ': 1, 'ู': 2, 'เ': 1, 'แ': 2, 'โ': 1, 'ใ': 2, 'ไ': 2, 'ำ': 2,
        '่': 1, '้': 1, '๊': 2, '๋': 2, '์': 1, 'ๆ': 2, 'ฯ': 1, 'ฺ': 1, 'ํ': 1
    },
    'vi':{
        'A': 3, 'Ă': 4, 'Â': 4, 'B': 3, 'C': 1, 'D': 2, 'Đ': 3,
        'E': 3, 'Ê': 4, 'G': 2, 'H': 3, 'I': 1, 'K': 3, 'L': 2, 'M': 4,
        'N': 3, 'O': 1, 'Ô': 2, 'Ơ': 2, 'P': 2, 'Q': 2, 'R': 3, 'S': 4,
        'T': 2, 'U': 3, 'Ư': 3, 'V': 2, 'X': 2, 'Y': 3,
        '́': 1, '̀': 1, '̉': 1, '̃': 1, '̣': 1
    },
    'he':{
        'א': 3, 'ב': 2, 'ג': 2, 'ד': 2, 'ה': 3, 'ו': 1, 'ז': 2,
        'ח': 3, 'ט': 4, 'י': 1, 'כ': 2, 'ך': 1, 'ל': 2, 'מ': 3,
        'ם': 2, 'נ': 2, 'ן': 1, 'ס': 3, 'ע': 2, 'פ': 3, 'ף': 2,
        'צ': 3, 'ץ': 2, 'ק': 3, 'ר': 2, 'ש': 3, 'ת': 3
    }

}
stroke_dict = {
    'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
    'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
    'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
    'Y': 3, 'Z': 3
}

def get_strokes_for_word(word: str) -> list:
    """Convert a word into a list of stroke counts for each letter."""
    stroke_dict = GLOBAL_STROKE_DICT.get(get_language())
    if get_language() == 'ko':
        strokes = []
        for char in word.upper():
            if '가' <= char <= '힣':
                jamo = decompose_korean_syllable(char)
                strokes.extend([stroke_dict[j] for j in jamo if j in stroke_dict])
            elif char in stroke_dict:
                strokes.append(stroke_dict[char])
        return strokes
    if get_language() == 'vi':
        word = unicodedata.normalize('NFD', word.upper())

    return [stroke_dict[ch] for ch in word.upper() if ch in stroke_dict]


def interleave_tokens(name1: str, name2: str) -> list:
    """Interleave words from two names, filling missing words with '0'."""
    tokens1 = name1.split()
    tokens2 = name2.split()

    max_len = max(len(tokens1), len(tokens2))
    merged_tokens = []

    for i in range(max_len):
        merged_tokens.append(tokens1[i] if i < len(tokens1) else "0")
        merged_tokens.append(tokens2[i] if i < len(tokens2) else "0")

    return merged_tokens


def adjacency_sum(arr: list) -> list:
    """Reduce the list by summing adjacent numbers until two digits remain."""
    while len(arr) > 2:
        arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
    return arr

def adjacency_sum_steps(arr: list) -> list:
    """Return a list of each step taken during adjacency summing until two digits remain."""
    steps = [arr[:]]  # Store the initial array
    while len(arr) > 2:
        arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
        steps.append(arr[:])
    return steps

def adjacency_sum_steps_fixed(arr: list, total_steps: int = 5) -> list:
    """Return a fixed number of adjacency sum steps (default 5).
    If the result reaches two digits early, repeat the last step."""
    steps = [arr[:]]  # Start with the initial array

    while len(steps) < total_steps:
        if len(arr) <= 2:
            # Repeat the last step if already reduced
            steps.append(arr[:])
        else:
            arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
            steps.append(arr[:])
    return steps


def get_name_compatibility_with_steps(name1: str, name2: str) -> tuple:
    """Calculate compatibility score and return 5 adjacency sum steps."""
    merged_tokens = interleave_tokens(name1, name2)
    stroke_list = [stroke for token in merged_tokens for stroke in get_strokes_for_word(token)]
    steps = adjacency_sum_steps_fixed(stroke_list, total_steps=5)
    final_score = int("".join(map(str, steps[-1])))  # From the last step
    return final_score, steps



def get_name_compatibility(name1: str, name2: str) -> int:
    """Calculate the compatibility score between two names."""
    merged_tokens = interleave_tokens(name1, name2)
    stroke_list = [stroke for token in merged_tokens for stroke in get_strokes_for_word(token)]
    final_two = adjacency_sum(stroke_list)
    return int("".join(map(str, final_two)))


def split_names(name1, name2):
    words1 = name1.split()  # Split name1 into words
    words2 = name2.split()  # Split name2 into words

    merged = []
    max_len = max(len(words1), len(words2))

    # Merge names in an alternating pattern
    for i in range(max_len):
        if i < len(words1):
            merged.append(words1[i])
        if i < len(words2):
            merged.append(words2[i])

    # Ensure the final list has exactly 6 elements, filling with "_"
    while len(merged) < 6:
        merged.append("_")

    return merged[:6]  # Return exactly 6 elements


def decompose_korean_syllable(char):
    """Decompose Korean syllable into Jamo components"""
    CHOSUNG_LIST = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
        'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]
    JUNGSUNG_LIST = [
        'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ',
        'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ',
        'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
        'ㅡ', 'ㅢ', 'ㅣ'
    ]
    JONGSUNG_LIST = [
        '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
        'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
        'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
        'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]

    if '가' <= char <= '힣':
        code = ord(char) - 0xAC00
        cho = CHOSUNG_LIST[code // (21 * 28)]
        jung = JUNGSUNG_LIST[(code % (21 * 28)) // 28]
        jong = JONGSUNG_LIST[code % 28]
        return [cho, jung] + ([jong] if jong else [])
    return [char]


def split_names_safe(name1, name2):
    words1 = name1.split()  # Split name1 into words
    words2 = name2.split()  # Split name2 into words

    merged = []
    max_len = max(len(words1), len(words2))

    # Merge names in an alternating pattern
    for i in range(max_len):
        if i < len(words1):
            merged.append(words1[i])
        if i < len(words2):
            merged.append(words2[i])

    # Ensure the final list has exactly 6 elements, filling with "_"
    if len(merged) <= 4:
        while len(merged) <= 4:
            merged.append("_")
        return merged[:4]
    if len(merged) > 4:
        while len(merged) < 6:
            merged.append("_")
        return merged[:6]

def get_total_stroke(word: str) -> int:
    """Return the total stroke count for a word."""
    # for ch in word.upper():
    #     print(stroke_dict)
    #     print(ch,stroke_dict.get(ch, 0))
        
    stroke_dict = GLOBAL_STROKE_DICT.get(get_language())
    if get_language() == 'ko':
        total = 0
        for char in word.upper():
            if '가' <= char <= '힣':
                jamo = decompose_korean_syllable(char)
                total += sum(stroke_dict.get(j, 0) for j in jamo)
            else:
                total += stroke_dict.get(char, 0)
        return total
    for ch in word.upper():
        if ch in stroke_dict:
            print(ch,stroke_dict[ch])
    return sum(stroke_dict.get(ch, 0) for ch in word.upper())


def split_names_into_6(name1: str, name2: str) -> list:
    """Split both names and interleave up to 3 parts each to get 6 tokens."""
    parts1 = name1.split()
    parts2 = name2.split()

    merged = []
    for i in range(3):
        if i < len(parts1):
            merged.append(parts1[i])
        else:
            merged.append("_")
        if i < len(parts2):
            merged.append(parts2[i])
        else:
            merged.append("_")
    return merged

def split_names_into_4(name1: str, name2: str) -> list:
    """Split both names and interleave up to 3 parts each to get 6 tokens."""
    parts1 = name1.split()
    parts2 = name2.split()

    merged = []
    for i in range(2):
        if i < len(parts1):
            merged.append(parts1[i])
        else:
            merged.append("_")
        if i < len(parts2):
            merged.append(parts2[i])
        else:
            merged.append("_")
    return merged


def get_number_of_split(name1: str, name2: str) -> int:
    """Return the number of times the names are split into 6 tokens."""
    parts1 = name1.split()
    parts2 = name2.split()
    merged = []
    for i in range(3):
        if i < len(parts1):
            merged.append(parts1[i])
        if i < len(parts2):
            merged.append(parts2[i])

    return merged

def adjacency_sum_steps_fixed_5(arr: list) -> list:
    """Return 5 steps of adjacency summing (even if 2 elements reached early)."""
    steps = [arr[:]]
    while len(steps) < 5:
        if len(arr) <= 2:
            steps.append(arr[:])
        else:
            arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
            steps.append(arr[:])
    return steps

def adjacency_sum_steps_fixed_3(arr: list) -> list:
    """Return 5 steps of adjacency summing (even if 2 elements reached early)."""
    steps = [arr[:]]
    while len(steps) < 3:
        if len(arr) <= 2:
            steps.append(arr[:])
        else:
            arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
            steps.append(arr[:])
    return steps

def get_name_compatibility_with_5steps(name1: str, name2: str) -> tuple:
    """Get compatibility score with 5 steps starting from 6 tokens."""
    #set_current_language()
    splits = get_number_of_split(name1, name2)
    if len(splits) > 4:
        six_parts = split_names_into_6(name1, name2)
        initial_strokes = [get_total_stroke(word) for word in six_parts]
        steps = adjacency_sum_steps_fixed_5(initial_strokes)
        final_score = int("".join(map(str, steps[-1])))
        return final_score, steps
    else:
        four_parts = split_names_into_4(name1, name2)
        initial_strokes = [get_total_stroke(word) for word in four_parts]
        steps = adjacency_sum_steps_fixed_3(initial_strokes)
        final_score = int("".join(map(str, steps[-1])))
        return final_score, steps
