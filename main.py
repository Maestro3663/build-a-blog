from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Twilight84*@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    
    blogs = Blog.query.all()


    return render_template('blog.html',title="Build a Blog",blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])

def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ' '
        body_error = ' '
        if len(blog_title) == 0:
            title_error = 'Please fill out the title'
            body_error = 'Please fill out the body'
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
        if len(blog_body) == 0:
            body_error = 'Please fill out the body'
            title_error = 'Please fill out the title'
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = str(new_blog.id)
      
            return redirect('/blog?id={0}'.format(blog_id))
    
    return render_template('newpost.html')

@app.route('/blog')

def single():

    blog_id = int(request.args.get('id', 'default id'))
    blog = Blog.query.get(blog_id)
    blog_title = blog.title
    blog_body = blog.body

    return render_template('single.html', blog_title=blog_title, blog_body=blog_body)


    

if __name__ == '__main__':
    app.run()