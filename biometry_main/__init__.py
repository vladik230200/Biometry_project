import os
from web_biometry import settings

if not os.path.exists(settings.VOICE_FILES): os.mkdir(settings.VOICE_FILES)