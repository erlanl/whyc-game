from flask import make_response, jsonify, request
from api.controllers.connectPlayers import *
import openai
import json
import requests
from dotenv import dotenv_values

MODEL_GPT = 'gpt-4'

credentials = dotenv_values(".env")

openai.api_key = credentials['OPENAI_API_KEY']
openai.Model.list()

def generate_image(active_rooms_lock, active_rooms):
    key_words = request.json
    sessionID = key_words["id"]
    room = compute_hashed_room(key_words["room"])

    with active_rooms_lock:
        if room in active_rooms:
            if sessionID in active_rooms[room].keys():
                active_rooms[room][sessionID]["words"] = key_words["key_words"]
                active_rooms[room][sessionID]["score"] = 0

    dalle_prompt = gpt_call(key_words["key_words"])
    image_url = dalle_call(dalle_prompt)   #DALLE
    #image_url = stable_diffusion_call(dalle_prompt, credentials) #STABLE DIFFUSION

    return make_response(
        jsonify(message='IMAGE URL:', url=image_url)
    )

def pass_image(active_rooms_lock, active_rooms):
    image = request.json
    sessionID = image["id"]
    room = compute_hashed_room(image["room"])

    with active_rooms_lock:
        if room in active_rooms and sessionID in active_rooms[room].keys():
            active_rooms[room][sessionID]["imageURL"] = image["url"]
            active_rooms[room][sessionID]["status"] = "Preparando"
            return {
                'message': 'Sucess'
            }
        return {
            'message': 'Failure'
        }

def gpt_call(key_words):
    gpt_prompt = "Crie um DALLE prompt em inglês utilizando as seguintes palavras:"
    for i in key_words:
        gpt_prompt = gpt_prompt + " " + i
    print(f"GPT PROMPT -> {gpt_prompt}")
    
    gpt_response = openai.ChatCompletion.create(
        model = MODEL_GPT,
        messages = [
            #{"role": "system", "content": ""},
            {"role": "user", "content": gpt_prompt}
        ],
        temperature = 1.5,
    )
    dalle_prompt = gpt_response['choices'][0]['message']['content']
    dalle_prompt = dalle_prompt[1:-1]
    dalle_prompt = dalle_prompt + " Detailed, Award-Winning Art, Trending on ArtStation, Photorealistic, 4K/8K"
    print(f"DALLE PROMPT -> {dalle_prompt}")
    
    return dalle_prompt

def dalle_call(dalle_prompt):
    dalle_response = openai.Image.create(
        prompt = dalle_prompt,
        n = 1,
        size = "1024x1024"
    )
    image_url = dalle_response['data'][0]['url']
    print(f"IMAGE URL -> {image_url}")

    return image_url

def stable_diffusion_call(stable_diffusion_prompt, credentials):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    data = {
      'prompt': stable_diffusion_prompt,
      'key': credentials['stable_diffusion_api_key'],
      'width': 1024,
      'height': 1024,
      'samples': 1,
      'safety_checker': "yes",
      'self_attention': "yes"
    }
    image_url = requests.post(url, data=data).json()['output']

    return image_url[0]