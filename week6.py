from ssl import ALERT_DESCRIPTION_BAD_RECORD_MAC
from flask import Flask 
from flask import request 
from flask import redirect 
from flask import render_template 
from flask import session
from flask import url_for
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="12131213",
  database="website"
)
cursor=mydb.cursor(dictionary=True)

app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/" 
)

app.secret_key="any string but secret"

# 首頁
@app.route("/")
def index():
    return render_template("main.html")

# 登入驗證 post方法 導向成功或失敗
@app.route("/signin",methods=["post"])
def signin():
    account=str(request.form["account"])
    secret=str(request.form["secret"])
    account_sel="SELECT * FROM member WHERE username=%s"
    account_val=(account,)
    cursor.execute(account_sel,account_val)
    accountsql = cursor.fetchall()
    # member=accountsql[0]
    # print(member)
    # secret_sel="SELECT * FROM member WHERE password=%s"
    # secret_val=(secret,)
    # cursor.execute(secret_sel,secret_val)
    # secretsql = cursor.fetchall()
    # print(accountsql[0]["username"])
    # return "ok"
    # cursor.execute("SELECT id,name,username,password FROM member")
    # result = cursor.fetchall()
    # for i in range(len(accountsql)):
    if accountsql!=[]:
        if accountsql[0]["username"]==account and accountsql[0]["password"]==secret:
            session["id"]=accountsql[0]["id"]
            session["account"]=accountsql[0]["name"]
            return redirect("/member")
        # elif accountsql[i]==[]:
        #     return redirect(url_for("error",message="帳號或密碼輸入錯誤"))  
        # else:
            # return redirect(url_for("error",message="帳號或密碼輸入錯誤"))    
    else:
        return redirect(url_for("error",message="帳號或密碼輸入錯誤"))   

# 成功頁面
@app.route("/member")
def member():
    if "account" in session:
        name=session["account"]
        return render_template("member.html",name=name)
    else:
        return redirect("/")

# 失敗頁面
@app.route("/error")
def error():
    data=request.args.get("message","")
    data=str(data)
    return render_template("error.html",message=data)

# 登出頁面導向首頁
@app.route("/signout")
def signout():
    session.pop("account", None)
    return redirect("/")

# 註冊頁面
@app.route("/signup",methods=["post"])
def signup():
    name=request.form["name"]
    account=request.form["account"]
    secret=request.form["secret"]
    # cursor.execute("SELECT username FROM member")
    # result = cursor.fetchall()
    # for x in result:
    #     if account==x["username"]:
    #         return redirect(url_for("error",message="帳號已有人註冊"))
    #     else:
    #         sql="INSERT INTO member(name,username,password) VALUES (%s,%s,%s)"
    #         val=(name,account,secret)
    #         cursor.execute(sql,val)
    #         mydb.commit()
    #         return redirect("/")
    sql="SELECT * FROM member WHERE username=%s"
    usn=(account,)
    cursor.execute(sql,usn)
    result = cursor.fetchall()
    if result!=[]:
        return redirect(url_for("error",message="帳號已有人註冊"))
    else:
        sql="INSERT INTO member(name,username,password) VALUES (%s,%s,%s)"
        val=(name,account,secret)
        cursor.execute(sql,val)
        mydb.commit()
        return redirect("/")

# 埠號
app.run(port=3000)