## Task Manager

This is an API task manager service. You can create and altered task.

## Getting Started

You need to download project from here, GitHub.

### Prerequisites

You need to install docker, and docker-compose. All necessary instructions you can find here:
https://www.docker.com/

### Installing

After you downloaded project and install docker-compose, you need to enter a terminal and go 
to main project directory. Then you run:
```
docke-compose up
```
or
```
sudo docke-compose up
```
if you getting error about permissions.

## Adding some data to test and play

Firs of all you need to aply migrations. For this action you need to know your container ID.
Run this command:
```
(sudo) docker container ls
```
and you find some containers running. We need container with IMAGE name task_manager_web and copy ID.
Then you need to run this:
```
docker container exec -ti <your container id> python manage.py migrate
```
After that, if you want some preset data, you have it in this repositories. To apply it, you need to run this:
```
docker container exec -ti <your container id> python manage.py loaddata fixtures.json
```
Now you have test superuser with this credentials: 
  username: user 
  password: user
and some data.
You can add some data with localhost:8000/admin

If you don't want use fixtures or you want add your own superuser, you need to run this:
```
docker container exec -ti <your container id> python manage.py createsuperuser
```

Good luck and have fun!
## Instructions to use API

In this manager you can interact with two models: Task and HistoryTask. 
First model is for creating, editing and deleting tasks. Second - for watching history of task editing.

To interact with this service you need to register. 
Make POST request to: http://localhost:8000/api/v1/user/registration/ with your account credentials (username, passwod).
Then you need authorization. Make POST request to: http://localhost:8000/api/v1/token/ and you have received your token for access in field 'access'. To interact with service you need to add HEADER parameter to all your requests. ('Authorization': 'Bearer ')

For getting all your tasks, you need to go to: http://localhost:8000/api/v1/tasks/ with GET request.
For getting single task, you need to go to: http://localhost:8000/api/v1/tasks/<task_id>/ where task_id is id, which you can get in previous paragraph.

To create a task, you need to make a POST request to: http://localhost:8000/api/v1/tasks/ with this parameters: 
* 'title' : <title of your task> 
* 'description': 
* 'status':<one of this: New, Planned, In work, Done. Default: New> 
* 'finish_date':
To editing a task, you need to make a PATCH request to: http://localhost:8000/api/v1/tasks/<task_id>/ where task_id is id of task wich you wanna edit.
  
To deleting a task, you need to make a DELETE request to: http://localhost:8000/api/v1/tasks/<task_id>/ where task_id is id of task wich you wanna delete.

To access a history of a task, you need to know ID of this task, then you need to make GET request to: http://localhost:8000/api/v1/history/<task_id>/ 

To history you can only make GET request. You can't altered history.

Good luck and have fun with this services.


## Authors

* **Pavel Chuykin** - *Initial work* - (https://github.com/p1chkn)
* job offers: p7chkn@yandex.ru

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
