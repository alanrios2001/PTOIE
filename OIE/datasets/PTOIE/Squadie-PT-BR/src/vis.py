from glob import glob
from operator import index
from posixpath import split
from signal import NSIG
import spacy
import nltk
from tool_functions import *
import os

#nltk.download('punkt')
nlp = spacy.load('pt_core_news_lg')


indexblenk = 0
qual = 0
que = 0
threeOrFour = 0
quem = 0
onde = 0
como = 0
generic = 0
noObj = 0
noNsubj = 0

def parse(sentence, answer, contexto):
	obj = False
	nsubj = False

	global qual
	global que
	global quem
	global onde
	global como
	global threeOrFour
	global generic
	global noObj
	global noNsubj

	# Contabilizando os tipos de perguntas.
	if sentence[0].lower_ == 'qual':
		qual+=1
	if sentence[0].lower_ == 'que':
		que+=1
	if len(sentence) <= 4:
		threeOrFour+=1
	if sentence[0].lower_ == 'quem':
		quem+=1
	if sentence[0].lower_ == 'onde':
		onde+=1
	if sentence[0].lower_ == 'como':
		como+=1
	generic+=1

	for token in sentence:
		if token.dep_.endswith("obj"): 
			obj = True
		if "subj" in token.dep_ and not isWh(token):
			nsubj = True
	if not obj:
		noObj+=1
	if not nsubj:
		noNsubj+=1
	#======================================================================

	whichParse(sentence, answer, contexto)
	whoParseNsubj(sentence, answer, contexto)
	whereParse(sentence, answer, contexto)
	howParse(sentence, answer, contexto)
	threeOrFourParser(sentence, answer, contexto)
	genericParse(sentence, answer, contexto)
	noObjParse(sentence, answer, contexto)
	noSubjParse(sentence, answer, contexto)

	#Contabilizando no Terminal
	os.system('cls' if os.name == 'nt' else 'clear')
	print("=================== RESUMO ======================")
	print("Qual: ", qual)
	print("Que: ", que)
	print("ThreeOrFour: ", threeOrFour)
	print("Quem: ", quem)
	print("Onde: ", onde)
	print("Como: ", como)
	print("NoObj: ", noObj)
	print("NoNsubj: ", noNsubj)
	print("Generic (TOTAL): ", generic)
	return None
	#===============================================================

#====================================================
#        Parses selecionados pela funcao parse      |
#====================================================

def whichParse(sentence, answer, contexto): 
	if sentence[0].lower_ == "qual":
		root = None
		is_verb = False

		if sentence.root.pos_ != 'VERB':
			for token in sentence:
				if token.dep_ == 'cop' and token.pos_ == 'AUX':
					root = [token]
					break
		else:
			root = [sentence.root]
			is_verb = True


		if root != None:
			if is_verb:
				argx, argy = split_args(sentence, root[0])
				for token in argx:
					if 'aux' in token.dep_:
						root.insert(0, token)
						argx.remove(token)

				complements = find_cases(argx)
			
				for lista in complements:
					argx = set(argx) - set(lista)
			
				if len(argx) == 0:
					arg1, rel, arg2 = extractHelper([answer], root, argy)
					if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
						return None
					define_explicita("WhichQualParser", arg1, rel, arg2, contexto)
				else:
					arg1, rel, arg2 = extractHelper([answer], root, argy)
					if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
						return None
					define_explicita("WhichQualParser", arg1, rel, arg2, contexto)
					for i in complements:
						argy = argy + i
					arg1, rel, arg2 = extractHelper([answer], root, argy)
					if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
						return None
					define_explicita("WhichQualParser", arg1, rel, arg2, contexto)						
			else:
				argx, argy = split_args(sentence, root[0])
				if len(argy) > 0 and argy[0].dep_ == 'det':
					arg1, rel, arg2 = extractHelper(argy, root, answer)
					if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
						return None
					define_explicita("WhichQualParser", arg1, rel, arg2, contexto)
				else:
					arg1, rel, arg2 = extractHelper([answer], root, argy)
					if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
						return None
					define_explicita("WhichQualParser", arg1, rel, arg2, contexto)		
	else:
		propn = None
		argx1 = None
		argx2 = None

		arg1 = None
		rel = None
		arg2 = None

		aux = None

		if len(sentence) <= 1 or sentence[0].lower_ != 'que' or sentence[1].dep_ != 'nsubj' or sentence.root == None:
			return None

		for i in range(1, len(sentence)):
			if sentence[i].pos_ == "PROPN" or sentence[i].pos_ == "PRON":
				propn = sentence[i].i
				break
	 
		if propn != None:
			argx1, argx2 = split_args(sentence, sentence.root)
		
			if propn < sentence.root.i:
				aux = argx1.pop(0)

				if aux.lower_ in answer.lower():
					aux = answer
				else:
					aux = aux.text + " " + answer
			
			
				arg1, rel, arg2 = extractHelper(argx1, [sentence.root], argx2 + [aux])
				if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
					return None
				define_explicita("WhichQueParser", arg1, rel, arg2, contexto)

				arg1, rel, arg2 = extractHelper(argx1, [sentence.root], [aux] + argx2)
				if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
					return None
				define_explicita("WhichQueParser", arg1, rel, arg2, contexto)

				arg1, rel, arg2 = extractHelper(argx1, [sentence.root], argx2 + [answer])
				if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
					return None
				define_explicita("WhichQueParser", arg1, rel, arg2, contexto)
			else:
				arg1, rel, arg2 = extractHelper([answer], [sentence.root], argx2)
				if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
					return None
				define_explicita("WhichQueParser", arg1, rel, arg2, contexto)
		else:
			return None


def whoParseNsubj(sentence, answer, contexto):

		arg1 = ""
		arg2 = ""
		rel = []
		relBad = []

		nmod = True
		dobj = True

		if sentence[0].lower_ != "quem": 
			return None
		
		arg1 = answer 

		_, rel = descendants(sentence, sentence.root, True) 
		for child in rel:
			if child.dep_ == "nmod":
				relBad.append(child)
				pobj = True
				break
			else:
				pobj = False

		if pobj == False:
			for child in rel:
				if child.dep_ == "dobj":
					relBad.append(child)
					dobj = True
					break
				else:
					dobj = False
	
		if dobj == False:
			for child in rel:
				if child.dep_ == "nsubj":
					relBad.append(child)
					break
		
		sinal = False
		if len(relBad) != 0:
			for token in rel:
				if sinal:
					relBad.append(token)
				if token.text == relBad[0].text:
					sinal = True

		rel = [token for token in rel if not token in relBad]
		rel_true = []
		bl_aux = []
		veri = True
		for i in rel:
			if veri:
				rel_true.append(i)
			else:
				bl_aux.append(i)
			if (i == sentence.root):
				veri = False

		arg1, rel, arg2 = extractHelper(answer, rel_true, bl_aux  + relBad)

		if (arg1 != None and rel != None and arg2 != None):
			define_explicita("WhoParse", arg1, rel, arg2, contexto)


def whereParse(sentence, answer, contexto):
	if sentence[0].lower_ == 'onde':
		arg1 = []
		arg2 = []
		rel = []

		prep = False
		other = False
		complement = None

		num = 0

		if sentence.root.pos_ == "VERB":
			_, rootChildren = descendants(sentence, sentence.root, True) 

			arg_aux1, arg_aux2 = split_args(sentence, sentence.root)

			l_aux = []
			index = []
			for token in arg_aux1:
				if token.dep_ == 'aux:pass' or token.dep_ == 'expl':
					index.append(arg_aux1.index(token))
					l_aux.append(token)
					break

			for i in index:
				arg_aux1.pop(i)
			rel = l_aux



			if len(arg_aux1) == 0:
				arg1 = arg_aux2
				arg2 = answer
				rel.append(sentence.root)
			else:
				arg1 = arg_aux1
				arg2 = arg_aux2 + [answer]
				rel.append(sentence.root)

	
		arg1, rel, arg2 = extractHelper(arg1, rel, arg2)

		if arg1 == "" or arg1 == None or rel == "" or rel == None or arg2 == "" or arg2 == None:
			return None
		global indexblenk
		indexblenk+=1
		define_explicita("WhereParse", arg1, rel, arg2, contexto)


def howParse(sentence, answer, contexto):
	arg1 = []
	rel = []
	arg2 = []

	list_complemente = ['por meio de', 'como', '']

	alanise_answer = nlp(answer)
	
	if sentence[0].lower_ == 'como' and sentence.root.pos_ == 'VERB':
		rel.append(sentence.root)

		argx, argy = split_args(sentence, sentence.root)

		for i in sentence:
			if i.dep_ == 'nsubj' or i.dep_ == 'nsubj:pass':
				_, arg1 = descendants(sentence, i, True)
				break

		for token in argx:
			if 'aux' in token.dep_ or 'expl' in token.dep_:
				rel.insert(0, token)
				argx.remove(token)

		if len(argx) == 0:
			for word in list_complemente:
				arg1, rel, arg2 = extractHelper(argy, rel, [word] + [answer])
				define_explicita("HowParse", arg1, rel, arg2, contexto)
		
		elif "VERB" in alanise_answer[0].pos_ and len(answer) > 30:
			
			for i in range(len(alanise_answer)):
				if i == 0:
					rel = [alanise_answer[i]]
				else:
					arg2.append(alanise_answer[i])

			arg1, rel, arg2 = extractHelper(arg1, rel, arg2)
			define_explicita("HowParse", arg1, rel, arg2, contexto)

		else:
			for word in list_complemente:
				arg1, rel, arg2 = extractHelper(argx, rel, argy + [word] + [answer])
				if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
					return None
				define_explicita("HowParse", arg1, rel, arg2, contexto)
				arg1, rel, arg2 = extractHelper(argx, rel, [word] + [answer] + argy)
				if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
					return None
				define_explicita("HowParse", arg1, rel, arg2, contexto)
		
		arg1, rel, arg2 = extractHelper(argx, [sentence.root], argy)
		define_explicita("HowParse", arg1, rel, arg2, contexto)

def threeOrFourParser(sentence, answer,  contexto):

	arg1 = None
	arg2 = None
	rel = None

	if len(sentence.text.split()) >= 5:
		return None

	for token in sentence:
		if token.pos_ == "VERB" and token.dep_ == "ROOT":
			rel = [token]
			break

	if rel != None:
		arg_s1, arg_s2 = split_args(sentence, sentence.root)

		if arg_s1 != None and arg_s2 != None:
			for i in arg_s1:
				if i.dep_ == "nsubj":
					arg1 = arg_s1
					arg2 = arg_s2 + [answer]
					break
			if (arg1 != None and rel != None and arg2 != None):
				arg1,rel,arg2 = extractHelper(arg1,rel,arg2)
				if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
					return None
				define_explicita("ThreeOurFourParser", arg1, rel, arg2, contexto)

def genericParse(sentence, answer, contexto):

	arg1 = None
	arg2 = None

	if sentence.root.pos_ != 'VERB':
		return None

	for i in sentence:
		if i.dep_ == "nsubj" and not isWh(i):
			_,arg1 = descendants(sentence, i, True)
		if i.dep_ == "obj":
			_,arg2= descendants(sentence, i, True)



	arg1, rel, arg2 = extractHelper([answer], [sentence.root], arg2)
	if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
		return None
	define_explicita("GenericParse", arg1, rel, arg2, contexto)



def noObjParse(sentence, answer, contexto):
	root = []
	subjGroups = []
	x = None
	y = None

	for token in sentence:
		if token.dep_.endswith("obj"): 
			return None 
		if (token.dep_ == "nsubj" or token.dep_ == "nsubjpass") and not isWh(token):
			subjGroups.append(descendants(sentence, token, True)[1])

	if len(subjGroups) == 0:
		return None
	trueSubjPos = len(subjGroups) - 1 
	if len(subjGroups) > 1: 
		count = 0
		for group in subjGroups:
			for word in group:
				if word.pos_ == "PROPN":
					trueSubjPos = count
			count = count + 1
	
	is_verb = False

	if sentence.root.pos_ != 'VERB':
		for token in sentence:
			if token.dep_ == 'cop' and token.pos_ == 'AUX':
				root = [token]
				break
	else:
		root = [sentence.root]
		is_verb = True

	if len(root) > 0:
		x, y = split_args(sentence, root[0])
	else:
		return None

	if is_verb:
		for token in subjGroups[trueSubjPos]:
			if 'aux' in token.dep_:
				root.insert(0, token)
				subjGroups[trueSubjPos].remove(token)

		arg1, rel, arg2 = extractHelper(''.join(str(i) + " " for i in subjGroups[trueSubjPos]).strip(), ''.join(str(i).replace("?", "").replace(",", "").strip() + " " for i in root).strip(), y + [answer])
		if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
			return None
		define_explicita("NoObj Parse", arg1, rel, arg2, contexto)

		arg1, rel, arg2 = extractHelper(''.join(str(i) + " " for i in subjGroups[trueSubjPos]).strip(), ''.join(str(i).replace("?", "").replace(",", "").strip() + " " for i in root).strip(), [answer])
		if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
			return None
		define_explicita("NoObj Parse", arg1, rel, arg2, contexto)

	else:
		arg1, rel, arg2 = extractHelper(y, ''.join(str(i).replace("?", "").replace(",", "").strip() + " " for i in root).strip(), [answer])
		if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
			return None
		define_explicita("NoObj Parse", arg1, rel, arg2, contexto)
	

def noSubjParse(sentence, answer, contexto):
	arg1 = []
	rel = []
	arg2 = []

	objCounter = 0
	nonObj = False
	noMoreObj = False

	for i in range(1, len(sentence)):
		token = sentence[i]
		if (token.dep_ == "nsubj" or token.dep_ == "nsubjpass") and not isWh(token):
			return None

	if "subj" in sentence[0].dep_: 
		arg1 = answer
		for child in sentence:
			if "obj" in child.dep_ and objCounter == 0 or "advcl" in child.dep_ and objCounter == 0 or "xcomp" in child.dep_ and objCounter == 0:
				_, rel = descendants(sentence, child, True, sentence.root)
				objCounter += 1
				nonObj = True
			if "prep" in child.dep_:
				_, arg2 = descendants(sentence, child, True)
				for obj in arg2:
					#print([i.dep_ for i in list(obj.rights)])
					if ('obj' in str([i.dep_ for i in list(obj.rights)]) and objCounter > 0) or ('obj' in str([i.dep_ for i in list(obj.rights)]) and nonObj == True):
						_, arg2 = descendants(sentence, child, True)
						noMoreObj = True
			if "obj" in child.dep_ and noMoreObj == False:
				_, arg2 = descendants(sentence,child,True)
		rel = [token for token in rel if not token in arg2]

	
	arg1, rel, arg2 = extractHelper(arg1, rel, arg2)
	if arg1 == None or arg1  == '' or rel == None or rel == '' or arg2 == None or arg2 == '':
		return None
	define_explicita("NoSubj Parse", arg1, rel, arg2, contexto)
