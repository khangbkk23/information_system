# Trực Quan Hóa Số Tín Chỉ Bằng Biểu Đồ Sunburst

## Tổng Quan
Tập lệnh Python này đọc dữ liệu khóa học từ tệp Excel và trực quan hóa phân bổ số tín chỉ bằng **Biểu Đồ Sunburst**. Dữ liệu được lọc để chỉ bao gồm các khóa học bằng tiếng Việt và được nhóm theo học kỳ, loại môn học và tên học phần.

## Tính Năng
- Đọc dữ liệu từ tệp Excel (`dataset-406H.xlsx`)
- Làm sạch tên cột và lọc dữ liệu cho các khóa học tiếng Việt
- Nhóm và xử lý dữ liệu để tính tổng số tín chỉ theo học kỳ
- Tạo **Biểu Đồ Sunburst** bằng `plotly.graph_objects`
- Xuất tệp HTML tương tác (`chart.html`) để trực quan hóa

## Yêu Cầu
Đảm bảo bạn đã cài đặt các thư viện Python sau:

```bash
pip install pandas plotly openpyxl
