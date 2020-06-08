# Enodo Fullstack Engineering Challenge

Welcome to our Fullstack Engineering Challenge repository. This README will guide you on how to participate in this challenge.

Please fork this repo before you start working on the challenge. We will evaluate the code on the fork.


## Challenge


Front-end and backend to allow users to search, select, or unselect properties from the DB.

## Requirements
- Build frontend with Element.js and Vue.js
- Create DB from data in excel file (suggestion: Sqlite)
- Create API to interact with database (suggestion: falcon, flask, express...)
- Input field with [autocomplete](https://element.eleme.io/#/en-US/component/input#autocomplete), displaying the properties from the DB through the API.
  - On Selection of search result, save as "Selected" to DB.
- Table Showing selected properties:
  - Column 1: Full Address
  - Column 2: Class Description
  - Column 3: Delete button
- Include a delete button to unselect property from DB.
- Add a test to your implementation.
- Include a Readme on how to run your solution.

## Setup
Setup virtual environment
```
python3 -m venv env
source env/bin/activate
```

Install dependencies
```
pip3 install -r requirements.txt
```

## Run
```
python3 main.py
```

Open `index.html` to see the frontend.

## Test
```
python3 main_test.py
```