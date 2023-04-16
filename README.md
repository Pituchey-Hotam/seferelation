# Welcome
This project is tool to recommend you what to learn. 

# Developers Installation
First clone this repository and go to the clone directory. 

Install dependencies:

python3 is required. then run: 
```bash
sudo pip install -r src/requirements.txt
sudo pip install -e src/
```

Now you can run the api server with the graph in it by running: 
```bash
cd src
uvicorn apiserver:app
```