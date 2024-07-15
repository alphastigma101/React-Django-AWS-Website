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
* **NOTE:** index.html must be at the top-level directory meaning it should not be inside a folder, if you manually drap and drop them into the bucket
* Whenever you create new policies they will always be in a **json data structure** 

** **Sources:**
    * **Deploying your front end code to S3**:
        - *https://dev.to/oyetoket/how-to-deploy-your-frontend-application-on-aws-s3-31m9*
    * **Creating And Managing Access Keys For IAM**:
        * *https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html*
    * **Creating Your First Policy**
        * *https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-iam-policy.html*




### Setting Up The BackEnd
* TODO:
    * Save the rules from security group and delete them 
    * Do the same thing with the acls
    * Re-create the back end and get it to work then add back the rules



* **ACLS**
* They control how the subnets of a network communicate with eachother while the **security groups** communicate at a higher level
* **INNER BOUND RULES:**
* *<FMI>*
* **OUTERBOUND RULES**
* *<FMI>*

*https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html?icmpid=docs_ec2_console#concepts-public-addresses*
*https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-prerequisites.html#eic-prereqs-network-access*
*https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-prerequisites.html#ec2-instance-connect-setup-security-group*
*https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html*
*https://docs.aws.amazon.com/AmazonS3/latest/userguide/enabling-cors-examples.html?icmpid=docs_amazons3_console*
*https://docs.aws.amazon.com/comprehend/latest/dg/setting-up.html*
*https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html*
*https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules-reference.html#sg-rules-local-access*
* Read this: *https://dev.to/awscommunity-asean/create-and-deploy-python-django-application-in-aws-ec2-instance-4hbm*
* **Sources:**
    * *https://awstip.com/host-back-end-environment-in-aws-ec2-d254bc4135e4*

### Setting Up A Custom VPC
* To setup a custom VPC (Virtual Private Connect), which is a private network, you need to configure a security group that will be associated with it, with basic rules such as routing HTTP,HTTPS, and SSH, you also need to set up the routing table which needs to be routed to your *internet gateway*, and it needs to be attached to your vpc. 

### Setting Up A Custom VPC
* In order to create a custom VPC, you need to configure a set of rules in your *security groups* and *ACL rules*



# Sources: 
    .....

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
````
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
# Sources:
        * **Connect to your instance through SSH**:
            - *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-connect-to-instance-windows*
        * **What is a elastic Ip address**:
            - *https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html*
        * **Setting Up SSM Agent**:
            - *https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-linux.html*
            - *https://docs.aws.amazon.com/systems-manager/latest/userguide/manually-install-ssm-agent-linux.html*
        * **Attach a policy to your IAM user**:
            - *https://awstip.com/troubleshooting-failed-to-connect-to-your-instance-response-on-ec2-92428837ea4a*
        




### Sources

* **ReactDOM**:
    * *https://legacy.reactjs.org/docs/react-dom.html*
* **React**:
    * *https://legacy.reactjs.org/docs/react-api.html*
