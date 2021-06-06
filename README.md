# framework_design_for_graduate_applications

## Command

1 - Build and run the app with Compose
```
$ docker-compose up --build -d
```

2 - Restore the graduate database
```
$ docker exec -i mysql_db mysql -uuser -ppassword graduate < graduate.sql
```

3 - Give permission for GUI Display
```
$ xhost +local:docker
$ export DISPLAY=$DISPLAY
```
4 - Run the docker
```
$ docker run -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix python
```
5- Exec the python3 container
```
$ docker-compose exec python3 bash
```
6- Run the project
```
$ python3 app.py
```



/////////////////////////////////////////////////////////////////////////////////////////////////
## MYSQL CONTAINER
Run a command in 'mysql_db' container
```
$ docker-compose exec mysql_db bash
```
access mysql
```
$ mysql -u user -h mysql_db -D graduate -ppassword
```
## PYTHON CONTAINER
Run a command in 'python' container
```
$ docker-compose exec python3 bash
```
Run the project
```
$ python3 app.py

```
## EXTRA INFORMATION
If you started docker using sudo , then you should run docker-compose up with sudo Like: 
```
$ sudo docker-compose up
```


