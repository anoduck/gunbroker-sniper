#!/usr/bin/env python3
# ==========================================
#  ___
# | . \ ___  ___  ___  ___  _ _  ___ ._ _ _
# | | |/ ._>/ ._>| . \/ . || '_><_> || ' ' |
# |___/\___.\___.|  _/\_. ||_|  <___||_|_|_|
#                |_|  <___'
# ==========================================

from deepgram import Deepgram
import asyncio
import json
import os

# ---------------------------------
# Variables
# ---------------------------------

dg_key = os.getenv(DG_KEY)
dg_client = Deepgram(dg_key)


def deep_trans():
	async def main():
		# Open the audio file
		with open("captcha.wav", 'rb') as audio:
			# ...or replace mimetype as appropriate
			source = {'buffer': audio, 'mimetype': 'audio/wav'}
			response = await dg_client.transcription.prerecorded(source, {'punctuate': True})
			print(json.dumps(response, indent=4))
	asyncio.run(main())
	
