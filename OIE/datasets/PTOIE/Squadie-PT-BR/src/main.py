import json
import vis as v
import spacy
import sys
import argparse
import nltk
import tool_functions
# Creates qaTuples-train and dev which contains questions, IDs, answers, tuples, and the contextual paragraphs


parser = argparse.ArgumentParser()
parser.add_argument("-dev", "--devset", action="store_true",
                    help="Use of the much smaller dev training set")
args = parser.parse_args()

VERSION = "2.0v1.1"
TRAINFILE = "./squad2/train-v2.0.json"
JSON_FILE = "./data/qaTuples-train.json"

if args.devset:
	TRAINFILE = "./squad2/dev-v2.0.json"
	JSON_FILE = "./data/qaTuples-dev.json"


nlp = spacy.load('pt_core_news_lg')
failures = 0
successes = 0


with open(TRAINFILE, encoding = "utf8") as f:
	dataset_json = json.load(f)
	dataset = dataset_json['data']

failList = []

with open(JSON_FILE, "w", encoding = "utf8") as outFile:
	squadieJson = {"version": VERSION, "data": []}
	for topic in dataset: 
		squadieTopic = {"title": topic['title'], "paragraphs": []}
		for blob in topic['paragraphs']:
			squadieParagraph = {"qas": [], "context": blob["context"]}
			for span in blob['qas']: 
				squadieQa = {"question": None, "id": span['id'], "answer": None, "tuple": None, "answer_start": None}
				if len(span['question']) < 60:# -> Cut off at 60 characters because parser doesn't do well on long sentences
					q = span['question'].replace("\t", "")
					if q.endswith("."):
						q = q[:-1]
					if q.endswith(" "):
						q.rstrip()
					if not q.endswith("?"):
						q += "?"
					shortAnswer = None
					shortAnswerStart = None
					for answerBlob in span['answers']:
						ans = answerBlob['text']
						if shortAnswer == None or len(ans) < len(shortAnswer):
							shortAnswer = ans
							shortAnswerStart = answerBlob['answer_start']
							successes = successes + 1
					sentence = list(nlp(q).sents)[0]
					x = v.parse(sentence, shortAnswer.replace("\t", ""), blob["context"])
					if x == None:
						failures = failures + 1
						failList.append(str(sentence) + " " + str(shortAnswer))
					else:
						successes = successes + 1
						#print(x,"\n")
						squadieQa['question'] = q
						squadieQa['tuple'] = str(x)
						squadieQa['answer'] = shortAnswer
						squadieQa['answer_start'] = shortAnswerStart
				squadieParagraph['qas'].append(squadieQa)
			squadieTopic["paragraphs"].append(squadieParagraph)
		squadieJson["data"].append(squadieTopic)
	json.dump(squadieJson, outFile, indent = 4, ensure_ascii = False)
						
				