# Requirements

## Run locally

Run `pip install requirements.txt` to install all the needed libraries to run the app.
Then type in the terminal `flask run` or `python app.py` that will run the flask API.

**Note:**  
Make sure you run the model notebook to generate the model files you will need to run the app.

## Run the docker

- Build the docker first : `docker build -t demo-flask:v0 .`
- Run the docker : `docker run -p 8501:8501 demo-flask:v0`
- To test the app visit :  `http://localhost:5000`  

## Troubleshooting for docker  

- Check the docker file currently running: `docker ps`
- Shut down the docker container: `docker stop container_id`
- Check if the port is already used: `lsof -i tcp:8501`
- Kill currently running process: `kill -9 7240`

