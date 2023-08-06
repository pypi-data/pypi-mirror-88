
# applauncher module

## Description
The applauncher module defines a standard way to launch and manage a basic application.

## Configuration class
**Configuration** class defines a standard logger which prompts in console and save log in a dated file.
I also define a standard way to configure the app with a settings file in yml format. 
This yml file is a key/value pair collection and allows substitution of values using the syntax {key}

Here is an example of yml file:

    mykey: myvalue
    value_to_substitute: '{otherkey}'
    otherkey: 3
    listkey:
        - key1: value1
        - key2: value2
    dictkey:
        key: value
        otherkey: othervalue
    booleankey: true

## Settings class
**Settings** is a class for which attributes are defined by the given dictionary

## error function
**error** function defines a standard error behaviour by displaying an error and exiting the app