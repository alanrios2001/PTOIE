from ast import arg
from locale import normalize
from operator import index
from nltk.tokenize import sent_tokenize, word_tokenize
from regex import B
from Contar import *

contador = Contar()


def print_debug(sentence, answer):
	print("============================== PRINT DEBUG ==============================")
	print(f"Pergunta: {sentence}\nResposta: {answer}")
	print("Analise de Dependencia: ")
	for word in sentence:
		print(f"{word.text} - {word.dep_} - {word.pos_} - {word.morph} - {word.head}")

def find_cases(set_arg):
	lis = []
	cas = False
	for token in set_arg:
		#print(token.text, token.dep_)
		if (token.dep_ == 'case' or token.dep_ == 'det') and cas == True:
			cas = False
		if (token.dep_ == 'case' or token.dep_ == 'det') and cas == False:
			lis.append([token])
			cas = True
		elif cas == True:
			lis[len(lis) - 1].append(token)
	return lis

def split_args(sentence, rel):
	if sentence == None or rel == None:
		return None

	sinal = False
	arg1 = []
	arg2 = []

	for token in sentence:
		if token == sentence[0]:
			continue
		if token == rel:
			sinal = True
			continue
		if sinal:
			arg2.append(token)
		else:
			arg1.append(token)

	return arg1, arg2


def split_sent_extract(sent, arg1, rel, arg2, id):
	with open("Sent explicita.", 'a', encoding='utf-8') as f:
		f.writelines(f"{sent}\n")
	with open("Extract explicita", 'a', encoding='utf-8') as f:
		f.writelines(f"{arg1}  |||   {rel}  |||  {arg2}\n")


def print_extraction(parser, sentence, answer, arg1, rel, arg2, contexto, id):
	name_file = parser + ".txt"
	text = f"Sentenca: {id}\n"
	text+= f'"{contexto}"\n'
	text+= f"-> Pergunta: {sentence} - Respotas: {answer}\n"
	text+= f"{arg1}  |||   {rel}  |||  {arg2}\n\n"
	with open(name_file, 'a', encoding='utf-8') as f:
		f.writelines(text)

def descendants(sentence, ancestor, ignoreFirst, *includes): 
	sent = sentence
	if ancestor == None:
		return None, None
	descendants = ""
	descendantList = []
	if ignoreFirst and isWh(sent[0]):
		sent = sentence[1:]
	for token in sent:
		if ancestor.is_ancestor(token) or ancestor == token or token in includes:
			descendants += str(token) + " "
			descendantList.append(token)
	if (len(descendants) > 0):
		return descendants.strip(), descendantList
	else:
		return None, None

def isWh(token):
	return token.lower_ in ['quem', 'onde', 'como', 'que', 'qual', 'quantos', 'quantas']


def extractHelper(arg1, rel, arg2):
	if "list" in str(type(arg1)):
		arg1 = ''.join(str(i) + " " for i in arg1).replace("?","").strip()
		arg1 = arg1.replace("  ", " ")
	if "list" in str(type(rel)):
		rel = ''.join(str(i).replace("?","").strip() + " " for i in rel).replace("  "," ").strip()
		rel = rel.replace("   ", " ")
	if "list" in str(type(arg2)):
		arg2 = ''.join(str(i) + " " for i in arg2).replace("?","").strip()
		arg2 = arg2.replace("  ", " ")
	return arg1.capitalize(), rel, arg2


def badExtract(i):
	if i == None or i.arg1 == None or str(i.arg1) == "" or i.rel == None or str(i.rel) == "" or i.arg2 == None or str(i.arg2) == "":
		return True
	return False

def normailazao(s):
	s = s.replace(')', "")
	s = s.replace('(', "")
	s = s.replace(']', "")
	s = s.replace('[', "")
	s = s.replace(",", "")
	s = s.replace("'", "")
	s = s.replace('"', "")
	s = s.replace("...", "")
	s = s.replace(".", "")
	s = s.replace("-", " ")
	s = s.replace(":", "")
	s = s.lower()
	return s

def find_best_senten(sentence_set, arg1, rel, arg2):
	b_score = 0
	b_sent = None

	arg1 = normailazao(arg1).split(" ")
	rel = normailazao(rel).split(" ")
	arg2 = normailazao(arg2).split(" ")

	for sent in sentence_set:
		aux = normailazao(sent).split(" ")
		a = len(set(arg1) & set(aux)) / len(arg1)
		b = len(set(rel) & set(aux)) / len(rel)
		c = len(set(arg2) & set(aux)) / len(arg2)

		if (a + b + c) > b_score:
			b_score = a + b + c
			b_sent = sent

	return b_sent

		


index_final = 0
def define_explicita(parser, arg1, rel, arg2, contexto):
	
	with_rel = []
	without_rel = []

	sentences_set = sent_tokenize(contexto)

	for sent in sentences_set:
		if rel in sent:
			with_rel.append(sent)
		else:
			without_rel.append(sent)

	best_sent = find_best_senten(with_rel, arg1, rel, arg2)

	if best_sent != None:
		contador.increment_explicitas()
		text = f"Id: {contador.explicitas}\n"
		text+= f"Sentenca: {best_sent}\n"
		text+= f"{arg1}  |||   {rel}  |||  {arg2}\n\n"
		with open("src/extracoes/" + parser + "Explicitas.txt", 'a', encoding='utf-8') as f:
			f.writelines(text)
	else:
		best_sent = find_best_senten(without_rel, arg1, rel, arg2)
		contador.increment_implicitas()
		text = f"Id: {contador.implicitas}\n"
		text+= f"Sentenca: {sent}\n"
		text+= f"{arg1}  |||   {rel}  |||  {arg2}\n\n"
		with open("src/extracoes/" + parser + ".txt", 'a', encoding='utf-8') as f:
			f.writelines(text)
		return
	##========= Teste =======================
	global index_final
	argx = normailazao(arg1).split(" ")
	relx = normailazao(rel).split(" ")
	argy = normailazao(arg2).split(" ")

	for sent in with_rel:
		aux = normailazao(sent).split(" ")
		a = len(set(argx) & set(aux)) / len(argx)
		b = len(set(relx) & set(aux)) / len(relx)
		c = len(set(argy) & set(aux)) / len(argy)
		
		if a > 0.8 and b > 0.8 and c > 0.8:
			#best_sent = find_best_senten(without_rel, arg1, rel, arg2)
			#contador.increment_implicitas()
			index_final+=1
			text = f"Id: {index_final}\n"
			text+= f"{parser}\n"
			text+= f"Sentenca: {sent}\n"
			text+= f"{arg1}  |||   {rel}  |||  {arg2}\n\n"
			with open("src/extracoes/" + "PTOIE_" + ".txt", 'a', encoding='utf-8') as f:
				f.writelines(text)
			break

