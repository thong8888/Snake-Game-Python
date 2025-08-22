# 🐍 Snake Game Python

Đây là phiên bản **Snake Game** viết bằng Python + Pygame, có đầy đủ menu, chế độ chơi, độ khó và lưu **High Score**.

---

## 🎮 Tính năng
- 2 chế độ chơi:
  - **Vô tận (Endless Mode)**: chơi đến khi thua.
  - **Theo màn (Level Mode)**: mỗi độ khó có mốc điểm, qua màn sẽ tăng tốc độ và đổi màu nền. Thắng khi hoàn thành tất cả màn.
- 3 độ khó: **Dễ, Trung bình, Khó**.
- Lưu **High Score** vào file `highscore.txt`.
- Menu trực quan để chọn chế độ và độ khó.
- Màu sắc thay đổi khi qua màn (Level Mode).

---

## ⚙️ Cài đặt
1. Cài Python (>= 3.8).
2. Cài thư viện **pygame**:
   ```bash
   pip install pygame
3.Tải file snake.py về.

⌨️ Điều khiển

⬆️ Mũi tên lên: đi lên

⬇️ Mũi tên xuống: đi xuống

⬅️ Mũi tên trái: đi trái

➡️ Mũi tên phải: đi phải

🏆 Luật chơi

Ăn mồi 🍎 để tăng điểm và làm rắn dài thêm.

Đụng tường hoặc cắn vào thân → Game Over.

Level Mode: đạt đủ điểm → qua màn → rắn nhanh hơn + màu nền thay đổi.

Hoàn thành tất cả màn = Chiến thắng 🎉.

👨‍💻 Tác giả : ME

Viết bằng Python + Pygame.

Dành cho mục đích học tập và giải trí.
