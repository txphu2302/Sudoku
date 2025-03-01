# Giải Trò Chơi Sudoku

Một ứng dụng Sudoku viết bằng Python với cả giao diện trò chơi và hai giải thuật giải khác nhau.

## Tổng Quan

Dự án này bao gồm ba thành phần chính:
- `main.py`: Trò chơi Sudoku với giao diện đồ họa
- `genetic.py`: Cài đặt giải thuật di truyền để giải các câu đố Sudoku
- `genetic_visual.py`: Giao diện trực quan để theo dõi giải thuật di truyền giải các câu đố

## Tính Năng

- Trò chơi Sudoku tương tác với giao diện đồ họa
- Ba cấp độ khó (Dễ, Trung bình, Khó)
- Hai phương pháp giải:
  - Giải thuật quay lui (main.py)
  - Giải thuật di truyền (genetic.py)
- Biểu diễn trực quan của quá trình giải

## Yêu Cầu

- Python 3.x
- Pygame
- Pygame_widgets

File `requirements.txt` đã được cung cấp để dễ dàng cài đặt các thư viện cần thiết:

```
pip install -r requirements.txt
```

## Cài Đặt

1. Clone hoặc tải dự án về máy:
```
git clone <đường-dẫn-repository>
```

2. Di chuyển vào thư mục dự án:
```
cd <tên-thư-mục-dự-án>
```

3. Cài đặt các thư viện phụ thuộc:
```
pip install -r requirements.txt
```

4. Chạy ứng dụng:
```
python main.py
```
hoặc
```
python genetic_visual.py
```

## Các Thành Phần Chính

### main.py

File này chứa trò chơi Sudoku cốt lõi với giao diện đồ họa đầy đủ được xây dựng bằng Pygame.

**Tính năng:**
- Lưới tương tác để chơi Sudoku
- Nhiều cấp độ khó khác nhau
- Bộ giải sử dụng giải thuật quay lui
- Kiểm tra hợp lệ trò chơi (kiểm tra các nước đi hợp lệ)
- Đánh dấu và chọn ô
- Điều khiển bằng bàn phím

**Điều khiển:**
- Phím mũi tên: Di chuyển trên lưới
- Số 1-9: Nhập giá trị
- 'E': Chuyển sang chế độ Dễ
- 'A': Chuyển sang chế độ Trung bình  
- 'H': Chuyển sang chế độ Khó
- 'C': Xóa lưới
- Nút "Solve": Giải câu đố bằng thuật toán quay lui

### genetic.py

File này cài đặt giải thuật di truyền để giải câu đố Sudoku.

**Cách hoạt động:**
1. Tạo một quần thể các lời giải tiềm năng
2. Đánh giá độ phù hợp của mỗi lời giải (ít xung đột = độ phù hợp cao hơn)
3. Sử dụng phương pháp chọn lọc giải đấu để chọn các bố mẹ
4. Tạo ra các lời giải mới thông qua phép lai ghép và đột biến
5. Lặp lại cho đến khi tìm được lời giải hợp lệ hoặc đạt đến số thế hệ tối đa

**Các hàm chính:**
- `fitness()`: Đánh giá xung đột trong một lời giải ứng viên
- `tournament_selection()`: Chọn bố mẹ để tạo ra thế hệ mới
- `crossover()`: Kết hợp hai bố mẹ để tạo ra một lời giải con
- `mutate()`: Đưa vào những thay đổi ngẫu nhiên để duy trì sự đa dạng
- `genetic_algorithm()`: Thuật toán chính điều phối quá trình giải

### genetic_visual.py

File này cung cấp giao diện trực quan để quan sát giải thuật di truyền giải các câu đố Sudoku.

**Tính năng:**
- Giao diện đồ họa giống trò chơi chính
- Tích hợp với bộ giải giải thuật di truyền
- Trực quan hóa tiến trình giải theo thời gian thực
- Nhiều cấp độ khó khác nhau

**Điều khiển:**
- 'E': Chuyển sang chế độ Dễ
- 'A': Chuyển sang chế độ Trung bình
- 'H': Chuyển sang chế độ Khó
- 'C': Xóa lưới
- Nút "Solve": Giải câu đố bằng giải thuật di truyền

## Cấu Trúc Dự Án

```
sudoku-game/
│
├── main.py              # Trò chơi Sudoku chính với giải thuật quay lui
├── genetic.py           # Cài đặt giải thuật di truyền
├── genetic_visual.py    # Giao diện trực quan cho giải thuật di truyền
├── requirements.txt     # Danh sách các thư viện phụ thuộc
└── README.md            # Tài liệu hướng dẫn này
```

## Sự Khác Biệt Giữa Các Giải Thuật

### Giải Thuật Quay Lui (main.py)
- **Cách tiếp cận**: Thử các giá trị một cách có hệ thống và quay lui khi có mâu thuẫn
- **Ưu điểm**: Đảm bảo tìm được lời giải nếu tồn tại, tương đối nhanh cho các câu đố đơn giản
- **Hạn chế**: Có thể chậm đối với các câu đố rất khó

### Giải Thuật Di Truyền (genetic.py)
- **Cách tiếp cận**: Phát triển một quần thể các lời giải tiềm năng qua các thế hệ
- **Ưu điểm**: Có thể xử lý tốt các câu đố khó, thú vị khi quan sát
- **Hạn chế**: Xác suất (không đảm bảo tìm được lời giải), có thể cần điều chỉnh tham số

## Cách Sử Dụng

### Chơi Sudoku
1. Chạy `python main.py`
2. Sử dụng phím mũi tên để di chuyển và phím số để điền giá trị
3. Chọn cấp độ bằng phím E (Dễ), A (Trung bình), hoặc H (Khó)
4. Nhấn nút "Solve" để giải tự động bằng giải thuật quay lui

### Xem Giải Thuật Di Truyền Hoạt Động
1. Chạy `python genetic_visual.py`
2. Chọn cấp độ bằng phím E, A, hoặc H
3. Nhấn nút "Solve" để xem giải thuật di truyền giải câu đố
4. Quan sát quá trình giải diễn ra theo thời gian thực

## Cải Tiến Trong Tương Lai

- Thêm thống kê thời gian để so sánh các phương pháp giải
- Triển khai tạo câu đố
- Thêm nhiều giải thuật giải hơn
- Cải thiện giao diện và thêm hiệu ứng động
- Thêm khả năng lưu/tải câu đố
- Tính năng gợi ý cho người chơi
- Hỗ trợ đa ngôn ngữ

## Đóng Góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo pull request hoặc báo cáo vấn đề nếu bạn phát hiện lỗi hoặc có ý tưởng cải tiến.

## Giấy Phép

Dự án này được phân phối dưới Giấy phép MIT. Xem file `LICENSE` để biết thêm thông tin.