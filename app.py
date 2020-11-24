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
            
            cur.execute("INSERT INTO user_info (cws_id,phone_no,phone_model,created_time,id,updated_time) VALUES (?,?,?,?,?,?)", (cws,phone_no,phone_model,created_time,ids,created_time) )
            
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

@app.route('/validate_user')
def validate_user():
   return render_template('validate.html')

@app.route('/update_user')
def update_user():
   return render_template('update.html')

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from user_info")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/validate',methods = ['POST', 'GET'])
def validate():
   if request.method == 'POST':
      ids = request.form['ids']
      con = sql.connect("database.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("select * from user_info where id = (?)",(ids,))

      rows = cur.fetchall();
      return render_template("validate_result.html", rows=rows)

@app.route('/search',methods = ['POST', 'GET'])
def search():
   if request.method == 'POST':
      cws = request.form['cws']
      con = sql.connect("database.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("select * from user_info where cws_id = (?)",(cws,))

      rows = cur.fetchall();

      return render_template("search_result.html", rows=rows)

@app.route('/update',methods = ['POST', 'GET'])
def update():
   if request.method == 'POST':
      try:
         opt = operation.operation()
         cws = request.form['cws']
         phone_no = request.form['phone_no']
         phone_model = request.form['phone_model']
         created_time, ids = opt.calculate_code(cws, phone_no, phone_model)
         with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("UPDATE user_info SET phone_no = ?,phone_model = ?,id = ?, updated_time = ? where cws_id = ? ",(phone_no, phone_model, ids, created_time, cws))

            con.commit()
            msg = "Record successfully updated"
         if opt.qr_code_png(ids, cws):
            msg = msg + " and QR code has been generated"
            print("Sending mail to the user")
            image_mail.Mailer().send_message(cws)
      except Exception as err:
         con.rollback()
         msg = "error in update operation "+str(err)

      finally:
         return render_template("result.html", msg=msg)
         con.close()


if __name__ == '__main__':
   app.run(port=8080,debug = True)