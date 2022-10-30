# week6 optional
```python
# 會員頁面
@app.route("/member")
def member():
    if "account" in session:
        name=session["account"]
        content_sel="SELECT name,content FROM member INNER JOIN message on member.id=message.member_id"
        cursor.execute(content_sel)
        result=cursor.fetchall()
        row=result
        return render_template("member.html",name=name,data=row)
    else:
        return redirect("/")
```

```python
# 儲存留言頁面
@app.route("/message",methods=["post"])
def message():
    member_id=session["id"]
    message=request.form["message"]
    sql="INSERT INTO message(member_id,content) VALUE (%s,%s)"
    val=(member_id,message)
    cursor.execute(sql,val)
    mydb.commit()
    return redirect("/member")
```

```html
<!---會員頁面--->
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title>member</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body style="background-color:#f7f9f9">
        <div class="title">歡迎光臨</div>
        <div class="text">{{ name }}，歡迎登入系統</div>
        <div  class="form">
            <form action="signout">
                <div class="button1"><button >登出</button></div>
            </form>
        </div>
        <hr>
        <div class="text">快來留言吧</div>
        <div  class="form">
            <form action="/message" method="post">
                <div class="input">留言: <input type="text" name="message"/></div>
                <div class="button"><button>送出</button></div>
            </form>
        </div>
        <hr>
        <div class="text">留言板</div>
            {% for i in data %}
            <div class="message">{{ i.name }}:{{ i.content }}</div>
            {% endfor %}
    </body>
</html>
````
