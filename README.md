# ml-model-management-docker

## Overview
This github repo demonstrates how to use a pickle ML mode from within a Flask  (http://flask.pocoo.org/) application.


## Setup

### Download the trained model
The project doesn't include the trained & saved model (due to the model's size). A working model can be downloaded from here https://olifileexchange.blob.core.windows.net/ml-share/trained_model.pkl (537MB). After you downloaded the model, place the pkl file in the folder of the '*flask-web-app*'.

Update the code in main.py ('*flask-web-app*') and replace the placeholder ```YOUR_MODE_FILE_NAME``` with the filename of your pickle model. Your ```main.py``` file should look similar to this:

```python
with open(os.path.join(APP_ROOT, 'trained_model.pkl'), 'rb') as f:
```

> **ATTENTION**</br> 
>This sample was tested with a **Python 3.6** environment. Other versions weren't tested.

## Run

### Locally
Open a commandline navigate to folder '*flask-web-app*' and run the following command 
```python 
python main.py
```

This will start the flask web application (the link will be displayewd in your commandline window). Open a browser and navigate to that url. You should see 'Hi'. 

After you verfied that the app is running and works. Let's create a prediction. Use curl (https://curl.haxx.se/) or Postman (https://www.getpostman.com/) and send a ```POST``` request to the web app using the '\predict' path (e.g. http://localhost:5000/predict). 

Ensure that you set the request's content-type (request header) to ```application/json``` and that you provide an image url in the body. For example: 

```json
{ 
    "image_url": "https://shop.epictv.com/sites/default/files/ae42ad29e70ba8ce6b67d3bdb6ab5c6e.jpeg" 
} 
```

### Locally (Docker)

>**NOTE** </br>
>Before running the app using Docker please ensure that it successfully runs locally (outside of a container). 

#### Build the image
Open a commandline and navigate to your Flask web application folder. Execute the following command to create the Docker image.

>**Attention** </br>
>Please replace the placeholder ```YOUR_IMAGE_NAME``` with your Docker image name. Also, notice the ```.``` character at the end of the command!

```console
docker build -t YOUR_IMAGE_NAME:latest . 
```

#### Run the container
```console
docker run -d -p 5000:5000
```

#### Test the app
Open a browser and navigate to http://localhost:5000.

### Azure

#### Push the image to a Docker container registry (e.g. Docker Hub)
Since we will push the image to Docker Hub (https://hub.docker.com/), please ensure that you have a valid Docker Hub account. 

Follow the steps listed here 'https://docs.docker.com/docker-cloud/builds/push-images/' to push the image to Docker Hub 

> **Note** </br>
> Alternatively, you can also publish your Docker image to a private doker registry like Azure Container registry (https://azure.microsoft.com/en-us/services/container-registry/). 

#### Create an new '*Web App for Containers*' on Azure

> **NOTE** </br>
> For further information around '*Azure Web App for Container*' please see https://azure.microsoft.com/en-us/services/app-service/containers/

Once the image is available in the container registry (e.g. Docker Hub) please follow this tutorial https://docs.microsoft.com/en-us/vsts/build-release/apps/cd/deploy-docker-webapp#create-an-azure-web-app-to-host-a-container to create a new *Web App for Containers* on Azure.

Since we pushed the Docker image to Docker Hub (and not to Azure Container registry) please ensure that you select '*Docker Hub*' in step #3. 

Most Docker images have environment variables that need to be configured. If you are using an existing Docker image built by someone else, the image may use a port other than 80. You tell Azure about the port that your image uses by using the ```WEBSITES_PORT``` app setting. Here you need to set ```WEBSITES_PORT``` to 5000 


#### Test the app
Wait until the web app was successfully created. Then open a browser and nagivate to the Azure web app's public IP address.