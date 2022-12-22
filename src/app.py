from PIL import ImageDraw, Image
import qrcode, random, json, time, uuid, os, dotenv, datetime, base64
from threading import Thread
from hubspain.generation import stablediffusion
from flask import Flask, render_template, request
from queue import Queue
from io import BytesIO

app = Flask(__name__)

dotenv.load_dotenv(dotenv.find_dotenv())
ON_PRODUCTION = os.getenv("ON_PRODUCTION")
PRODUCTION_URL = os.getenv("PRODUCTION_URL")
DEVELOPMENT_URL = os.getenv("DEVELOPMENT_URL")
hsp_apikey = os.getenv("HSP_APIKEY")
queue = Queue()
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
image_count = 0
total_served = 0
start_time = time.time()
start_time = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
sleep_mode = False
num_loaded_prompts = 0

def generate_image():
    while True:
        global sleep_mode
        if queue.qsize() < 101:
            sleep_mode = False
            with open('src/static/data/prompts.txt', 'r', encoding='utf-8') as f:
                PROMPT_LIST = f.readlines()
                # count prompts
                global num_loaded_prompts
                num_loaded_prompts = len(PROMPT_LIST)
            selected_prompt = random.choice(PROMPT_LIST)
            with open('src/static/data/submit_dict.json', 'r') as fp:
                submit_dict = json.load(fp)
            params = submit_dict['params']
            submit_dict = {
            "prompt": selected_prompt,
            "params": params,}
            images = stablediffusion(hsp_apikey,submit_dict=submit_dict)
            for i, image in enumerate(images):
                global image_count
                image_count += 1
                id_image = str(uuid.uuid4())
                image_buffer = BytesIO()
                image.save(image_buffer, format="PNG")
                image_buffer.seek(0)
                img_toqr = Image.open(image_buffer)
                qr_image = draw_qr_code(img_toqr, id_image)
                image_data = {
                    "image": image,
                    "prompt": selected_prompt,
                    "id_image": id_image,
                    "image_qr": qr_image,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                queue.put(image_data)
            time.sleep(3)
        else:
            sleep_mode = True
            # delete 10 images from queue
            for i in range(10):
                queue.get()
            time.sleep(3)

def draw_qr_code(image, id_image):
    size = image.size
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6, 
        border=2)
    if ON_PRODUCTION:
        qr.add_data(f"{PRODUCTION_URL}/image/{id_image}")
    else:
        qr.add_data(f"{DEVELOPMENT_URL}/image/{id_image}")
    qr.make(fit=True)
    img = qr.make_image(back_color="white", fill_color="black")
    img_draw = ImageDraw.Draw(image)
    corner_x = size[0]
    corner_y = size[1]
    img_draw.bitmap((corner_x - 255, corner_y - 250), img)
    return image


@app.route("/imagine")
def show_image():
    global total_served
    total_served += 1
    if queue.empty():
        return render_template("loading.html")
    else:
        image_data = queue.queue[-1]
        id_image = image_data['id_image']
        image_qr = image_data['image_qr']
        buffer = BytesIO()
        image_qr.save(buffer, format="PNG")
        buffer.seek(0)
        image_content = buffer.getvalue()
        image_qr = base64.b64encode(image_content).decode('utf-8')
        return render_template("image.html", image_qr=image_qr, id_image=id_image)

@app.route("/image/<id_image>")
def show_unprocessed_image(id_image):
    found = False
    for i, image in enumerate(queue.queue):
        if image['id_image'] == id_image:
            found = True
            break
    if found:
        image_data = queue.queue[i]
        selected_id = id_image
        prompt = image_data['prompt']
        image_original = image_data['image']
        buffer = BytesIO()
        image_original.save(buffer, format="PNG")
        buffer.seek(0)
        image_content = buffer.getvalue()
        image_data = base64.b64encode(image_content).decode('utf-8')
        return render_template("landing.html", image_data=image_data, id_image=selected_id, prompt=prompt)
    else:
        return render_template("404.html")

@app.route("/imagine/stats")
def show_stats():
    if sleep_mode:
        sleeper = "Activo"
    else:
        sleeper = "No activo"
    if queue.empty():
        stats = {
            "start_time": start_time,
            "num_loaded_prompts": num_loaded_prompts,
            "total_served": "Recopilando datos...",
            "total_images": "Recopilando datos...",
            "current_queue_size": "Recopilando datos...",
            "last_timestamp": "Recopilando datos...",
            "sleep_mode": sleeper,
        }
        
        return render_template("stats.html", stats=stats)
    else:
        imade_data = queue.queue[-1]
        last_timestamp_image = imade_data['timestamp']
        last_timestamp_image = last_timestamp_image[:-3]
        last_timestamp_image = last_timestamp_image[-5:]
        stats = {
            "start_time": start_time,
            "num_loaded_prompts": num_loaded_prompts,
            "total_served": total_served,
            "total_images": image_count,
            "current_queue_size": queue.qsize(),
            "last_timestamp": last_timestamp_image,
            "sleep_mode": sleeper,
        }
        return render_template("stats.html", stats=stats)

if __name__ == "__main__":
    try:
        print(f"Production Server: {ON_PRODUCTION}")
        thread_generate_image = Thread(target=generate_image)
        thread_generate_image.start()
        app.run(host="0.0.0.0", port=5081)
    except KeyboardInterrupt:
        thread_generate_image.join()
        print("Exiting")
