# currency_viewer
Service for working with currency rates of the Central Bank of the Russian Federation

## Necessary requirements
- Python 3.11

## Project setup
### SSH-key setup
To download the repository, you need to create an SSH key and add it to your account according to [instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
).

Now you can clone the repository using SSH
```
$ git clone git@github.com:Valentina-Gol/currency_viewer.git
```
### Python virtual environment
To run the project locally you need to set up a python virtual environment
```
$ cd currency_viewer
$ python -m venv currency_viewer_venv
```

Activate the virtual environment
- on Windows
```
$ currency_viewer_venv\Scripts\activate
```
- on macOS or Linux
```
$ source currency_viewer_venv/bin/activate
```
### Installing dependencies
Install dependencies for the service
```
$ pip install -r requirements.txt
```

## Working with the service
### Launch
Start the service using Uvicorn
```
$ uvicorn app.main:app 
```
### Interfaces
The service will be deployed at
```
http://127.0.0.1:8000
```
You can interact with the service via Swagger UI at
```
http://127.0.0.1:8000/docs
```
And also use ReDoc
```
http://127.0.0.1:8000/redoc
```

### Tests
To run the tests, run the commands
```
$ cd tests
$ pytest -v
```
