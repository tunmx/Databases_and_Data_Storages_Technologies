# How to install mysql5.7 in my MacOS(Intel x86)

## 1. Install Docker

pass

## 2. Pull MySQL5.7 Docker image

Open Terminal, exec command:

```shell
docker pull mysql:5.7
```

## 3. Start a MySQL container

```shell
mkdir /Users/tunm/software/mysql57
docker run --name mysql57 -v /Users/tunm/software/mysql57:/var/lib/mysql  -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
```

- --name mysql57：Container name, my format is mysql+version
- -e MYSQL_ROOT_PASSWORD=my-secret-pw：Password of User root
- -d mysql:5.7：Use mysql:5.7 Docker Image
- -v :Local mount directory where mysql persistent files are stored
- p 3306: Exposed port

## 4. Check docker status

exec command:

```shell
docker ps
```

## 5. Connect to mysql container

Keep container running

```shell
docker exec -it mysql57 mysql -u root -p
```

Need enter password.