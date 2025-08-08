# A dict mapping moods to a list of sticker filenames
import random
mood_stickers = {
    "happy": ["pic1.png", "pic4.png"],
    "tired": ["pic3.png"],
    "stressed": ["pic2.png", "pic4.png"],
    "neutral": ["pic2.png"]
}

import random

def get_sticker_for_mood(mood):
    return random.choice(mood_stickers.get(mood, []))