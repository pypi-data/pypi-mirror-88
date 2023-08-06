# -*- coding: utf-8 -*-

"""Payload."""

import spacy

"""
Payloads are assigned to Open Class Words ONLY!

https://universaldependencies.org/docs/u/pos/

Open class words 	Closed class words 	Other
----------------	------------------	-----
ADJ 				ADP 				PUNCT
ADV 				AUX 				SYM
INTJ 				CONJ 				X
NOUN 				DET 	 
PROPN 				NUM 	 
VERB 				PART 	 
  					PRON 	 
  					SCONJ 	 
"""

_POS_SCORES_ = {
	'ADJ'  :  1.5, 	#adjective
	'ADV'  :  1.5, 	#adverb
	'INTJ' :  1.0, 	#interjection
	'NOUN' :  2.0, 	#noun
	'PROPN':  2.5, 	#proper noun
	'VERB' :  2.0
}

"""
Part of Speech payloads are cool, but the real juice is from dependencies!
Specifically: subjects, objects, and roots.

Intuition: the "aboutness" of sentences is more important than just the concepts mentioned.
"""

_DEP_SCORES_ = {
	'nsubjpass': 2.0,
	'nsubj'    : 2.0,
	'dobj'     : 2.0,
	'pobj'     : 1.5,
	'root'     : 2.0
}


class Payloader:

	def enrich(self,stream):
		
		payloads = []

		for tok in stream:
			score = None

			if (len(tok.text)>0) and ('|' not in tok.text):

				if (tok.is_alpha) and (len(tok.lemma_)>0) and (tok.pos_ in self.pos_scores):
					score = self.pos_scores[tok.pos_]

					if tok.dep_ in self.dep_scores:
						score += self.dep_scores[tok.dep_]

					value = str(score) # + 'f'

					payloads.append(tok.lemma_ + '|' + value + ' ')

				else:
					payloads.append(tok.text_with_ws)

			else:
				payloads.append(tok.text_with_ws.replace('|',''))

		return ''.join([t for t in payloads if len(t)>0])

	def __init__(self,pos_scores=_POS_SCORES_,dep_scores=_DEP_SCORES_):
		self.dep_scores = dep_scores
		self.pos_scores = pos_scores