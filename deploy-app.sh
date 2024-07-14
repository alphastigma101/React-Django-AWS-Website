#!bin/bash

###################################
# Update the dependencies of the app
###################################
# Note: There is a bug going on with npm audit so if you run npm audit and it outputs nth-check, ignore it
# Source: https://stackoverflow.com/questions/71781795/react-npm-inefficient-regular-expression-complexity-in-nth-check
npm update 
# Check to see if there are any vulernabilities in dependencies
# Note: If any vulernablities are detected when running npm audit --production or npm audit --omit=dev, there is an issue that needs to be fixed
npm run predeploy


# If everything runs smoothly, execute the app
# Start the app from your client 
npm start
