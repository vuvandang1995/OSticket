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

	
	
	
		
		
			
		