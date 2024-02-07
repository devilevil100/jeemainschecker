import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from flask import session
from flask_session import Session
import time
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.html']
app.config['UPLOAD_PATH'] = '/home/lolex1098/mysite/uploads'
app.config['SECRET_KEY'] = 'abdullahmohabdullah'
app.config['SESSION_TYPE'] = 'filesystem'

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413
import requests, json





@app.route('/')
def index():

    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_resfiles():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]

        if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
            return f"{file_ext} Invalid", 400
        session['res']= filename
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))


    return '', 204

@app.route('/gay', methods=['POST'])
def upload_anssfiles():

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    session['ansswer']= filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]

        if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
            return f"{file_ext} Invalid", 400

        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))



    return '', 204
@app.route("/forward/", methods=['GET','POST'])
def move_forward():
    if request.method == "POST":
        responsefile = session.get('res')
        answerfile = session.get('ansswer')
        if answerfile == None:
            return f"bruh {responsefile}"
        soup = BeautifulSoup(open(f"/home/lolex1098/mysite/uploads/{responsefile}", encoding="utf8"), "html.parser")
        divs = soup.find_all('table', {'class': 'menu-tbl'})

        response = []
        answerkeys = []
        counter = 0
        for div in divs:
            first_td = div.find_all('td', {'class':'bold'})
            if first_td[0].text == 'MCQ':
                question_id = first_td[1].text
                answermarked= first_td[-1].text

                if answermarked != " -- ":
                    answermarkedid = first_td[int(answermarked)+1].text


                    optionsids=[int(first_td[2].text),int(first_td[3].text),int(first_td[4].text),int(first_td[5].text)]
                    optionslist =  sorted(optionsids)
                    print(optionslist)
                    positionid = optionslist.index(int(answermarkedid))
                    response.append({'question_id':question_id, 'answerid':positionid+1})
            else:
                findquestion = soup.find_all('table', {'class': 'questionPnlTbl'})
                table2 = findquestion[counter]
                first_td = table2.find_all('td', {'class':'bold'})

                question_id2 = first_td[-2].text
                answerid2= first_td[-4].text
                if answerid2 != " -- ":
                    response.append({'question_id':question_id2, 'answerid':answerid2})

            counter +=1

        print(len(response))
        answerkey = BeautifulSoup(open(f"/home/lolex1098/mysite/uploads/{answerfile}", encoding="utf8"), "html.parser")
        divs = answerkey.find('table')


        first_td = divs.find_all('td')
        counter = 0
        for tf in first_td:
            if counter%3 == 0:
                questionid = tf.text
                answer = first_td[counter+1].text
                answerkeys.append({'question_id':questionid, 'answerid':answer})
            counter +=1
        correct = 0
        incorrect = 0
        qmatched = 0
        wrongq=[]
        for i in response:
            qid = i['question_id']
            print(f"question: {i['question_id']}\n answer: {i['answerid']} ")
            for an in answerkeys:

                if an['question_id'] == qid:
                    qmatched +=1
                    print(f"answerkey: {str(an['answerid']) == str(i['answerid']) }")
                    if str(an['answerid']) == str(i['answerid']):

                        correct +=1
                    else:
                        wrongq.append(qid)
                        incorrect +=1
        print(qmatched)
        print(correct)
        print(incorrect)
        marks=correct*4-incorrect
        print(f"MARKS SCORED {marks}")
        

        return render_template('index.html', marks=marks, correct = correct,inc=incorrect,qids=wrongq);
    else:
        return redirect(url_for('index'))
