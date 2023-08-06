# Assistant
So guys this module will help you to create your own Assistant with the minimum lines of code.


## Installation
```pip install assistant```


## How to use it?
First install this module then create a python file. Import ```from personal.assistant import Assistant,run``` or ```from assistant import *``` after that create a class and inherite the ```Assistant``` class. After that you have to initialize some variables for example 


```
#create a class 

class ClassName(Assistant):
    name = YourName  #By default name is user
    voice = male or female  #By default voice version is male   
    path = Path to save text files  #By default it's current working directory.
    wait = Time in seconds to to mute the Programme  #By default it is 10 seconds
    duration = Voice recording time in seconds  #By defaukt recording time is 10 seconds
    code = Name of code editor #By default it is None
    mails={}  #mails name with their email address
    my_mail = None  #your email address and it should be less secured on becuase it uses SMTP
    my_password = None  #your given email password 


# Create a object of the class

class_object = ClassName()

# call the run function and pass the class object

run(class_object)

#And enjoy with your personal Assistant :)
```


## Errors

there are some chances to get some errors for example 
you can get a error while installing the this module like ```pyaudio``` wheel file is not installing as same in ```psutils``` because many of users face these type of errors so you can separately download wheel files form ```https://www.lfd.uci.edu/~gohlke/pythonlibs/``` and then install them. this method can pull you out from this problem. if you face any other type of problem contect me by mail i will try to solve your problem ,Thanks for using this module :)


## License

© 2020 Govind Potdar

This repository is licensed under the MIT license. See LICENSE for details.
