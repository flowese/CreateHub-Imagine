![create_logo](https://github.com/flowese/CreateHub-Imagine/blob/main/src/static/imgs/logo_wide.png?raw=true)

# CH-Imagine
This is the repository of the CreateHub-Imagine web application, it generates beautiful images with artificial intelligence that can be used as a presentation and images on a TV or digital photo frame among other supports.

<br><br>
🟢 See live APP: https://create.hubspain.com/imagine
<br>
🟢 See live Minimal Stats Panel: https://create.hubspain.com/imagine/stats
<br><br>

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
cd CreateHub-Imagine
pip install -r requirements.txt
```
<br>
To run the application, use the following command:
<br>

```bash
python3 src/app.py
```
<br>

## Configuration
The configuration of the application is done through the `.env` file, in this file you can change the following parameters:

```bash
ON_PRODUCTION = False # If True, the application will be run in production server mode
HSP_APIKEY = "HUBSPAIN_APIKEY"
```
<br>

<br>
The main path where images are displayed is: http://localhost:5081/imagine
<br>
Each image has a unique identifier, which can be seen by scanning the QR code or clicking on the image. By clicking on the image or scanning the QR, you will be redirected to the image page where it can be downloaded.
<br>
There is a mini server status dashboard available at: http://localhost:5081/imagine/stats
<br>

### Requirements
In order to run the application, it is necessary to have Python 3.8 or higher installed.
<br>

### License
This project is licensed under the MIT license. For more information, see the [LICENSE]('https://github.com/flowese/CreateHub-Imagine/blob/main/LICENSE') file.
<br>

### Author
This project has been developed by [@flowese]('https://github.com/flowese').
