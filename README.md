# TMS [Timetable Management System]

## Functions (func.py)
 ### Timetable sort Algorithm 
  - Init -> creates a sample DB sData[], appends "Subject" for (sub_priority * No: of classes) times into sData[]
  - Process -> Gets a random "Subject" from sData, check if it matches the given timetable column and other criterions(*), if not chooses another "Subject" randomly (repeats process till condition satifies.)

[Refer func.py for detailed codewise explanation.]

## Web (web.py)
  - GUI is a website interface. Uses flask as web server.

## Templates Folder
 - Contains all HTML templates for GUI

## Model (model.py)
- Contains model classes (Data classes) for the functions.

## Requirements
- flask [web framework]
- Flask-session
- pymongo==3.12.3 [for saving user sessions]
- py-jsonic [for serializing data classes to json]


## Getting started
    Run web.py

## Currently Deployed on heroku:
   - <a href="https://tm0.herokuapp.com">tms0.herokuapp.com</a>
