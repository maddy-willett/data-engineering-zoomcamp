# Module 1 Homework: Docker & SQL (Answers & Explainations)

### Question 1. Understanding Docker images

When running a docker image with the `python:3.13` image and the entrypoint set to `bash`, the version of `pip` in the image is: *pip 25.3*

How did I do this? 
* First I ran the command `docker run -it --entrypoint=bash python:3.13` which starts an interactive container from the `python:3.13` image and overrides the default command to open in a Bash shell. 
* Second I ran the command `pip --version` which then prints the version of `pip` installed inside the container!


### Question 2. Understanding Docker networking and docker-compose

