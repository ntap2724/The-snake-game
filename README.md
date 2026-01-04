# The Snake Game

Trò chơi Rắn săn mồi (Snake) viết bằng Python, có menu, tạm dừng, theo dõi điểm cao và cửa sổ có thể thay đổi kích thước.

## Mô tả
Điều khiển rắn ăn thức ăn để tăng chiều dài và điểm số. Trò chơi kết thúc khi rắn chạm vào chính mình. Tốc độ sẽ tăng dần theo số thức ăn đã ăn.

## Tính năng chính

- Menu bắt đầu, màn hình Game Over và trạng thái tạm dừng
- Điều khiển bằng phím mũi tên hoặc WASD
- Điểm cao và thống kê số ván chơi được lưu vào `high_scores.json`
- Cửa sổ có thể thay đổi kích thước và tự căn chỉnh giao diện

## Cài đặt

1. Clone repo về máy
2. Tạo môi trường ảo:
   **Windows (PowerShell hoặc CMD):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Mac/Linux (Bash/Zsh):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Cài đặt phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

4. Cài đặt package (để dùng lệnh `snakegame`):
   ```bash
   pip install -e .
   ```

## Cách chạy

```bash
python -m src.main
```

Hoặc:
```bash
snakegame
```

## Điều khiển

- **Mũi tên / WASD**: Di chuyển rắn
- **P**: Tạm dừng / tiếp tục
- **R**: Chơi lại nhanh khi đang chơi hoặc tạm dừng
- **Enter**: Bắt đầu từ menu / tiếp tục khi tạm dừng
- **Q / ESC**: Thoát
- **SPACE**: Chơi lại ở màn hình Game Over
- **M**: Về menu ở màn hình Game Over

## Cơ chế trò chơi

- Mỗi thức ăn tăng 1 điểm
- Rắn dài ra sau mỗi lần ăn
- Tốc độ tăng dần, có giới hạn tối đa
- Ván chơi kết thúc khi tự cắn mình

## Cấu trúc thư mục

```
src/
  ├── main.py        - Điểm vào trò chơi
  ├── game.py        - Vòng lặp và trạng thái trò chơi
  ├── snake.py       - Lớp Snake
  ├── food.py        - Lớp Food
  ├── game_board.py  - Lưới/khung chơi
  ├── high_score.py  - Lưu và đọc điểm cao
  ├── config.py      - Hằng số cấu hình
  └── utils.py       - Hàm tiện ích

tests/
  └── test_game.py   - Unit tests
```

## Phát triển

Chạy test:
```bash
pytest tests/
```

## Yêu cầu

- Python 3.10+
- Pygame 2.5.3+ (hiển thị)
- Pytest 7.4.3 (test)
- setuptools, wheel
