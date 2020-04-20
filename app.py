from flask import Flask, request, render_template

from inspector import ImgLinkInspector

app = Flask(__name__)


@app.route('/')
def root():
    url = request.args.get('url')
    img_statuses = ImgLinkInspector(url).inspect() if url else None
    return render_template('index.html', url=url, img_statuses=img_statuses)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)