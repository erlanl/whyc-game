from threading import Lock

from configFlask import *
from api.controllers.connectPlayers import *
from api.controllers.generateImage import *
from api.controllers.game import *

active_rooms = {}
active_rooms_lock = Lock()

@app.route("/create_room", methods=["POST"])
def create_room_post():
    return create_room(active_rooms_lock, active_rooms)

@app.route("/join_room", methods=["POST"])
def join_room_post():
    return join_room(active_rooms_lock, active_rooms)
 
@app.route("/leave_room", methods=["POST"])
def leave_room_post():
    return leave_room(active_rooms_lock, active_rooms)

@app.route("/get_active_rooms", methods=["GET"])
def get_active_rooms_get():
    return get_active_rooms(active_rooms)

@app.route("/get_answer", methods=["POST"])
def get_answer_post():
    return get_answer(active_rooms_lock, active_rooms)

@app.route("/get_image", methods=["POST"])
def image_post():
    return get_image(active_rooms)

@app.route('/generate-image', methods=['POST'])
def generate_image_post():
    return generate_image(active_rooms_lock, active_rooms)

@app.route('/pass_image', methods=['POST'])
def pass_image_post():
    return pass_image(active_rooms_lock, active_rooms)

@app.route('/room_full', methods=['POST'])
def is_room_full_post():
    return is_room_full(active_rooms)

@app.route('/change_status', methods=['POST'])
def change_status_post():
    return change_status(active_rooms)

@app.route('/check_oponent_status', methods=['POST'])
def check_oponent_status_post():
    return check_status_oponent(active_rooms)

@app.route('/define_win', methods=['POST'])
def define_win_post():
    return define_win(active_rooms)

@app.route('/define_score_win', methods=['POST'])
def define_score_win_post():
    return define_score_win(active_rooms)

@app.route('/redefine_game', methods=['POST'])
def redefine_game_post():
    return redefine_game(active_rooms)