# Background 
This flask app is a demo as part of a larger architecture for a project to improve public transport navigation for dementia patients.
The Station service here takes in 3 parameters: current MRT stop, starting MRT stop and ending MRT stop. It then finds the shortest path using Djikstra's/ uniform cost algorithm. Finally, it responds with the appropriate course of action or lack thereof for the passenger at the current stop. The stops are represented in their MRT station code, such as EW 4 for Tanah Merah. You can view all the stops represented in sgMrt.py

|File| Purpose|
|----|----|
|demo.py| simplified demonstration of the algorithm logic from MRT_Classes.py|
|MRT_Classes.py| defines classes and methods used. This includes Station which represents an MRT station and MetroMap, which represents the graph that links each station as a node|
|station_reader.py| Flask app that wraps the functionalities from MRT_Classes and returns appropriate HTTP responses|
|requirements.txt| Defines required libraries. Only Flask is not bundled with python3 by default|
|sgMrt.py| Loads the Singapore MRT system map as a dictionary of tuples |
|Dockerfile| Containerize the image |

This serves simply as a demo and provides a base to add on to the overall architecture, which also includes Platform service, Address service and SMS service.

|Service| Purpose|
|----|---|
|Station| Contains the logic for path finding and decision-making on behalf of the passenger|
|Address| Takes in a token ID and returns queried items such as the registered home station for the passenger, their last seen station, timestamps, phone number|
|SMS| Wrapper for a text service. Can be replaced by off-the-shelf APIs such as Twilio |

This readme will be updated with the project slides, video pitch and more services as the project continues.

# Installation 

## Docker
Do install docker to run this before hand. Alternatively you can navigate to station_reader.py and run it on your preferred IDE as a flask app.
Flask is also required on top of Python 3.9 or later. To install Flask:

Mac: `python3 -m pip install flask`

Windows: `python -m pip install flask`

If you intend to use Docker instead, you can skip this step.
You can install Docker at the following URLs:

[Linux](https://docs.docker.com/desktop/install/linux-install/)

[MacOS](https://docs.docker.com/desktop/install/mac-install/) for both x84_64/amd64 and arm64

[Windows](https://docs.docker.com/desktop/install/windows-install/)

## Local install
If you have the files installed locally, first navigate to the folder with the Dockerfile. Then, run 

`docker build -t station .`

This builds the container image. Then, run 

`docker run -p 4000:5000 station`

## Via Dockerhub
If you want to pull the image via Dockerhub directly, run 

`docker pull pochienlin/station:1.1` 

to get the image. Then, run 

`docker run -p 4000:5000 pochienlin/station:1.1` 

to run the container

# Usage
The endpoint for the Station service is /checkStop and the request body comprises current_code: str, start_code: str, end_code: str.
Here is a sample from the Postman Collection in the repo:

```
[POST] http://127.0.0.1:4000/checkStop

[REQUEST BODY]
{
    "current_code": "CG 2",
    "start_code": "CG 1",
    "end_code": "EW 10"
}
```

If you get ERROR 415 Unsupported Media, do add Content-Type as application/json in headers. 

It is recommended to use Postman to test this for the best experience. You can download Postman on your preferred device [here](https://www.postman.com/downloads/). The collection in the repo can be imported to run different test cases.