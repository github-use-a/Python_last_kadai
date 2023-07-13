from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

#初期画面
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

#ログイン
@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    # ログイン判定
    if db.login(user_name, password):
        session['user'] = True      # session にキー：'user', バリュー:True を追加
        session.permanent = True    # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=3)   # session の有効期限を 3分に設定
        return redirect(url_for('mypage'))
    else :
        error = 'ユーザ名またはパスワードが違います。'
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)


@app.route('/mypage', methods=['GET'])
def mypage():
    # session にキー：'user' があるか判定
    if 'user' in session:
        return render_template('mypage.html')   # session があれば mypage.html を表示
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト


@app.route('/register')
def register_form():
    return render_template('register.html')




@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, user_name=user_name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)
    
#機能一覧
    
@app.route('/bookregister')
def book_register():
    return render_template('bookregister.html')

@app.route('/book_register_exe', methods=['POST'])
def book_register_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')
    publisher = request.form.get('publisher')
           
    count = db.insert_book(title, author, category, publisher)
           
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('mypage', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('bookregister.html', error=error)

#図書一覧
@app.route('/booklist')
def book_list():
    book_list = db.select_all_books()
    return render_template('booklist.html', books=book_list)


@app.route('/backbooklist')
def back_booklist():
    return render_template('mypage.html')

#図書削除
@app.route('/book_delete')
def book_delete():
    return render_template('bookdelete.html')

@app.route('/book_select_delete', methods=['POST'])
def book_select_delete():
    title = request.form.get('keyword')
    db.delete_book(title)
    return render_template('mypage.html')

#図書検索








    
    
@app.route('/logout')
def logout():
    session.pop('user', None)   # session の破棄
    return redirect(url_for('index'))   # ログイン画面にリダイレクト

    
if __name__ == '__main__':
    app.run(debug=True)
    
    
