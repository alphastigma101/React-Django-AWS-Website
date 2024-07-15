#### Table Of Contents
1. [Introduction](#introduction)

2. [System Requirements And Software](#system-requirements-and-software)

3. [Running The App](#running-the-app-automatically-or-manually)

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


### Running the App Automatically Or Manually  
* Install dependencies with `npm install`. Note that there may be deprecated dependencies or it saying vulernable packages detected. You can ignore that if and only if talks about **nth-check** as the package.json file is structured in a way where it tests the product `dependencies` and the development `dependencies`. You can view this source here for more info: **https://stackoverflow.com/questions/71781795/react-npm-inefficient-regular-expression-complexity-in-nth-check**. You can also execute `deploy-app.sh` by she-banging it like so `deploy-app.sh` which will deploy the app

* Start the app **on your client machine**, issue `npm start` and follow prompts to view the code running in a browser.

* Open a **new terminal** and execute these commands to set it up inside the repo folder that was cloned: 
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



### Configuring React App For AWS (Front-End)
* In order to deploy your app, you need to run `npm run build` which will build the `index.html` file. 
* To set up your react on the front end, you will use **S3** which is a bucket, you need to also enable **static web hosting** once you're done creating the bucket, and set policies for it.
* Here is my app product link: *http://react-tictacktoe.s3-website-us-west-2.amazonaws.com/*

* In order to launch and deploy your front-end code, you need to create a IAM policy for it and add the user to it. You will get something like this:
```

```
* Once you're done, give it a name. Mine is `CreateAndManageKeys`, and add it to a IAM user. You can simply create one by going to settings and clicking on *IAM/User* in your settings
* Create the IAM user with the default options and you should see a link that allows you to create the access key for that IAM user.
* You also need to add the newly created user to group and attached your newly created policy to it and add the user to it.
* From there on, you want to execute this command in your client's terminal:
```
    aws configure 
```
* **You should get something like this:** 
```
    AWS Access Key ID [None]: <aws_access_key_id> 
    AWS Secret Access Key [None]: <aws_secret_access_key>
    Default region name [None]: us-west-1 
    Default output format [None]: json
```
* Copy your access key into the terminal, press enter, and copy your secret key into it again, and press enter.
* For the region, I went with *us-west-1*



* To keep updating your app from the cli, you can do this: 
```
    aws s3 sync <folder_path> s3://name-of-bucket
```
* My bucket name is `s3://react-tictacktoe`, and I want to upload my `build` folder's **files** and my **src** folder as well. 
* **NOTE:** index.html must be at the top-level directory meaning it should not be inside a folder

** **Sources:**
    * **Creating And Managing Access Keys For IAM**:
        * *https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html*
    * **Creating Your First Policy**
        * *https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-iam-policy.html*

### Setting Up The BackEnd

* **Sources:**
    * *https://awstip.com/host-back-end-environment-in-aws-ec2-d254bc4135e4*



### Sources

* **ReactDOM**:
    * *https://legacy.reactjs.org/docs/react-dom.html*
* **React**:
    * *https://legacy.reactjs.org/docs/react-api.html*
