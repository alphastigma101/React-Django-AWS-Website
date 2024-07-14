#### Table Of Contents
1. [Introduction](#introduction)

2. [System Requirements And Software](#system-requirements-and-software)

3. [Running The App](#running-the-app)

4. [Sources](#sources)




### Introduction
```
    The purpose of this public repo is to demostrate my knowledge of Django and React.js. The goal is to build an app using React.js for the front-end and Django as its backend.
```

#### System Requirements And Software
* Install **Node.js** on for **your distribution** and **npm** or find an alternative solution such as **yarn**. If yarn does not work for you, you can utilize this guide: *https://linuxize.com/post/how-to-install-node-js-on-ubuntu-20-04/* here for more information. The simple commands you need to run to install nodejs and npm is:
```
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
```
* **Note:** I am assuming that `/etc/apt/keyrings` already exists, if not, then issue this command: `sudo mkdir -p /etc/apt/keyrings`
* Install **pip** and **python3** and **python3-venv** for a virtual environment


### Running the App  
* Install dependencies with `npm install`. Note that there may be deprecated dependencies; this app is simple and **non-critical**. If dependencies complain about being deprecated, I have tried to fix the errors. Nevertheless, this app remains vulnerable, though it does not contain sensitive information or will it ever.

* Start a **local server** with `npm start` and follow prompts to view the code running in a browser.

* Open a new terminal and execute these commands to set it up inside the repo folder that was cloned: 
```
    python3 -m venv venv
    source venv/bin/active
    pip install --no-cache -r TicTackToe/requirements.txt
```
* **Note:** If *venv/bin* does not exist, you need to find a folder that points to active inside venv 

* Then issue this command to start the app: 
```
    cd TicTackToe
    python3 manage.py runserver

```
* **NOTE:** You can copy either all of them or copy just one at a time
* **http://127.0.0.1:8000/polls/start_game** *To see Django's api history endpoint*
* **http://localhost:8000/logging** this is to view  *Django's api logging* 
* **http://localhost:8000/winner** this is to view *Django's winner apie endpoint*

* **Sources:**
* **COORSHEADERS**:
    * *https://www.bezkoder.com/react-redux-crud-example/*
* **React Component Examples**
    * *https://legacy.reactjs.org/docs/components-and-props.html*
    * *https://react.dev/reference/react/useState#adding-state-to-a-component*

### Sources

* **ReactDOM**:
    * *https://legacy.reactjs.org/docs/react-dom.html*
* **React**:
    * *https://legacy.reactjs.org/docs/react-api.html*
