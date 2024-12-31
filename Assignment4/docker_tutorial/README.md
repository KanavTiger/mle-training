# Housing Price Prediction Docker Deployment

This repository contains the Docker setup for the housing price prediction application. The following steps were followed to build, test, and deploy the Docker container for the app.


## Steps
### 1.**Build Docker Image**
- Created a `Dockerfile` to containerize the housing price prediction web app.
- Used Python 3.9-slim as the base image and installed dependencies from `requirements.txt`.
- Configured Flask to run on port 5000.

### 2.**Test Locally**
- Built the Docker image:
```bash
    docker build -t housing-price-prediction .
```
- Ran the container:
```bash
    docker run -p 5000:5000 housing-price-prediction
```
### 3.**Create Git Branch from v0.3 Tag**
- Created a new branch from the v0.3 tag:
```bash
    git checkout tags/v0.3 -b docker-setup
```

- Committed Docker-related changes and pushed to GitHub.

- Created a Pull Request (PR) from docker-setup to the main branch.

### 4.**Push Docker Image to DockerHub**
- Tagged and pushed the image to DockerHub:
```bash
    docker tag housing-price-prediction <dockerhub-username>/housing-price-prediction:v1.0
    docker push <dockerhub-username>/housing-price-prediction:v1.0
```


### 5.**Pull and Test Docker Image**
- Pulled the Docker image from DockerHub:
```bash
    docker pull <dockerhub-username>/housing-price-prediction:v1.0
```
- Ran the container and verified the app on port 5000.

## DockerHub Link
You can access the Docker image here:
"https://packaging.python.org/en/latest/tutorials/packaging-projects/"
```bash
vbnet
    This should now be fully contained within the markdown code block, ensuring you can copy the entire file as intended. Just replace `<dockerhub-username>` with your actual DockerHub username.

    Let me know if you need anything else!
```


