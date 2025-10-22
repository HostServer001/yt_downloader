from flask import Flask, render_template,request,send_file
from pytubefix import YouTube
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', username='Guest')


@app.route('/process', methods=['POST'])
def process():
    user_text = request.form['user_input']
    
    try:
        yt = YouTube(user_text)
        video_name = timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ys = yt.streams.get_highest_resolution()
        ys.download(f"downloads/{video_name}/")
        
        file_path = f"downloads/{video_name}/{yt.title}.mp4"
                
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"{yt.title}.mp4"
        )

    except Exception as e:
        return render_template('failed.html',ERROR_MSG=e)

if __name__ == '__main__':
    app.run(debug=True)
