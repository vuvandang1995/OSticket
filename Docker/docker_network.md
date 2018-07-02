# Docker networking
- Docker networking cung cấp tính năng cô lập hoàn toàn cho containers. Tổng quan bên dưới về default networking mà Docker Engine tạo ra. Nó mô tả về các kiểu networks được tạo mặc định hoặc user tự tạo.
## Default networks
- Cài đặt Docker Engine, mặc định có 3 networks trên máy host

<img src="">

- Đại diện cho mạng Bridge là `docker0`

<img src="">

- `docker0` interface tương tự như Linux bridge được tạo bởi docker vào thời điểm ban đầu. Docker sẽ lựa chọn ngẫu nhiên địa chỉ ip và subnet từ dải địa chỉ private được định nghĩa bởi RFC năm 1918 mà dải địa chỉ đó chưa được sử dụng trong máy host.

<img src="">

- Tất cả các `docker container` sẽ được kết nối tới `docker0` thông qua virtual Ethernet interface. Các container được kết nối tới `docker0` có thể sử dụng các rule iptables NAT được tạo bởi docker  để giao tiếp ra bên ngoài. Địa chỉ IP cho `docker0` mặc định là `172.17.0.0/16`
- Docker networking  tận dụng tính năng Linux namespaces kernel. Vì các network namespace được liệt kê trong thư mục `/var/run/netns`, nếu bạn muốn sử dụng công cụ quản lý namespace kiểu như lệnh `ip netns`, bạn nên liên kết mềm thư mục đó ra thư mục `/var/run/docker/netns`

<img src="">

- Tạo một container và kiểm tra host đang tạo một virtual Ethernet interface mới:

<img src="">

```
ifconfig
...
veth554166f	  Link encap:Ethernet  HWaddr c2:2c:85:40:de:2e  
			  inet6 addr: fe80::c02c:85ff:fe40:de2e/64 Scope:Link
			  UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
			  RX packets:8 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:45 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:0 
			  RX bytes:656 (656.0 B)  TX bytes:5895 (5.8 KB)
...
```

<img src="">


- Kết nối container vừa tạo và kiểm tra network stack của nó:

<img src="">

<img src="">

- Khi chạy lệnh `docker run` thì tự động sẽ add những container mới được tạo vào bridge `docker0`. Những container trong default network sẽ giao tiếp được với nhau bằng địa chỉ ip của `bridge docker0` cấp.
- Hình vẽ bên dưới thể hiện việc các container kết nối với host thông qua `docker0`:

<img src="">

- Một thiết bị ethernet ảo hoặc `veth` là một linux networking interface mà có thể kết nối giữa 2 network namespace. Một `veth` là một link song công kết nối 2 namespace. Traffic trong một interface được hướng ngoài interface khác. Docker network drivers sử dụng `veth` để kết nối giữa các namespace khi docker network được tạo. Khi một container được gắn vào một Docker network, một đầu của `veth` gắn vào container, thường nhìn thấy đó là `eth0`, đầu còn lại của `veth` gắn vào Docker network.
- `iptables` là hệ thống lọc gói tin, nó là một phần của Linux kernel. Nó là firewall của layer3, layer 4 mà cung cấp các rules cho việc đánh dấu các gói tin, drop hoặc NAT. Docker network drive hay sử dụng `iptables` để phân đoạn network traffic, cung cấp port NAT từ máy host và đánh đâu traffic cho việc cân bằng tải
- Xem thông tin của bridge network:

<img src="">

- Nhìn hình trên ta biết được các thông tin về `docker0`: name, id, scope: ở local, drive: kiểu bridge, địa chỉ config, gateway... ngoài ra còn biết thêm  thông tin về các container gắn với `docker0` này: name, ipv4, ipv6, MAC,...

- Bridge network là mạng phổ biến nhất cho các Docker container. Nó có một số option như:
	- Host mode
	- Container mode
	- None mode
1. Host mode
	- Ở host mode, Container được dùng chung networking namespaces với máy host, trực tiếp sử dụng những thông số đó khi ra bên ngoài (ip, MAC,port,...). Điều đó có nghĩa là bạn cần phải sử dụng port ánh xạ tới mỗi service bên trong container
	- Ví dụ:

	<img src="">

	- Kiểm tra địa chỉ ip của container vừa tạo

	<img src="">

	- Như hình bên trên, container ở host mode sẽ sử dụng các tài nguyên mạng của máy host như các interface, port,...

	- *Lưu ý*: tạo nhiều container ở host mode trên cùng một host được, chỉ cần không trùng port là được.
	- Xem thông tin của network host mode

	<img src="">

	- Như hình bên trên ta thấy các thông tin về network host, ta thấy các thông tin về mạng này, các container gắn vào với network này.
2. Container mode
	- Trong container mode, một container buộc phải sử dụng lại networking namespace của container khác. Điều đó được sử dụng nếu bạn muốn cung cấp mạng tùy chỉnh từ container đã nói phía trước. Ví dụ, cung cấp mạng cho nhiều container cũng như sử dụng chung 1 IP
	
	- Ví dụ: Tạo một container tên là web, kiểu network default, nó sẽ nhận được địa chỉ ip là `172.17.0.2`. Tạo thêm 1 container nữa với network container mode, nó cũng sẽ nhận địa chỉ ip `172.17.0.2`
	
	<img src="">

3. None mode
	- Là chế độ không cấu hình network. Điều này hữu ích cho việc  container không cần ra khỏi mạng
	`docker run --net=none -itd --name=centos-none centos`

## User defined bridge networks
- Docker cho phép user tạo network cô lập tốt hơn cho container. Docker cung cấp các drivers network để tạo những loại mạng này. Với docker, nó có khả năng tạo nhiều network và gán container vào nhiều hơn 1 network. Container CÓ THỂ chỉ giao tiếp trong mạng của nó. Một container gán với 2 network thì có thể giao tiếp với các container trong mạng đó. 
- Hình bên dưới là mô hình Docker multiple networking

<img src="">

- Tạo một bridge network tùy chỉnh:

<img src="">

- Sau khi tạo một network như trên, 1 interface được tạo ra tương tự như `docker0`

<img src="">

- Cũng có thể tạo network mà có interface là tên muốn đặt:

<img src="">

- Xem thông tin của network vừa tạo:

<img src="">

- Tạo một container gắn với mạng `bridge2` bên trên:

<img src="">

- Kiểm tra lại thông tin network `bridge2`, bạn sẽ thấy địa chỉ ip của container vừa tạo

<img src="">


- Gắn thêm 1 network nữa vào container vừa tạo:

<img src="">

- Xóa network trong docker:

<img src="">

## Using custom Docker networks
- Ví dụ: Chúng ta cần deploy nhiều ứng dụng như xây dựng 1 nền tảng blog WorPress sử dụng cơ sở dữ liệu MariaDB và máy chủ web Apache/PHP. Ứng dụng Apache/PHP sẽ lắng nghe các kết nối tới host port 80. Nó sử dụng một network internal User-defined để kết nối tới Máy chủ MarieDB lắng nghe trên cổng 3306. Máy chủ MarieDB được gắn với network internal
- Test:
	- Tạo một Internal network
	
	<img src="">
	
	- Tạo một MariaDB server gắn vào internal network
	
	<img src="">
	
	- Tạo ứng dụng WordPress gắn với default network:
	
	<img src="">
	
	- Để container Wordpress có thể kết nối được tới container mariadb
	
	<img src="">
	
## Inter container Communication
- Mặc định, Docker có thể giao tiếp giữa các container bởi vì tùy chọn `enable_icc=true` nghĩa là các container trên một host là giao tiếp tự do. Container giao tiếp với bên ngoài được quản lý thông qua Iptables và ip_fordwarding.
- Vì lý do bảo mật, nó phải disable inter-container  bằng các cài tùy chọn `enable_icc=true`  khi mình tạo network user-defined.
- Ví dụ, tạo một internal network và disable inter-container:

<img src="">

- Tạo 2 container gắn vào mạng internal vừa tạo và gán địa chỉ ip cho chúng:

<img src="">

- **Lưu ý**: Phần này để lại hỏi a Công.



# Tổng hợp các lưu ý:
1. thường thì sẽ sử dụng network user-defined.
	- Sư khác nhau giữa default network và user-defined là"
		- Các container gắn vào mạng user-defined có thể giao tiếp tự do với nhau ở tất cả các cổng. lưu ý là chỉ giao tiếp với nhau tự do ở tất cả các cổng thôi chứ muốn giao tiếp với bên ngoài vẫn cần phải NAT port thông qua máy host
		- Còn các container gắn vào mạng default thì muốn giao tiếp với nhau thì cần mở port đó. Ví dụ như container Apache và Mariadb đều gắn vào default network, Apache muốn kết nối tới Mariadb thì Mariadb phải mở port 3306.
		- User-defined network linh hoạt hơn trong việc thay đổi dải địa chỉ ip. Ví dụ cụ thể là: Giả sử có 2 container gắn với user-defined network dùng dải địa chỉ `192.168.1.0/24`. Muốn thay đổi dải địa chỉ cung cấp cho các container đó, chỉ cần disable user-default network kia đi, tạo cáo mới và gắn container vào cáo network mới.
		- Còn muốn thay đổi dải địa chỉ IP của default networkt thì cần phải thay đổi trong file cấu hình (file json gì đó)
		- Giả sử có 1 container gắn vào 1 user-defined network, muốn thay đổi network cho container đó, chỉ cần disable mạng ý, tạo user-defined mới và gắn container vào VÀ KHÔNG CẦN TẮT CONTAINER đó. Còn đối với container default network, muốn thay đổi network trong container đó, thì phải stop container đó, tạo container mới rồi gắn network thôi.
		
		




	
	
	
		
		
			
		