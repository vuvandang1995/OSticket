# Container Storage
Có 3 kiểu Container storage

  - Layered Filesystem trong container run storage
  - Persistent Volumes trong persistent data storage
  - Registry trong image storage

## Layered Filesystem
Storage used for reading image filesystem layers from a running container state typically require IOPS and other read/write intensive operations, which leads to performance being a key storage metric. Docker adopted a layered storage architecture for the images and containers. A layered file system is made of many separate layers allowing images to be constructed and deconstructed as needed instead of creating a large, monolithic image.
Loại Storage này được sử dụng để đọc lớp filesystem image. Mỗi khi file image được tạo ra, nó sẽ được lưu dưới dạng này. Và từ đó, mỗi lần file image được updated, sự thay đổi đó tạo ra 1 lớp mới nằm lồng lên file cũ.

<img src="">

Để kiểm tra storage layered file system, sử dụng lệnh `inspect` trong docker engine

```
docker system info | grep -i "Storage Driver"
Storage Driver: overlay
```

When a docker image is pulled from the registry, the engine download all the dependent layers to the host machine. When the container is launched from an image comprised of many layers, docker uses the Copy-on-Write capability of the layered file system to add a read write working directory on top of existing read only layers.
Khi một docker image được pull từ trên docker hub về, nó sẽ được tải tất cả những lớp phụ thuộc về docker host. Khi container được chạy từ một image  bao gồm nhiều lớp update, docker sử dụng tính năng **Copy-on-write** của hệ thống tệp layer để thêm một thư mục làm việc ghi đọc trên đầu các lớp chỉ đọc hiện có.

<img src="">

Pull một image ubuntu từ docker hub về:

```
[root@clastix00 ~]# docker pull ubuntu:15.04
15.04: Pulling from library/ubuntu
9502adfba7f1: Pull complete
4332ffb06e4b: Pull complete
2f937cc07b5f: Pull complete
a3ed95caeb02: Pull complete
Digest: sha256:2fb27e433b3ecccea2a14e794875b086711f5d49953ef173d8a03e8707f1510f
Status: Downloaded newer image for ubuntu:15.04

[root@host ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              15.04               d1b55fd07600        14 months ago       131 MB
```

Các lớp images được đặt trong vùng host storage local:

```
[root@host ~]# ll /var/lib/docker/overlay
total 0
drwx------ 3 root root 17 Apr 11 13:25 863324a4a64a561da3d5f1623040dd292d079a810fd8767296ae6d6f7561b902
drwx------ 3 root root 17 Apr 11 13:25 8c56e1d6822091e11edfb1b14b586ba29788de5bcdaa00234a0b5dfa1432ff7b
drwx------ 3 root root 17 Apr 11 13:34 c154bf1e4f992ce599b497da5fb554e52d32127eb4ecc3a141cbf48331788dba
drwx------ 3 root root 17 Apr 11 13:25 e8ef46122ade93666dd7c1218580063d0f4e0869f940707b2a3cdbf7ea83e9cb
```

When a container starts, this initial read write layer is empty until changes are made by the running container process. When a process attempts to write a new file or update an existing one, the filesystem creates a copy of the new file on the upper writeable layer.

[root@host ~]# docker run --name ubuntu -it ubuntu:15.04
root@3b927950034f:/# useradd adriano
root@3b927950034f:/# passwd adriano
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
...
Unfortunately, when the container dies the upper writeable layer is removed and all its content is lost unless a new image is created while the container is living. When a new image is created from a running container, only the changes made to the writeable layer, are added into the new layer.

To create a new layer from a running container

[root@host ~]# docker commit -m "added a new user" ubuntu ubuntu:latest
sha256:e46141824bfc8118d6f960b9be1d70bb917e2b159734ee2d2d26e2336521528a

[root@host ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              e46141824bfc        2 minutes ago       132 MB
ubuntu              15.04               d1b55fd07600        14 months ago       131 MB


[root@host ~]# docker history ubuntu:latest
IMAGE               CREATED             CREATED BY                                      SIZE      COMMENT
e46141824bfc        40 seconds ago      /bin/bash                                       330 kB    added a new user
d1b55fd07600        14 months ago       /bin/sh -c #(nop) CMD ["/bin/bash"]             0 B
<missing>           14 months ago       /bin/sh -c sed -i 's/^#\s*\(deb.*universe\...   1.88 kB
<missing>           14 months ago       /bin/sh -c echo '#!/bin/sh' > /usr/sbin/po...   701 B
<missing>           14 months ago       /bin/sh -c #(nop) ADD file:3f4708cf445dc1b...   131 MB
Notice the new changed ubuntu image does not have its own copies of every layer. The new image is sharing its underlying layers with the previous image as following



All containers started from the latest image will share layers with all containers started from the first image. This will lead to optimize both image space usage and system performances.

Persistent Volumes
Containers often require persistent storage for using, capturing, or saving data beyond the container life cycle. Utilizing persistent volume storage is required to keep data persistence. As a best practice, it is recommended to isolate the data from a containers, i.e. data management should be distinctly separate from the container life cycle.

Persistent storage is an important use case, especially for things like databases, images, file and folder sharing among containers. To achieve this goal, there are two different approaches:

host based volumes
shared volumes
In the first case, persisten volumes reside on the same host where container is running. In the latter, volumes reside on a shared filesystem like NFS, GlusterFS or others. In the first case, data are persistent to the host, meaning if the container is moved to an another host, the content of the volume is no more accessible to the new container. In the second case, since the mount point is accessible from all nodes, the volume can be mounted by any container, no matter the host is running the container. The latter case provides data persistence across a cluster of hosts.

Persistent volumes are mapped from volumes defined into Dockerfile to filesystem on the host running the container. For example, the following Dockerfile defines a volume /var/log where the web app stores its access logs

# Create the image from the latest nodejs
# The image is stored on Docker Hub at docker.io/kalise/nodejs-web-app:latest

FROM node:latest

MAINTAINER kalise <https://github.com/kalise/>

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
COPY package.json /usr/src/app/
RUN npm install

# Bundle app source
COPY . /usr/src/app

# Declare Env variables
ENV MESSAGE "Hello World!"

# Define the log mount point
VOLUME /var/log

# Expose the port server listen to
EXPOSE 8080
CMD [ "npm", "start" ]
Start a container from the nodejs image creating the volume

[root@centos ~]# docker run --name=nodejs \
   -p 80:8080 -d \
   -e MESSAGE="Hello" \
docker.io/kalise/nodejs-web-app:latest
All persistent volumes are created under /var/lib/docker/volumes/ directory. Inspect the container to check the volumes used by

[root@centos ~]# docker inspect nodejs
...
"Mounts": [
      {
          "Name": "84894a09fe25f503cd0f2d3a30eaa00a08d72190a92e2568d395cea5a277c456",
          "Source": "/var/lib/docker/volumes/84894a09fe25f503cd0f2d3a30eaa00a08d72190a92e2568d395cea5a277c456/_data",
          "Destination": "/var/log",
          "Driver": "local",
          "Mode": "",
          "RW": true,
          "Propagation": ""
      } ]
...
A volume persist even if the container itself is deleted.

[root@centos ~]# docker rm -f nodejs

[root@centos ~]# ls -l /var/lib/docker/volumes/84894a09fe25f503cd0f2d3a30eaa00a08d72190a92e2568d395cea5a277c456/
total 4
drwxr-xr-x 4 root root 4096 Apr 11 16:32 _data
To manually delete a volume, find the volume and remove it

[root@centos ~]# docker volume list
DRIVER              VOLUME NAME
local               84894a09fe25f503cd0f2d3a30eaa00a08d72190a92e2568d395cea5a277c456
    
[root@centos ~]# docker volume remove 84894a09fe25f503cd0f2d3a30eaa00a08d72190a92e2568d395cea5a277c456
Persistent volumes can be created before the container and then attached to the container

[root@centos ~]# docker volume create --name myvolume
[root@centos ~]# docker volume inspect myvolume
    [
        {
            "Driver": "local",
            "Labels": {},
            "Mountpoint": "/var/lib/docker/volumes/myvolume/_data",
            "Name": "myvolume",
            "Options": {},
            "Scope": "local"
        }
    ]
[root@centos ~]# docker run --name=nodejs \
       -p 80:8080 -d \
       -e MESSAGE="Hello" \
       -v myvolume:/var/log \
    docker.io/kalise/nodejs-web-app:latest

[root@centos ~]# docker inspect nodejs
    ...
    "Mounts": [
            {
                "Type": "volume",
                "Name": "myvolume",
                "Source": "/var/lib/docker/volumes/myvolume/_data",
                "Destination": "/var/log",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ]
    ...
Note: Persistent volumes are initialized when a container is created. If the container’s parent image contains data at the specified mount point, that existing data is copied into the new volume upon volume initialization.

Persistent volumes can be mounted on any directory of the host file system. This helps sharing data between containers and host itself. For example, we can mount the volume on the /logs directory of the host running the container

[root@centos ~]# docker run --name=nodejs \
   -p 80:8080 -d \
   -e MESSAGE="Hello" \
   -v /logs:/var/log \
docker.io/kalise/nodejs-web-app:latest
Volume data now are placed on the /logs host directory.

The same volume could be mounted by another container, for example a container performing some analytics on the logs produced by the nodejs application. However, multiple containers writing to a single shared volume can cause data corruption. Make sure the application is designed to write to shared data stores.

Note: When mounting a persistent volume on a given host directory, if the container’s parent image contains data at the specified mount point, that existing data is overwritten upon volume initialization.

Registry
A Docker registry service is a storage and content delivery system containing tagged images. Main registry service is the official Docker Hub but users can build their own registry. Users interact with a registry by using push and pull commands.

[root@centos ~]# docker pull ubuntu:latest
The above command instructs the docker engine to pull the latest ubuntu image from the official Docker Hub. This is simply a shortcut for the longer

[root@centos ~]# docker pull docker.io/library/ubuntu:latest
To pull images from a local registry service, use

[root@centos ~]# docker pull <myregistrydomain>:<port>/kalise/ubuntu:latest
The above command instructs Docker Engine to contact the registry located at <myregistrydomain>:<port> to find the image kalise/ubuntu:latest

In a typical deployment workflow, a commit to source code would trigger a build on Continous Integration system, which would then push a new image to the registry service. A notification from the registry triggers a deployment on a staging environment, or notify other systems that a new image is available.

Deploy a local Registry Service
To deploy a local registry service on myregistry:5000, install Docker on that server and then start a Registry container based on the registry image provided by Docker Hub

[root@centos ~]# docker pull registry:latest
[root@centos ~]# docker run -d -p 5000:5000 --restart=always --name docker-registry registry:latest
Get an image from the public Docker Hub, tag it to the local registry service

[root@centos ~]# docker pull docker.io/kalise/httpd
[root@centos ~]# docker tag docker.io/kalise/httpd myregistry:5000/kalise/httpd
The plain registry above is considered as insecure by Docker Engine. To make it accessible, each Docker Engine host should be instructed to trust the insecure registry service running on myregistry:5000 host.

Chance the docker engine /etc/docker/daemon.json configuration file

{
  "storage-driver": "devicemapper",
  "hosts": ["tcp://0.0.0.0:2375","unix:///var/run/docker.sock"],
  "insecure-registries": ["myregistry:5000"]
}
and restart the docker engine.

Now the Docker Engine is trusting the local registry, so we can push images on it

docker push myregistry:5000/kalise/httpd
The image can be now pulled from the local registry

docker pull myregistry:5000/kalise/httpd
To secure the registry with a self-signed certificate, first create the certificate

mkdir /etc/certs
cd /etc/certs
openssl req \
-newkey rsa:4096 -nodes -sha256 -keyout domain.key \
-x509 -days 365 -out domain.crt
Make sure the Common Name parameter matches the host name myregistry given to the host registry.

Now each Docker engine needs to be instructed to trust this certificate.

mkdir -p /etc/docker/certs.d/myregistry:5000
cp /etc/certs/domain.crt /etc/docker/certs.d/myregistry:5000/ca.crt
Remove the insecure registry set in the previous step by changing the /etc/docker/daemon.json configuration file

{
  "storage-driver": "devicemapper",
  "hosts": ["tcp://0.0.0.0:2375","unix:///var/run/docker.sock"],
}
and restart the Docker Engine.

Start the registry in secure mode passing the certificate as local volume and setting the related envinronment variables to the container

docker run -d -p 5000:5000 --restart=always --name docker-registry \
  -v /etc/certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  registry:latest
Now we can push/pull images to/from the local registry

docker push myregistry:5000/kalise/httpd
docker pull myregistry:5000/kalise/httpd
Storage backend for registry
By default, data in containers is ephemeral, meaning it will disappears when the container registry dies. To make images a persistent data of the registry container, use a docker volume on the host filesystem.

mkdir /data
docker run -d -p 443:5000 --restart=always --name docker-registry \
-v /data:/var/lib/registry \
-v /etc/certs:/certs \
-e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
-e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
registry:latest
Having used local file system directory /data as backend for the registry container, images pushed on that registry will survive to registry crashes or dies. However, having used a persistent backend does not prevent data loss due to local storage fails. For production use, a safer option is using a shared storage like NFS share.

Set the default Docker registry
Configure a registry mirror to change the default registry from Docker Hub to a local registry. The first time docker requests an image from local registry mirror, it pulls the image from the public Docker Hub and stores it locally. On subsequent requests, the local registry mirror is able to serve the image from its own storage.

Edit the /etc/docker/daemon.json configuration file

{
  "storage-driver": "devicemapper",
  "hosts": ["tcp://0.0.0.0:2375","unix:///var/run/docker.sock"],
  "registry-mirrors": ["https://myregistry:5000"]
}
and restart the Docker Engine.

