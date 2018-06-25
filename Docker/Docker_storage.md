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
- Docker cung cấp 3 cách khác nhau để có thể chia sẻ dữ liệu (mount data) từ Docker host tới container đó là:

        + volumes
        + bind mounts
        + tmpfs mounts

        volumes thường luôn là cách được lựa chọn sử dụng nhiều nhất đối với mọi trường hợp

    - Không có vấn đề nào xảy ra khi ta lựa chọn cách chia sẻ dữ liệu để sử dụng, vì các dữ liệu đều giống nhau trong container. Chúng được quy định giống như một thư mục hoặc một file trong filesystem của containers. Sự khác biệt giữa `volumes`, `bind mounts` và `tmpfs mounts` chỉ đơn giản là khác nhau về vị trí lưu trữ dữ liệu trên Docker host.

        > ![types-of-mounts.png](../../images/types-of-mounts.png)

    - Hình ảnh trên mô tả vị trí lưu trữ dữ liệu của container trên Docker host. Theo đó, ta có thể thấy được:

        + `volumes` được lưu trữ như một phần của filesystem trên Docker host và được quản lý bởi Docker (xuất hiện trong /var/lib/docker/volumes trên Linux).  Đây được xem là cách tốt nhất để duy trì dữ liệu trong Docker

        + `bind mounts` cho phép lưu trữ bất cứ đâu trong host system. 

        + `tmpfs mounts` cho phép lưu trữ tạm thời dữ liệu vào bộ nhớ của Docker host, không bao giờ ghi vào filesystem của Docker host.

- ### <a name="volumes"> Trường hợp nào thì sử dụng volumes</a>

    - volumes được tạo và quản lý bởi Docker. Ta có thể tạo volumes với câu lệnh `docker volume create` hoặc tạo volumes trong khi tạo containers, ...

    - Khi tạo ra volumes, nó sẽ được lưu trữ trong một thư mục trên Docker host. Khi ta thực hiện mount volumes vào container thì thư mục này sẽ được mount vào container. Điều này tương tự như cách `bind mounts` hoạt động ngoại trừ việc được Docker quản lý.

    - volumes có thể được mount vào nhiểu containers cùng một lúc. Khi không có containers nào sử dụng volumes thì volumes vẫn ở trạng thái cho phép mount vào containers và không bị xóa một cách tự động.

    - volumes hỗ trợ volume drivers, do đó ta có thể sử dụng để lưu trữ dữ liệu từ remote hosts hoặc cloud providers.

    - Đây là cách phổ biến được lựa chọn để duy trì dữ liệu trong services và containers. Một số trường hợp sử dụng volumes có thể bao gồm:

        + Chia sẻ dữ liệu với nhiều containers đang chạy. Dữ liệu yêu cầu phải tồn tại kể cả khi dừng hoặc loại bỏ containers.

        + Khi Docker host có cấu trúc filesystem không thống nhất, ổn định, thường xuyên thay đổi.

        + Khi muốn lưu trữ dữ liệu containers trên remote hosts, cloud thay vì Docker host.

        + Khi có nhu cầu sao lưu, backup hoặc migrate dữ liệu tới Docker host khác thì volumes là một sự lựa tốt. Ta cần phải dừng containers sử dụng volumes sau đó thực hiện backup tại đường dẫn `/var/lib/docker/volumes/<volume-name>`


- ### <a name="bind-mounts"> Trường hợp nào thì sử dụng bind mounts</a>

    - `bind mounts` có chức năng hạn chế so với `volumes`. Khi ta sử dụng `bind mounts` thì một file hoặc một thư mục trên Docker host sẽ được mount tới containers với đường dẫn đầy đủ.

    - Đây là các trường hợp phổ biến lựa chọn `bind mounts` đối với containers:

        + Chia sẻ các file cấu hình từ Docker host tới containers. 

        + Chia sẻ khi các file hoặc cấu trúc thư mục trên Docker host có cấu trúc cố định phù hợp với yêu cầu của containers.

        + Kiểm soát được các thay đổi của containers đối với filesystem trên Docker host. Do khi sử dụng `bind mounts`, containers có thể trực tiếp thay đổi filesystem trên Docker host.

- ### <a name="tmpfs"> Trường hợp nào thì sử dụng tmpfs mount</a>

    - `tmpfs mounts` được sử dụng trong các trường hợp ta không muốn dữ liệu tồn tại trên Docker host hay containers vì lý do bảo mật hoặc đảm bảo hiệu suất của containers khi ghi một lượng lớn dữ liệu một cách không liên tục.

____

- `bind mounts` và `volumes` đều có thể được mount vào container khi sử dụng flag `-v` hoặc `--volume` nhưng cú pháp sử dụng có một chút khác nhau. Đối với `tmpfs mounts` có thể sử dụng flag `--tmpfs`. Tuy nhiên, từ bản Docker 17.06 trở đi, chúng ta được khuyến cáo dùng flag `--mount` cho cả 3 cách, để cú pháp câu lệnh minh bạch hơn.

- Sự khác nhau giữa `--volume, -v` và `--mount` đơn giản chỉ là về cách khai báo các giá trị:

    + `--volume, -v` các giá trị cách nhau bới `:`. theo dạng source:target. Ví dụ: `-v myvol2:/app`
    + `--mount` khai báo giá trị theo dạng `key=values`. Ví dụ: `--mount source=myvol2,target=/app`. Trong đó `source` có thể thay thế bằng `src`, `target` có thể thay thế bằng `destination` hoặc `dst`.

- Khi sử dụng volumes cho services thì chỉ `--mount` mới có thể sử dụng.

- ### <a name="use-volumes"> Cách sử dụng volumes</a>

    - Volumes là cơ chế ưa thích cho việc duy trì dữ liệu được tạo ra bởi Docker containers và được quản lý bởi Docker. Trong khi `bind mounts` phụ thuộc vào cấu trúc thư mục của Docker host. Do đó, volumes có một số tính năng khác biệt so với `bind mounts` như sau:

        + Volumes dễ dàng backups, migrate hơn so với `bind mounts`.
        + Có thể quản lý volumes sử dụng Docker CLI hoặc Docker API.
        + Volumes làm việc trên cả Linux containers và Winodws containers.
        + Volumes an toàn hơn khi sử dụng để chi sẻ giữa nhiều containers.

    - Để tạo một volume, ta sử dụng câu lệnh:

            docker volume create my-vol

    - Khi khởi chạy containers với volume chưa có (tồn tại) thì Docker sẽ tự động tạo ra volume với tên được khai báo hoặc với một tên ngẫu nhiên và đảm bảo tên ngẫu nhiên này là duy nhất. Ví dụ:

            docker run -d \
              -it \
              --name devtest \
              --mount type=volume,source=myvol2,target=/app \
              nginx:latest

        câu lệnh trên sẽ thực hiện mount volume `myvol2` tới thư mục `/app` trong container `devtest`.

    - Nếu muốn mount volume với chế độ `readonly`, ta có thể thêm vào trong `--mount`. Với ví dụ trên có thể là làm như sau:

            --mount source=myvol2,target=/app,readonly

- ### <a name="use-bind"> Cách sử dụng bind mounts</a>

    - Sử dụng tương tự như volume, ta chỉ cần thay đổi giá trị của `type` trong `--mount`. Theo đó ta có câu lệnh ví dụ như sau:

            docker run -d \
              -it \
              --name devtest \
              --mount type=bind,source=myvol2,target=/app \
              nginx:latest

- ### <a name="use-tmpfs"> Cách sử dụng tmpfs mounts</a>

    - Khi sử dụng `tmpfs mounts` thì ta không thể chia sẻ dữ liệu giữa containers.
    - `tmpfs mounts` chỉ làm việc đối với Linux containers.

    - Tương tự như khi sử dụng volumes, ta chỉ cần thay đổi giá trị `type` trong `--mount`:

            docker run -d \
              -it \
              --name devtest \
              --mount type=tmpfs,source=myvol2,target=/app \
              nginx:latest
              

