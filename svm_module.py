#!/usr/bin/python
# -*- coding: utf_8 -*-


import numpy as np
import pandas as pd
import sys
from io import open
from sklearn import svm
import pickle

def main():
	f=open('tagged.txt','r')
	sent=f.read().strip()
	feat_extract(sent.split())
	f.close()

def f_n_tag(sent,pol):
	count=0
	for w in sent:
		w.split('/')
		if pol in w.split('/')[-1]:
			count=count+1
	return count

def f_n_order(sent,t1,t2):
	count=0

	for w in range(len(sent)-1):
		if (t1 in sent[w].split('/')[-1]) and (t2 in sent[w+1].split('/')[-1]):
			count=count+1
	return count
	
def f_pol_at(sent,loc):
	if loc=='f':
		flag=0
		for w in sent:
			if u'POS' in w.split('/')[-1]:
				flag=1
				break
			if u'NEG' in w.split('/')[-1]:
				flag=-1
				break
		return flag
	else:
		flag=0
		for w in range (len(sent)-1,-1,-1):
			if u'POS' in sent[w].split('/')[-1]:
				flag=1
				break
			if u'NEG' in sent[w].split('/')[-1]:
				flag=-1
				break
		return flag


def f_conj(sent,loc,tag):

	cc_loc=-1
	for w in range(len(sent)-1,-1,-1):
		if 'CC' in sent[w].split('/')[1]:
			cc_loc=w
	if cc_loc!=-1:
		if loc=='b':
			count=0
			for w in range(cc_loc):
				if tag in sent[w].split('/')[-1]:
					count=count+1
			return count
		else:
			count=0
			for w in range(cc_loc,len(sent)):
				if tag in sent[w].split('/')[-1]:
					count=count+1
			return count
	else:
		return 0

def feat_extract(sent):
	temp={}
	temp['n_pos']=f_n_tag(sent,u'POS')
	temp['n_neg']=f_n_tag(sent,u'NEG')
	temp['n_int']=f_n_tag(sent,u'INT')

	temp['n_int_pos']=f_n_order(sent,u'INT',u'POS')
	temp['n_int_neg']=f_n_order(sent,u'INT',u'NEG')
	temp['n_int_int']=f_n_order(sent,u'INT',u'POS')
	temp['f_pol']=f_pol_at(sent,'f')
	temp['l_pol']=f_pol_at(sent,'l')

	temp['c_a_pos']=f_conj(sent,'a',u'POS')
	temp['c_b_pos']=f_conj(sent,'b',u'POS')

	temp['c_a_neg']=f_conj(sent,'a',u'NEG')
	temp['c_b_neg']=f_conj(sent,'b',u'NEG')

	temp['c_a_int']=f_conj(sent,'a',u'INT')
	temp['c_b_int']=f_conj(sent,'b',u'INT')

	#print(temp)
	df = pd.DataFrame([temp])
	test = np.asarray(df)
	loaded_model = pickle.load(open('finalized_model.sav', 'rb'))#the model created by SVM learning process, only model file loaded here for prediction
	prediction_svm = loaded_model.predict(test)
	print(prediction_svm[0])
	return


if __name__ == "__main__":	
	main()

