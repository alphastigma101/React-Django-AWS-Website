#### Table Of Contents
1. [Introduction](#introduction)
2. [System Requirements And Software](#system-requirements-and-software)
3. [Learn React](#react)
    - [Sources](#react-sources)
4. [Running My App Locally](#running-the-app-locally)
    - [Sources](#local-sources)
5. [Configuring React App For AWS (Front-End)](#configuring-react-app-for-aws-(Front-end)) 
    - [Front End Configuration Sources](#front-end-configuration-sources)
6. [Setting Up The BackEnd on AWS](#setting-up-the-backend-on-aws)
    - [ACLS And Security Groups](#acls-and-security-groups)
    - [BackEnd Sources](#backend-sources)
7. [Setting Up A Custom VPC](#setting-up-a-custom-vpc)
    - [FMI](#..)
    - [FMI](#..)
8. [Automatically Deploying Your App On The BackEnd](#automatically-deploying-your-app-on-the-backend)
    - [Sources](#automatically-deploying-your-app-resources)
    - [TroubleShooting Auto Deployment](#troubleShooting-auto-deployment)
9. [TroubleShooting your VPC](#troubleshooting-your-vpc)
    - [Verifying Your Routing Table](#verifying-your-routing-table)
    - [Sources](#vpc-troubleshooting-resources)

* ----------------------------------------------------------------------------------------------

### Introduction
```
    The purpose of this public repo is to demostrate my knowledge of Django and React.js. The goal is to build an app using React.js for the front-end and Django as its backend. I am using existing code that you can copy from the react website itself called TickTackToe, but my version is a modified to include two additional components. The purpose of this is to show that I understand components and organization skills.
```

#### System Requirements And Software
* Install **Node.js** on for **your distribution** and **npm** or find an alternative solution such as **yarn**. If yarn does not work for you, you can utilize this guide: *https://linuxize.com/post/how-to-install-node-js-on-ubuntu-20-04/* here for more information. The simple commands you need to run to install nodejs and npm is:
```
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
```
* **Note:** I am assuming that `/etc/apt/keyrings` already exists, if not, then issue this command: `sudo mkdir -p /etc/apt/keyrings`
* Install **pip** and **python3** and **python3-venv** for a virtual environment


### React

* The key core of react apps are the `components`. They can  render in html code which is called JSX. They have the same functionality of setters and getter methods but can be modfied to do more than that. 

# React Sources
* **ReactDOM**:
    * *https://legacy.reactjs.org/docs/react-dom.html*
* **React**:
    * *https://legacy.reactjs.org/docs/react-api.html*
* ----------------------------------------------------------------------------------------------

### Running the App Locally 
* Install dependencies with `npm install`. Note that there may be deprecated dependencies or it saying vulernable packages detected. You can ignore that if and only if talks about **nth-check** as the package.json file is structured in a way where it tests the product `dependencies` and the development `dependencies`. You can view this source here for more info: **https://stackoverflow.com/questions/71781795/react-npm-inefficient-regular-expression-complexity-in-nth-check**. 

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

* Once you're done, you can run `npm run build`
# Local Sources
* **COORSHEADERS**:
    * *https://www.bezkoder.com/react-redux-crud-example/*
* **React Component Examples**
    * *https://legacy.reactjs.org/docs/components-and-props.html*
    * *https://react.dev/reference/react/useState#adding-state-to-a-component*


* ----------------------------------------------------------------------------------------------


### Configuring React App For AWS (Front-End)
* In order to deploy your app, you need to run `npm run build` which will build the `index.html` file. 
* To set up your react on the front end, you will use **S3** which is a bucket, you need to also enable **static web hosting** once you're done creating the bucket, and set policies for it.

* Create the IAM user with the default options and you should see a link that allows you to create the access key for that IAM user. You can do this by creating a custom policy or assign one that is already made to your IAM user. Once you made your IAM account, you want to execute this command in your client's terminal:
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
* **NOTE:** index.html must be at the top-level directory meaning it should not be inside a folder, if you manually drap and drop them into the bucket
* Whenever you create new policies they will always be in a **json data structure** 

# Front End Configuration Sources
* **Deploying your front end code to S3**:
    - *https://dev.to/oyetoket/how-to-deploy-your-frontend-application-on-aws-s3-31m9*
* **Creating And Managing Access Keys For IAM**:
    - *https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html*
* **Creating Your First Policy**
    - *https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-iam-policy.html*


* ----------------------------------------------------------------------------------------------

### Setting Up The BackEnd on AWS
* In order to set up your back end code for automatic deployment:
* you need to create an EC2 instance
* Attach a VPC to it [Setting Up A Custom VPC](#setting-up-a-custom-vpc)
* a security group needs to be associated with it,
* A couple of ACL/Security Group rules added to it. 
* And you need to create a IAM user. 
* You also need a Elastic IP Address which you can create by visiting EC2 and look to the left panel until you see elastic, or you can generate one and attach your instance to it

* The ACL rules are quite simple such as all you really need to do is create one in-bound rule that allows all incoming traffic and create the same exact rule but for the out-bound rule. Make sure that 

# ACLS And Security Groups
* They control how the subnets of a network communicate with eachother while the **security groups** communicate at a higher level
* **INNER BOUND RULES:**
* *<FMI>*
* **OUTERBOUND RULES**
* *<FMI>*

# BackEnd Sources
* **Setting premissions for your IAM**
    * *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-configure-IAM-role.html*
* *https://awstip.com/host-back-end-environment-in-aws-ec2-d254bc4135e4*
* *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html?icmpid=docs_ec2_console#concepts-public-addresses*
* *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-prerequisites.html#eic-prereqs-network-access*
* *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-prerequisites.html#ec2-instance-connect-setup-security-group*
* *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html*
* *https://docs.aws.amazon.com/AmazonS3/latest/userguide/enabling-cors-examples.html?icmpid=docs_amazons3_console*
* *https://docs.aws.amazon.com/comprehend/latest/dg/setting-up.html*
* *https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html*
* *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules-reference.html#sg-rules-local-access*

* ---------------------------------------------------------------------------------------------

### Setting Up A Custom VPC
* To setup a custom VPC (Virtual Private Connect), which is a private network, you need to configure a security group that will be associated with it, with basic rules such as routing HTTP,HTTPS, and SSH, you also need to set up the routing table which needs to be routed to your *internet gateway*, and it needs to be attached to your vpc. 


* --------------------------------------------------------------------------------------------

### TroubleShooting your VPC
* When using the query command, you can modify the json structure and filter out what you want to see like so:
```
 --query "string,Ebs={DeleteOnTermination=boolean,VolumeId=string},NoDevice=string,VirtualName=string}"

       JSON Syntax:

          [
            {
              "DeviceName": "string",
              "Ebs": {
                "DeleteOnTermination": true|false,
                "VolumeId": "string"
              },
              "NoDevice": "string",
              "VirtualName": "string"
            }
            ...
          ]

```
# Verifying Your Routing Table
```
    It is good practice that your routing table routes all your network traffic to your gateway. Which in this case for AWS, your gateway would be igw-xxxxxxxx
    This section will give you steps to verify that your routing table is indeed set up correctly. This section will only have AWS CLI steps, so if you're using the AWS GUI, you can visual check and see if your routing table is properly connected
```
    * Enter the command after you have issued `aws configure`:
        ```
            aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<your-vpc-id>"
        ```
    * **NOTE:** The command above will output a json structure that will show you your vpc network id and the name **which is needed** for the next step
    * This should help you verify to see if your routing table is set up correctly
    * ---------------------------------------------------------------------------------------------------------------------------------------------------
    * **Section:** Check and see if your VPC is connected to your instance
        * To check to see if your instance is connected to your VPC, you need its Id:
        ```
            aws ec2 describe-instances --query "Reservations[*].Instances[*].{ID:InstanceId}"
        ```
        * Once you obtain your Id, issue this command:
        ```
            aws allocate-address --region <your region>
        ```
        * Copy and paste the Id into here:
        ```

        ```
# Trouble Shooting Sources:
        * **Connect to your instance through SSH**:
            - *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-connect-to-instance-windows*
        * **What is a elastic Ip address**:
            - *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html*
        * **Setting Up SSM Agent**:
            - *https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-linux.html*
            - *https://docs.aws.amazon.com/systems-manager/latest/userguide/manually-install-ssm-agent-linux.html*
        * **Attach a policy to your IAM user**:
            - *https://awstip.com/troubleshooting-failed-to-connect-to-your-instance-response-on-ec2-92428837ea4a*
        
* --------------------------------------------------------------------------------------

### Automatically Deploying Your App On The BackEnd

* Issue this command: `sudo nano /etc/systemd/system/gunicorn.service` and copy the code below and modify it so it points to the *wsgi* python module:

```
    [Unit]
        Description=gunicorn daemon
        Requires=gunicorn.socket
        After=network.target

    [Service]
        User=ubuntu
        Group=ubuntu
        WorkingDirectory=/home/ubuntu/<PROJECT-NAME>
        ExecStart=/home/ubuntu/React-Django-AWS-Website/venv/bin/gunicorn \
            --access-logfile - \
            --workers 3 \
            --bind unix:/home/ubuntu/React-Django-AWS-Website/gunicorn.sock \
            <PROJECT-NAME>.wsgi:application

    [Install]
        WantedBy=multi-user.target
```
* **NOTE:** My project name is `TicTackToe` So I would place `PROJECT_NAME` with it 


* Run this command: `sudo vim /etc/systemd/system/gunicorn.socket` and copy this code: 
```
    [Unit]
        Description=gunicorn socket

    [Socket]
        ListenStream=/home/ubuntu/<PROJECT_NAME>/gunicorn.sock

    [Install]
        WantedBy=sockets.target
```
* **NOTE:** By making the gunicorn not in */run* where it normally should be at, this avoids premission issues and you're not doing anything sensitive with it so it should be fine
* **NOTE:** change `PROJECT_NAME` to your actually project name and change the **/home/ubuntu** to your actual user for both of those files

* Issue these commands: 
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
* Check the socket status just in case: 
```
    sudo systemctl status gunicorn.socket
```
* Issue this command: `sudo vim /etc/nginx/sites-available/<YOUR-PROJECT-NAME>` and add the following code into the file you created and modify it :
```
server {
    listen 80;
    server_name YOUR_INSTANCE_ELASTIC_IP_ADDRESS;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/<YOUR-PROJECT>;
    }
    location /media/ {
        root /home/ubuntu/<YOUR-PROJECT>;    
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/React-Django-AWS-Website/gunicorn.sock;
    }
}
```
* Check it: 
```
    sudo nginx -t
```

* Link it:
```
sudo ln -s /etc/nginx/sites-available/<YOUR-PROJECT-NAME> /etc/nginx/sites-enabled

```
* Restart `nginx` and visit the elastic ip address:
```
    sudo systemctl restart nginx
```

* **NOTE:** Whenever you shutdown your instance, you need to restart your gunicorn.service file. A bash script can be created that will automatically executed on the user level if needed.
# Automatically Deploying Your App Resources
* **Automaticall Setting Up Back End Code with gunicorn and wsgiserver**
    - *https://realpython.com/django-nginx-gunicorn/#starting-with-django-and-wsgiserver*
* **Deploying Back End Code:**
        * **NOTE**: The guides below are a bit out dated such as you don't really need to create all the in-bound/out-bound rules
        * *https://dev.to/awscommunity-asean/create-and-deploy-python-django-application-in-aws-ec2-instance-4hbm*
        * *https://dev.to/rmiyazaki6499/deploying-a-production-ready-django-app-on-aws-1pk3#installing-dependencies*
    * **Perks Of Creating .socket Inside The Root Of Your Project:**
        * You avoid premission errors which is very crucial when it comes to back end deployment
        * *https://pythoncircle.com/post/697/hosting-django-app-for-free-on-amazon-aws-ec2-with-gunicorn-and-nginx/*


# TroubleShooting Auto Deployment
* If you run into **bad gateway 502**, you need to change the user to **root** inside the `nginx.conf` file. More info here: *https://stackoverflow.com/questions/70111791/nginx-13-permission-denied-while-connecting-to-upstream*
 

