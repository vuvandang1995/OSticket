# Tìm hiểu docker
## I. Công nghệ container
- a. Linux container được hình thành từ 2 features chính của Linux kernel. đó chính là Linux namespace và control groups (Cgroup). Hiểu đơn giản, nhiệm vụ chính của `Namespace` là **isolate** và **virtualize** các system resources, còn `Cgroups` thì tính toán và giới hạn việc sử dụng của các isolated và virtualized system resources mà namespace thực hiện.
- b. Runtime sẽ sử dụng các features trên của Linux kernel để quản lý các linux containers. Tổng kết nhanh về một số runtime cho linux containers:
	- RunC: được hình thành bởi Open Container Initiative (OCI). Nó là một runtime được chuẩn hóa và sử dụng bởi Docker
	- Liblxc: Là runtime được sử dụng bởi LXC và LXD. Cách đây 3 năm thì docker cũng dùng nó nhưng giờ đã bị deprecated và thay vào đó là cặp bài trùng libcontainer+RunC
	- rkt+systemd+nspawn: Được sử dụng như là runtime của rkt. 'rkt'  được sử dụng đôi lúc hơi cẩu thả một chút khi nó vừa được dùng để ám chỉ runtime cũng như là container manager
- c. Cái ta cần hiện giờ chính là một wrapper của các runtime trên hay còn gọi là container manager
	- Các wrapper của runtime cần được phải add thêm các tool cũng như các features, networking, volume để quản lý container. Ngoài ra nó cũng cần thiết phải thân thiện với người dùng vì mục đích của các container manager này chính là cung cấp API cho người dùng thực hiện các thao tác tới container.
		- LXC: Là một container manager được sponsor bởi Canonical. Nó sử dụng liblxc làm runtime và được support tới 2019
		- LXD: là một phiên bản update của LXC. Nó cũng dùng liblxc làm runtime. Tuy nhiên nó khác với các container manager khác là nó boots một full linux system ở một container (tức là ta sẽ thấy 'init' process chạy bên trong container). Nếu đứng tại góc nhìn này thì một LXD container khá giống một linux system.
		- rkt: là một sản phẩm của CoreOS. Bản thân Rkt cũng support các image của Docker
		- Docker: là ông kẹ của container manager, một container manager mạnh nhất trong khoảng 2 năm trở lại đây.
		- OCID: một sự kết hợp của K8s và Redhat nhằm mục đích thay thể docker
1. Lịch sử hình thành
	- 1.1 Ngày lâu rồi, mô hình máy chỉnh thường là `máy chủ vật lý + hệ điều hành (OS) + application`
	
	<img src="https://i.imgur.com/XbTd6C9.png">
	 
	Vấn đề ở đây là lãng phí tài nguyên, một máy chủ chỉ được cài một OS, cho dù ổ cứng và ram khủng như nào cũng không tận dụng được hết
	- 1.2 Công nghệ ảo hóa `virtualization` ra đời
	
	<img src="https://i.imgur.com/yyKBDMK.png">
	
	Virtualbox và VMware sử dụng công nghệ này, trên một máy chủ vật lý có thể tạo ra nhiều OS, tận dụng tài nguyên tốt hơn nhưng xảy ra một vấn đề khác: Khi chạy máy ảo, bạn phải cung cấp "cứng" dung lượng ổ cứng và ram cho máy ảo đó, bật máy ảo đó lên không làm gì thì máy thật cũng phải phân phát tài nguyên. Hơn nữa, việc khởi động các máy ảo khá lâu
	
	- 1.3 Công nghệ Containerlization
	
	<img src="https://i.imgur.com/2NdI6U9.png">
	
	Với công nghệ này, trên một máy chủ vật lý, ta sẽ sinh ra nhiều máy con (giống với công nghệ ảo hóa virtualization), nhưng tốt hơn ở chỗ các máy con này (guess OS) đều dùng chung phần nhân của máy mẹ (host OS) và chia sẻ tài nguyên với máy mẹ. 
	Có thể nói khi nào cần tài nguyên thì mới được cấp, cần bao nhiêu cấp bấy nhiêu, như vậy việc tận dụng tài nguyên đã tối ưu hơn. Điểm nổi bật nhất của containerlization là nó sử dụng các container.
2. Vậy Container là gì?
- Hiểu đơn giản thì container là một giải pháp để chuyển giao phần mềm một cách đáng tin cậy giữa các môi trường máy tính khác nhau bằng cách:
	- Tạo ra một môi trường chứa mọi thứ mà phần mềm có thể chạy được
	- không bị các yếu tố liên quan đến môi trường hệ thống làm ảnh hưởng tới
	- Cũng như không làm ảnh hưởng tới các thành phần còn lại của hệ thống
- Các prcocess trong một container bị cô lập với các tiến trình của các container khác trong cùng hệ thống tuy nhiên tất cả các container này đều chia sẻ kernel của host OS (dùng chung tài nguyên host OS)
- Ưu điểm:
	- Linh động: Triển khai ở bất kỳ nơi đâu do sự phụ thuộc của ứng dụng vào tầng OS cũng như cơ sở hạ tầng được loại bỏ
	- Nhanh: Do chia sẻ host OS nên container có thể được tạo ra gần như tức thì. Điều này khác với vagrant - tạp môi trường ảo ở level phần cứng, nên khi khởi động mất nhiều thời gian hơn.
	- Nhẹ: Container cũng sử dụng chung các images nên không nhiều disks
	- Đồng nhất: Khi nhiều người dùng cùng phát triển trong một dự án sẽ không bị sai khác về mặt môi trường
	- Đóng gói: Có thể ẩn môi trường bao gồm cả app vào trong một gói được gọi là container. Có thể test được các container. Việt tạo hay xóa container rất dễ dàng

## Docker
1. Docker là gì?
- Là một dứng dụng mã nguồn mở để hiện thực hóa công nghệ container trong linux.
2. Chức năng và vai trong của docker?
	- Tự động triển khai các ứng dụng bên trong các container bằng các cung cấp thêm một lớp trừu tượng và tự động hóa việc ảo hóa mức hệ điều hành
	- Docker có thể được sử dụng ở cả 3 hệ điều hành biến: Windows, Linux và Mac OS
	- Lợi ích của docker bao gồm:
		- Nhanh trong việc triển khai và di chuyển, khởi động container
		- bảo mật
		- lightweight (tiết kiệm disk & CPU)
		- Mã nguồn mở
		- Hỗ trợ APIs để giao tiếp với các container
		- Phù hợp trong môi trường làm việc đòi hỏi phải liên tục tích hợp và triển khai các dịch vụ, phát triển cục bộ, các ứng dụng multi-tier
3. Các khái niệm cần biết khi sử dụng docker
	- Image:
		- Images trong Docker hay con gọi Mirror. là một template có sẵn (hoặc có thể tự tạo) với các chỉ dẫn dùng để tạo ra các container
		- Được xây dựng từ một loạt các layers. Mỗi layer là một kết quả đại diện cho một lệnh trong Dockerfile
		- Lưu trữ dưới dạng read-only template
	- Registry
		- Docker registry là nơi chứa các images với 2 chế độ public và private
		- Là nơi cho phép chia sẻ các image template để sử dụng trong quá trình làm việc với docker
	- Volume
		- Volume trong Docker là nơi để dùng để chia sẻ dữ liệu trong các container
		- Có thể thực hiện sử dụng Volume đối với 2 trường hợp:
			- Chia sẻ giữa container với container
			- Chia sẻ giữa container và Host
	- Container
		- Docker container là một thể hiện cụ thể của Docker image với những thao tác cơ bản để sử dụng CLI như start, stop, restart hay delete...
		- Container image là một gói phần mềm thực thi lightweight, độc lập và có thể thực thi được bao gồm mọi thứ cần thiết để chạy được nó: Code, system libraries, sttings. Các ứng dụng có sẽ cho cả Linux Windowns. các container sẽ luôn chạy ổn định bất kể môi trường.
		
		<img src="https://i.imgur.com/RVjs9ig.png">
		
		- Containers and virtual machines có sự cách ly và phân bổ tài nguyên tương tự, nhưng có chức năng khác vì các container ảo hóa hệ điều hành thay vì phần cứng. Các container có tính portable và hiệu quả hơn.
		
		<img src="https://i.imgur.com/XnghyLR.png">
		
		- Container là một sự trừu tượng hóa ở lớp ứng dụng và code phụ thuộc vào nhau. Nhiều container có thể chạy trên cùng một máy và chia sẻ kernel của hệ điều hành với các container khác, mỗi máy đều chạy như các quá trình bị cô lập trong không gian người dùng. Các container chiếm ít không gian hơn các máy ảo (container image thường có vài trăm thậm chí là vài MB), và start gần như ngay lập tức.
		- Máy ảo (VM) là một sự trừu tượng của phần cứng vật lý chuyển tiếp từ một máy chủ sang nhiều máy chủ. Hypervisor cho phép nhiều máy ảo chạy trên một máy duy nhất. Mỗi máy ảo bao gồm một bản sao đầy đủ của một hệ điều hành, một hoặc nhiều ứng dụng, các chương trình và thư viện cần thiết - chiếm hàng chục GB. Máy ảo cũng có thể khởi động chậm.
	- Dockerfile
		- Docker Image có thể được tạo ra một các tự động bằng việc đọc các chỉ dẫn trong Dockerfile
4. Các thành phần, kiến trúc trong Docker

<img src="https://i.imgur.com/VvR6QEb.png">

- Hình ảnh bên trên là mô tả về Docker Engine. Theo đó, Docker Engine là một ứng dụng client-server với các thành phần chính:
	- Một máy chủ đảm nhiệm thực hiện quá trình daemon (chạy câu lệnh dockerd).
	- REST API xác định các giao diện mà các chương trình có thể sử dụng để nói chuyện với daemon và hướng dẫn nó phải làm gì.
	- Một CLI (chạy câu lệnh docker).
- CLI sẽ sử dụng Docker REST API để kiểm soát hoặc tương tác với Docker daemon thông qua kịch bản hoặc lệnh CLI trực tiếp.

<img src="https://i.imgur.com/CXlGIRQ.png">

- Docker sử dụng kiến trúc client-server. Docker client sẽ giao tiếp với Docker daemon các công việc building, running và distributing các Docker Container.
- Docker client và Docker daemon có thể chạy cùng trên một hệ thống hoặc ta có thể kết nối một Docker client tới một remote Docker daemon. Docker client và Docker daemon liên lạc với nhau bằng việc sử dụng REST API thông qua UNIX sockets hoặc network interfaces.
- Docker daemon (dockerd ) sẽ lắng nghe các request từ Docker API và quản lý Docker objects bao gồm images, containers, networks và volumes. Một daemon cũng có thể liên lạc với các daemons khác để quản lý Docker services.
- Docker client (docker ) là con đường chính để những người sử dụng Docker tương tác và giao tiếp với Docker. Khi sử dụng mộ câu lệnh chẳng hạn như docker run thì client sẽ gửi câu lệnh tới dockerd để thực hiện câu lệnh. Các câu lệnh từ Docker client sử dụng Docker API và có thể giao tiếp với nhiều Docker daemon.

5. Network trong Docker
- Dưới đây là hình ảnh mô tả kiến trúc Network của container hay còn gọi là Container Networking Model (CNM)

<img src="https://i.imgur.com/tSLRBmv.png">

- Đây là cáu trúc mức độ cao trong CNM. Theo đó, ta có:
	- Sandbox - chứa các cấu hình của ngăn xếp mạng container. Bao gồm quản lý network interface, route table và các thiết lập DNS. Một Sandbox có thể được coi là một namespace network và có thể chứa nhiều endpoint từ nhiều mạng
	- Endpoint - Là điểm kết nối một Sandbox tới một mạng
	- Network - CNM không chỉ định một mạng tuân theo mô hình OSI. Việc triển khai mạng có thể là VLAN, Bridge,... Các endpoint không kết nối với mạng thì không kết nối trên mạng
	- CNM cung cấp 2 interface có thể được sử dụng cho việc liên lạc, điều khiển ... container trong mạng:
		- Network Drives - Cung cấp, thực hiện thực tế việc tạo ra một mạng hoạt động. Được sử dụng với các drivers khác và thay đổi một cách dễ dàng đối với các trường hợp cụ thể. Nhiều network driver có thể được sử dụng trong Docker nhưng mỗi một network chỉ là một khởi tạo từ một network driver duy nhất. Theo đó mà ta có 2 loại chính của CNM network drivers như sau:
			- Native Network Drivers - Là một phần của Docker Engine và được cung cấp bới Docker. Có nhiều drivers để dễ dàng lựa chọn cho khả năng của mạng như overlay networks hay local bridges.
			- Remote Network Drivers - Là các network drivers được tạo ra bởi cộng đồng và các nhà cung cấp. Được sử dụng để tích hợp vào các phần mềm hoặc phần cứng đang hoạt động.
		
		- IPAM Drivers: Drivers quản lý các địa chỉ IP cung cấp mặc định cho các mạng con hoặc địa chỉ IP cho các mạng và endpoint nếu chúng không được chỉ định. Địa chỉ IP cũng có thể gán thủ công qua mạng, container,...
	- Giao tiếp giữa docker engine-libnetwork-driver
	
	<img src="https://imgur.com/e649kEq">
	
	- Docker Native Network Drivers - là một phần của Docker Engine và không yêu cầu cần phải có nhiều modules. Được gọi và sử dụng thông qua các câu lệnh docker network. Dưới đây là native network hiện có:
	
	<img src="https://i.imgur.com/ueBGh0w.png">
	
	- Đối với native driver network trong container. Ta có:
		- Chiều outbound khi các container sử dụng trong container
	
		<img src="https://i.imgur.com/wF05EDB.png">
	
		- Chiều inbound khi các container sử dụng trong container
		
		<img src="https://i.imgur.com/U37suFM.png">
		
		- Container kết nối với network thông quan docker0 interface:
		
		<img src="https://i.imgur.com/e8ySZsT.png">
		
6. Volume trong Docker
- Volume là một thư mục đặc biệt được chỉ định trong một hoặc nhiều container
- Volume được thiết kế để duy trì dữ liệu, độc lộc với vòng đời của container
- Do đó, Docker sẽ không bao giờ tự động xóa volumes khi ta xóa bỏ container. Còn được biết đến là data volume
- Có 3 kiểu volume đó là: host, anonymous, named:
	- host volume: tồn tại trên file system của docker host và có thể được truy cập từ bên trong container
	- named volume: là volume được Docker quản lý và được đặt tên
	- anonymous volume: tương tự như named volume. Tuy nhiên rất có thể để có thể tham vấn tới cùng một volume theo thời gian khi volume là một đối tượng vô danh. Lưu trữ các tập tin mà Docker xử lý.
