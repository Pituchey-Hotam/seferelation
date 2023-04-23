# Welcome
This project is tool to recommend you what to learn. 

# Developers Installation
First clone this repository and go to the clone directory. 

Install dependencies:

python3 is required.
To install other requirements run: 
```bash
sudo pip install -r src/requirements.txt
sudo pip install -e src/
```

You can generate the graph-model from the sefaria source sheets by running:
```bash
cd src/seferelation
python main.py
```
Or download and put it in the `src/seferelation` directory. Contact me if you want to download. 

Now you can run the api server with the graph in it by running: 
```bash
cd src
uvicorn apiserver:app
```