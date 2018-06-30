#!/usr/bin/python
# -*- coding: utf_8 -*-
from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from io import open
import sys
import re
import subprocess
#from subprocess import check_output

# App config.
# App config.

PEOPLE_FOLDER = os.path.join('static', 'media')
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
 

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 

@app.route("/", methods=['GET', 'POST'])
def hello():
	flag=0
	form = ReusableForm(request.form)
	
	print form.errors
	if request.method == 'POST':
		name=request.form['name']
		
		if request.form['select'] == 'sentclicked':
			print(request.form['select'])
			flag=0
			#return redirect(url_for("hello",flag=flag))
		else:
			if request.form['select'] == 'parclicked':
				print(request.form['select'])
				flag=1

 		if request.form['select'] == 'submitsentclicked' or request.form['select'] == 'submitparclicked':
			if request.form['select'] == 'submitsentclicked':
				flag=0
			else:
				flag=1
			if form.validate():
				sent=preprocess(name) # a list of sentences
				#print(sent)
				no_of_sent = float(len(sent))
				pos = 0.0
				neg = 0.0
				nu = 0.0
				for s in sent:
					# Save the comment here.
					out=tagging(s)
					if out.replace('\n','') == 'POS':
						pos=pos+1.0
					elif out.replace('\n','') == 'NEG':
						neg=neg+1.0
					else:
						nu=nu+1.0
					flash('Sentence: '+s+'\n')
					flash('The Polarity of Sentence: '+out)

				tag=biggest(pos, neg)
				imagepath='static/media/'+tag+'.gif'
				pos_per = (pos/no_of_sent)*100.00
				neg_per = (neg/no_of_sent)*100.00
				return render_template('sentiment.html', form=form, value=imagepath,pos_per=pos_per,neg_per=neg_per,flag=flag,tag=tag)
			else:
				flash('All the form fields are required. ')
	
	return render_template('sentiment.html', form=form,flag=flag)

def biggest(pos, neg):
	if pos > neg:
		return 'POS'    
	elif neg > pos:
		return 'NEG'
	else:
             return 'NU'

def preprocess(sent):
	sent = sent.replace('?','.').replace('!','.') #replaced '!' and '?' with '.'
	sent=sent+'.'
 	sent = re.sub(r'\.+', ".", sent) # removed multiple consecutive '.'
	return sent.split('.')[:-1]


def tagging(sent):

	path='/home/rahul/flask-application/flask-env/bin/dictionary/'
	f=open(path+'neg.txt','r',encoding="utf-8")
	neg_lex=f.readlines()
	f.close()
	f=open(path+'pos.txt','r',encoding="utf-8")
	pos_lex=f.readlines()
	f.close()
	f=open(path+'int.txt',"r",encoding="utf-8")
	intensifier=f.readlines()
	f.close()

	f=open("tagged.txt","w",encoding="utf-8")
	words=re.sub(' +', ' ',sent).replace('.','').replace(',','').strip().split()
	counter=0
	neghandle=[]
	for w in words:
		temp=u''
		if (w+'\n'.decode('utf-8') in pos_lex) and  (w+'\n'.decode('utf-8') in intensifier):
			if (counter+1) < len(words):
				if (words[counter+1]+'\n'.decode('utf-8') in pos_lex) or  (words[counter+1]+'\n'.decode('utf-8') in neg_lex) or (words[counter+1]+'\n'.decode('utf-8') in intensifier):
					temp=temp+' '+w+'/INT'
				else:
					temp=temp+' '+w+'/POS'
			else:
				temp=temp+' '+w+'/POS'
		elif (w+'\n'.decode('utf-8') in neg_lex) and  (w+'\n'.decode('utf-8') in intensifier):
			if (counter+1) < len(words):
				if (words[counter+1]+'\n'.decode('utf-8') in pos_lex) or  (words[counter+1]+'\n'.decode('utf-8') in neg_lex) or (words[counter+1]+'\n'.decode('utf-8') in intensifier):
					temp=temp+' '+w+'/INT'
				else:
					temp=temp+' '+w+'/NEG'
			else:
				temp=temp+' '+w+'/NEG'
		elif (w+'\n'.decode('utf-8') in intensifier) and  (w+'\n'.decode('utf-8') not in pos_lex) and  (w+'\n'.decode('utf-8') not in neg_lex):
			temp=temp+' '+w+'/INT'
		elif (w+'\n'.decode('utf-8') in pos_lex):
			temp=temp+' '+w+'/POS'
		elif (w+'\n'.decode('utf-8') in neg_lex):
			temp=temp+' '+w+'/NEG'
		else:
			temp=temp+' '+w+'/0'

		counter=counter+1
		neghandle.append(temp)

	#negation handling
	rev=[]
	for w in neghandle:
		rev.insert(0,w)

	fn=open(path+'negation.txt','r',encoding="utf-8")
	
	negation=fn.readlines()
	fn.close()
	pos=0
	for w in rev:
		if (w.replace(' ','').split('/')[0]+'\n'.decode('utf-8') in negation):
			for i in range (pos+1,len(rev)):
				if rev[i].split('/')[-1].replace(' ','') == 'POS':
					rev[i]=rev[i].replace('POS','NEG')
					break
				if rev[i].split('/')[-1].replace(' ','') == 'NEG':
					rev[i]=rev[i].replace('NEG','POS')
					break
		pos=pos+1
	

	neghandle=rev
	rev=[]
	for w in neghandle:
		rev.insert(0,w)

	for w in rev:
		f.write(w)

	f.close()
	try:
    		return subprocess.check_output("python svm_module.py",shell=True,stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
    		raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


 
if __name__ == "__main__":
    #app.run()
    #app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 5001)))
    app.run(host= '0.0.0.0')
