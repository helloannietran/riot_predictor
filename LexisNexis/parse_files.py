import re
from datetime import datetime
import os
from os import listdir, mkdir
from os.path import isfile, join
import shutil



keywords = {}

def load_keywords():
	global keywords
	with open("../keywords.txt", 'r') as kwrd_file:
		keywords_tmp = eval(kwrd_file.read())
	for k in keywords_tmp.keys():
		vals = [v.lower() for v in keywords_tmp[k]]
		keywords[k] = vals


def find_doc_number(read_file):
	while  True:
		l = ""
		try:
			l = read_file.readline()
			if not l:
				return '-1'
			l = l.strip()
			r = re.match('[0-9]+ of [0-9]+ DOCUMENTS', l)
			if r and r.group(0) == l:
				num = l.split()[0]
				return '%03d' % int(num)
		except ValueError as e:
				continue

def spare_lines(read_file):
	line = None
	while not line:
		line = read_file.readline().strip()
	return line

def read_one_file(read_file, pre):
	subject = find_doc_number(read_file)
	if subject == '-1':
		return False
	filename = subject if len(subject) < 100 else subject[:100]
	filename = pre + '_' + filename.strip() + '.out'
	line = subject
	subject = subject.strip()
	with open('files/' + filename, 'w') as write_file:
		while(True):
			write_file.write(line)
			if line.startswith('LANGUAGE:'):
				# lang_line = spare_lines(read_file).strip()
				# publish_type = spare_lines(read_file).strip()
				# write_file.write(lang_line+'\n'+publish_type+'\n')
				write_file.write(line)
				break
				# if lang_line.startswith('LANGUAGE:') and publish_type.startswith('PUBLICATION-TYPE:'):
				# 	break
			line = read_file.readline()
			if not line:
				break
	return True

def separate_files():
	src_dir = 'lexis_res/'
	try:
		shutil.rmtree('files')
	except Exception as e:
		print e

		pass
	mkdir('files')
	all_files = get_all_files_in_dir(src_dir)
	print 'all: ', all_files
	for file in all_files:
		pref = file.split(".")[0]
		with open(src_dir + file, 'r') as read_file:
			while True:
				if not read_one_file(read_file, pref):
					break
	print "Dooone"

def get_all_files_in_dir(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def does_match_riot(text, keywords):
	for word in keywords:
		w = word.lower()
		if text.find(w) < 0:
			return False
	return True

def find_match_riot(text):
	global keywords
	matches = []
	text = text.lower()
	for k in keywords.keys():
		if does_match_riot(text, keywords[k]):
			matches.append(k)
	print 'found matches: ', matches
	if len(matches) < 15:
		return matches
	else:
		return None


def match_files():
	global keywords
	load_keywords()
	all_files = get_all_files_in_dir('files')
	try:
		shutil.rmtree('riots')
	except:
		pass
	mkdir('riots')

	res_dir = 'riots/'
	for file in all_files:
		print 'looking at riot %s' % file
		with open('files/'+ file, 'r') as in_file:
			content = in_file.read()
			matches = find_match_riot(content)
			if matches:
				for match in matches:
					match = '%03d' % int(match)
					try:
						mkdir(res_dir + match)
					except:
						pass
					with open("riots/%s/%s" %(match, file), 'w') as riot_file:
						riot_file.write(content)





separate_files()
match_files()