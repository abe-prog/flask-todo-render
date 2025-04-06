import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Modified Database Configuration for Render Persistent Disk ---
# Renderでマウントする永続ディスクのパス (Render UIで設定するパスに合わせる)
# ここでは例として '/data' とする
persistent_data_dir = '/data' 
db_path = os.path.join(persistent_data_dir, 'todo.db')

# データベースファイルのパスを設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
# SQLAlchemyのイベントシステムを無効化（リソース節約）
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.task[:10]}>'

# --- データベース初期化 ---
# 初回起動時などにテーブルを作成
with app.app_context():
    # 永続ディスクのディレクトリが存在することを確認 (Renderがマウントするため通常は不要だが念のため)
    # os.makedirs(persistent_data_dir, exist_ok=True) 
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.id).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        new_task = Todo(task=task_content, done=False)
        try:
            db.session.add(new_task)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding task: {e}")
    return redirect(url_for('index'))

@app.route('/check/<int:id>')
def check_task(id):
    task_to_check = db.session.get(Todo, id)
    if task_to_check:
        try:
            task_to_check.done = not task_to_check.done
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error checking task: {e}")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = db.session.get(Todo, id)
    if task_to_delete:
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting task: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 本番環境ではGunicornがWSGIサーバーとして動作する
    # この部分はローカル開発用
    app.run(debug=True) # 本番デプロイ時は debug=False または削除