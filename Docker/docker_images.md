# Docker mirror (docker images)
## Một số chú ý:
- Docker images là template để tạo ra các container. Tức là các container chạy được từ các image này
- Có 2 cách để tạo ra các mirror container
	- C1: Tạo một container, chạy các câu lệnh cần thiết và sử dụng lệnh docker commit để tạo image mới. Cách này thường không được  khuyến cáo
	- C2: Viết một dockerfile và thực thi nó để tạo ra một images.
- Khi một container được tạo ra từ đầu, nó sẽ kép các image (pull) từ `Docker Hub` (Chính là Docker Registry) về và thực tạo container từ image đó
- Tất cả mọi người đều có thể tạo ra các images
- Docker hub có thành phần docker registry - được vận hành với công ty Docker, nơi đây chứa các image mà người dùng chia sẻ.
- Các images là dạng file - read only (chỉ đọc). Khi tạo một container mới, trong mỗi container sẽ tạo thêm một lớp có thể `ghi` được gọi là `container-layer`. Các thay đổi trên container như thêm, sửa, xóa file ... sẽ được ghi trên lớp này. Do vậy, từ một image ban đầu, ta có thể tạo ra nhiều container mà chỉ tốn rất ít dung lượng ổ đĩa.
- Docker cung cấp 3 công cụ phân tán giúp chúng ta lưu trữ và quản lý các docker image. Để tự dụng một private registry và lưu trữ các private image chúng ta có thể sử dụng một trong các công cụ sau:
	- Docker Registry: một opensource image distribusion tool giúp lưu trữ và quản lý image
	- Docker Trusted Registry: một công cụ trả phí, nó khác với Docker Registry là có giao diện quản lý và cung cấp một số tính năng bảo mật
	- Docker Hub: đây là một dịch vụ mà bạn không muốn tự quản lý registry. Cung cấp public và private image registry. Mặc định Docker client sẽ sử dụng docker hub nếu không có registry nào được cấu hình. Trên này có rất nhiều image offcial của các phần mềm như nginx, mongodb, mysql,...
- Quy tắc đặt tên images: [REPOSITORY[:TAG]]
	- Trong đó, TAG là phiên bản của images, mặc định không khai báo tag thì docker sẽ hiểu là latest

## Thực hành với image
- Tìm kiếm một image từ docker hub. Ví dụ tìm kiếm image về apace:
`docker search apache`
