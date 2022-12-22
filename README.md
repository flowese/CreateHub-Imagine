![create_logo](https://github.com/flowese/CreateHub-Imagine/blob/main/src/static/imgs/logo_wide.png?raw=true)

# CreateHub-Imagine
This is the repository of the CreateHub-Imagine web application, it generates beautiful images with artificial intelligence that can be used as a presentation and images on a TV or digital photo frame among other supports.

Simply open a browser once the application is launched at the url http://localhost:5081/imagine
<br>
## Features
A queue is used to store the generated images and a thread is used to continually generate new images in the background. In addition, it has a small statistics panel to see the status of the server.
<br>

✅ Generate images with StableDiffusion.<br>
✅ QR codes for each image.<br>
✅ Web application to display images generated.<br>
✅ Page for each image with download link.<br>
✅ Minimal stats page to see the status of the server.<br>

## Installation and execution
To clone this repository, use the following command:

```bash
git clone https://github.com/flowese/CreateHub-Imagine.git
```
<br>
Once cloned, install the requirements from the `requirements.txt` file with the following command:
<br>
```bash
pip install -r requirements.txt
```
<br>
To launch the app, run the following command:
<br>
```bash
python src/app.py
```
<br>
The main path where images are displayed is http://localhost:5081/imagine
<br>
Each image has a unique identifier, which can be seen by scanning the QR code or clicking on the image. By clicking on the image or scanning the QR, you will be redirected to the image page where it can be downloaded.
<br>
There is a mini server status dashboard available at http://localhost:5081/imagine/stats
<br>
### Requirements
In order to run the application, it is necessary to have Python 3.8 or higher installed.
<br>
### License
This project is licensed under the MIT license. For more information, see the [LICENSE]('https://github.com/flowese/CreateHub-Imagine/blob/main/LICENSE') file.
<br>
### Author
This project has been developed by [@flowese]('https://github.com/flowese').
