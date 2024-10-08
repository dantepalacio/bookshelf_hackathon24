import os
import sys

from uuid import uuid4

from flask import Flask, request, jsonify, send_from_directory
from flasgger import Swagger
from flasgger.utils import swag_from

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cv.check import check_post
from sqlite.db_operations import insert_data, get_post_id, get_table, get_post_by_id, set_action, change_status
# from mail_configuration import send_mail, configure_mail, send_appelation_mail
from utils.utils import add_to_csv

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger/index.yml')
# mail = configure_mail(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route("/")
@swag_from('swagger/index.yml')
def client():
    return send_from_directory('static/', 'index.html')

@app.route("/<path:path>")
def base(path):
    return send_from_directory('static/', path)

@app.route("/uploads/<path:path>")
def get_uploads(path):
    print(path)
    return send_from_directory('uploads/', path)


# {
#     action: like|dislike,
#     id: int
# }
HEADERS = {"Access-Control-Allow-Origin":"*"}


def rate_post(id, action):
    publication_from_db =  get_post_by_id(id)

    publication = {
        'text': publication_from_db['comment'],
        'image': publication_from_db['image'],
        'video': publication_from_db['video']
    }

    add_to_csv(publication, action)
    set_action(action,id)


@app.route('/rate', methods=['GET'])
def get_eval():
    if not request:
        return "400", 400, HEADERS
    action = request.args.get("action")
    id = request.args.get("id")
    if action is None or id is None:
        return "400", 400, HEADERS

    rate_post(id, action)
    return '<script>window.close()</script>',HEADERS


    


def get_attachment_from_request():
    file = request.files.get("attachment")
    print(f'AAA\n{file}')
    if file is None:
        return None, None
    if len(file.filename) < 1: # type: ignore
        return None, None
    
    *_, extension = file.filename.split(".")
    file_filename = f"{uuid4()}.{extension}"
    file_path = f"{app.config['UPLOAD_FOLDER']}{file_filename}"
    file.save(file_path)

    image_path = None
    video_path = None
    if file.mimetype.startswith("image/"):
        image_path = file_path
    elif file.mimetype.startswith("video/"):
        video_path = file_path
    return image_path, video_path


@app.route('/process_post_request', methods=['POST'])
def process_post_request():

    if not request:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400, HEADERS

    text = request.form.get('text')
    image_path, video_path = get_attachment_from_request()
    attachment = image_path or video_path

    if text is None and attachment is None:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400, HEADERS


    post_dict = {
        "text": text,
        "image": image_path,
        "video": video_path
    }

    answer = check_post(post_dict)


    if answer['text'] is not None:

        text_result = answer['text']
        print(f'TEXT:{text_result}')

    else:
        text_result = {'is_explicit': 'publish', 'reasons': []}

    if answer['image'] is not None:

        overall_image_result = answer['image']
        image_result = overall_image_result[0]
        ocr_image_result = overall_image_result[1]
        print(f'IMAGE:{image_result}')
        print(f'OCR IMAGE:{ocr_image_result}')

    else:
        overall_image_result = {'is_explicit': 'publish', 'reasons': []}


    if answer['video'] is not None:
        print()
        overall_video_result = answer['video']
        print(f'VIDEO:{overall_video_result[0]}')
        print(f'VIDEO OCR:{overall_video_result[1]}')
        
        audio_result = answer['audio']
        print(f'AUDIO FROM VIDEO:{audio_result}')

    else:
        overall_video_result = {'is_explicit': 'publish', 'reasons': []}
        audio_result = {'is_explicit': 'publish', 'reasons': []}


    overall_reasons = []
    temp_status = 'publish'
    for res_key, res_val in answer.items():
        if res_val is not None:
            for i in res_val:
                if i['is_explicit'] == 'ban':
                    temp_status = 'ban'
                    overall_reasons += i['reasons']
                elif i['is_explicit'] == 'same':
                    temp_status = 'same'
                    overall_reasons += i['reasons']
        
        else:
            continue
    

    insert_data(temp_status, text, image_path, video_path, ', '.join(overall_reasons))
    

    id = get_post_id(temp_status, text, image_path, video_path, ', '.join(overall_reasons))


    # if temp_status == 'ban' or temp_status == 'same':
    #     try:
    #         send_mail(mail, temp_status, {'status': temp_status, 'id': id, 'reasons': overall_reasons}, text=text, image_path=image_path, video_path=video_path)
    #     except Exception as e:
    #         print(e)

    return jsonify({'status': temp_status, 'id': id, 'reasons': overall_reasons}), 200, HEADERS



@app.route('/get_posts_request', methods=['GET'])
def get_posts_request():
    
    if not request:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400, HEADERS
    
    results = get_table()
    
    return jsonify({'results': results}), 200, HEADERS


@app.route('/send_appelation', methods=['POST'])
def send_appelation():
    if not request:
        return "400", 400, HEADERS

    id = request.form.get('id')

    user_message = request.form.get('text')

    post_data = get_post_by_id(int(id))

    send_appelation_mail(mail, id, user_message, post_data)

    return '200', 200, HEADERS


@app.route('/change_post_status', methods=['GET'])
def change_post_status():
    if not request:
        return "400", 400, HEADERS

    new_status = request.args.get("new_status")
    id = request.args.get("id")

    change_status(int(id), new_status)

    return '<script>window.close()</script>',HEADERS


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
