from flask import Flask, render_template, request
import jinja2

app = Flask(__name__,
            static_folder='.',        # CSS/JS 在根目錄
            static_url_path='')       # 讓 /style.css 直接對到根目錄

app.jinja_loader = jinja2.FileSystemLoader('.')

@app.context_processor
def inject_helpers():
    def fake_url_for(endpoint, **kwargs):
        mapping = {
            'dogs.list':               '/',
            'dogs.detail':             f"/dogs/{kwargs.get('id','')}",
            'dogs.create':             '/dogs/create',
            'dogs.edit':               f"/dogs/{kwargs.get('id','')}/edit",
            'applications.apply':      f"/apply/{kwargs.get('dog_id','')}",
            'applications.my_applications': '/my-applications',
            'applications.review':     '/review',
            'admin.dashboard':         '/admin',
            'admin.reports':           '/admin/reports',
            'auth.login':              '/login',
            'auth.logout':             '/logout',
            'auth.register':           '/register',
            'static':                  f"/{kwargs.get('filename','')}",
        }
        return mapping.get(endpoint, '/')
    return dict(url_for=fake_url_for,
                request=request,
                current_user=type('U', (), {
                    'is_authenticated': False,
                    'role': 'guest',
                    'name': '',
                    'email': '',
                    'phone': '',
                    'city': ''
                })())

@app.route('/')
def index():
    return render_template('list.html',
                           dogs=[],
                           dogs_json=[],
                           stats={'available': 128, 'adopted': 342},
                           liked_ids=[],
                           pagination=None)

if __name__ == '__main__':
    app.run(debug=True)