from flask import Flask, render_template, request
import sqlite3 as sql
import operation

import image_mail
app = Flask(__name__)



@app.route('/')
def home():
   return render_template('home.html')


@app.route('/enternew')
def new_student():
   return render_template('user.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         opt = operation.operation()
         cws = request.form['cws']
         phone_no = request.form['phone_no']
         phone_model = request.form['phone_model']
         created_time , ids = opt.calculate_code(cws,phone_no,phone_model)
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO user_info (cws_id,phone_no,phone_model,created_time,id) VALUES (?,?,?,?,?)", (cws,phone_no,phone_model,created_time,ids) )
            
            con.commit()
            msg = "Record successfully added"
         if opt.qr_code_png(ids,cws):
            msg = msg + " and QR code has been generated"
            print ("Sending mail to the user")
            # mailer.Mailer().send("febiponwin@gmail.com")
            # imageMailer.Mailer().messageBody("cws")
            image_mail.Mailer().send_message(cws)
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from user_info")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


if __name__ == '__main__':
   app.run(port=8080,debug = True)