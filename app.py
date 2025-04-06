from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ToDoリストを格納するPythonリスト (メモリ上なので再起動で消える)
todos = [
    {'task': 'Renderにデプロイする', 'done': False},
    {'task': 'ポートフォリオ完成させる', 'done': False}
]

@app.route('/')
def index():
    """ 一覧ページを表示 """
    # enumerateを使って、テンプレートでインデックス番号も使えるようにする
    return render_template('index.html', todos=todos, enumerate=enumerate)

@app.route('/add', methods=['POST'])
def add_task():
    """ 新しいタスクを追加 """
    task_content = request.form.get('task') # フォームから'task'の値を取得
    if task_content: # 空でなければ追加
        todos.append({'task': task_content, 'done': False})
    return redirect(url_for('index')) # トップページにリダイレクト

@app.route('/check/<int:index>')
def check_task(index):
    """ タスクの完了状態を切り替える (インデックスで指定) """
    if 0 <= index < len(todos):
        todos[index]['done'] = not todos[index]['done'] # 完了状態を反転
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_task(index):
    """ タスクを削除する (インデックスで指定) """
    if 0 <= index < len(todos):
        todos.pop(index) # リストから削除
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Flaskの開発用サーバーを起動
    app.run(debug=True)