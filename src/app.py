from PIL import ImageDraw, Image
import qrcode, random, json, time, uuid, os, dotenv, datetime, base64
from threading import Thread
from hubspain.generation import stablediffusion
from flask import Flask, render_template
from queue import Queue
from io import BytesIO

app = Flask(__name__)
queue = Queue()
images_dict = {}
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
dotenv.load_dotenv(dotenv.find_dotenv())
hsp_apikey = os.getenv("HSP_APIKEY")

def generate_image():
    while True:
        if queue.qsize() < 10:
            with open('static/data/prompts.txt', 'r', encoding='utf-8') as f:
                PROMPT_LIST = f.readlines()
            selected_prompt = random.choice(PROMPT_LIST)
            with open('static/data/submit_dict.json', 'r') as fp:
                submit_dict = json.load(fp)
            params = submit_dict['params']
            submit_dict = {
            "prompt": selected_prompt,
            "params": params,}
            images = stablediffusion(hsp_apikey,submit_dict=submit_dict)
            for i, image in enumerate(images):
                id_image = str(uuid.uuid4())
                image_data = {
                    "image": image,  # guarda la imagen original en el diccionario images_dict
                    "prompt": selected_prompt
                }
                images_dict[id_image] = image_data
                # add image to buffer
                image_buffer = BytesIO()
                image.save(image_buffer, format="PNG")
                image_buffer.seek(0)
                # add qr code to image from buffer
                img_toqr = Image.open(image_buffer)
                img_toqr = draw_qr_code(img_toqr, id_image)
                # add image to queue
                queue.put(img_toqr)
                print(f"{timestamp} - (Imagen generada) Cola actual: {queue.qsize()} imágenes")
            time.sleep(1)
        else:
            print(f"{timestamp} - (Cola llena) Cola actual: {queue.qsize()} imágenes")

def draw_qr_code(image, id_image):
    size = image.size
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6, 
        border=2)
    qr.add_data(f"https://create.hubspain.com/image/{id_image}")
    qr.make(fit=True)
    img = qr.make_image(back_color="white", fill_color="black")
    img_draw = ImageDraw.Draw(image)
    corner_x = size[0]
    corner_y = size[1]
    img_draw.bitmap((corner_x - 255, corner_y - 250), img)
    return image

@app.route("/imagine")
def show_image():
    if queue.empty():
        return render_template("loading.html")
    else:
        image_bytes = queue.get()
        for id_image, image_data in images_dict.items():  # recorre el diccionario images_dict
            if image_data['image'] == image_bytes:  # si encuentra la imagen actual en images_dict
                break  # sale del bucle
        print(f"{timestamp} - (Imagen servida) Cola actual: {queue.qsize()} imágenes")
        buffer = BytesIO()
        image_bytes.save(buffer, format="PNG")
        buffer.seek(0)
        image_content = buffer.getvalue()
        image_qr = base64.b64encode(image_content).decode('utf-8')
        return render_template("image.html", image_qr=image_qr, id_image=id_image)  # se pasa el id_image a la plantilla HTML

@app.route("/image/<id_image>")
def show_unprocessed_image(id_image):
    if id_image not in images_dict:
        return render_template("404.html")
    else:
        image_data = images_dict[id_image]  # obtiene la imagen original del diccionario images_dict
        selected_id = id_image
        prompt = image_data['prompt']
        image_original = image_data['image']  # obtiene la imagen original del diccionario images_dict
        buffer = BytesIO()
        image_original.save(buffer, format="PNG")  # guarda la imagen original en el buffer
        buffer.seek(0)
        image_content = buffer.getvalue()
        image_data = base64.b64encode(image_content).decode('utf-8')
        return render_template("landing.html", image_data=image_data, id_image=selected_id, prompt=prompt)


if __name__ == "__main__":
    try:
        thread = Thread(target=generate_image)
        thread.start()
        app.run(host="0.0.0.0", port=8501)
    except KeyboardInterrupt:
        thread.join()
        print('exit')