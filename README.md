# GPA Advisor System

## Mô tả
Hệ thống tư vấn học tập AI sử dụng Selenium để crawl dữ liệu bảng điểm và AI Agent để phân tích, đưa ra lời khuyên học tập.

## Tính năng chính
- Crawl dữ liệu bảng điểm từ portal sinh viên (sử dụng Selenium)
- Chuyển đổi dữ liệu JSON thành DocumentKnowledgeBase để phân tích
- AI Agent phân tích và đưa ra gợi ý cải thiện học tập
- Debug logging đầy đủ và error handling
- Xử lý timing issues và file synchronization

## Cấu trúc dự án

```
.
├── gpa_advisor.py          # File chính chứa toàn bộ hệ thống
├── test_gpa_advisor.py     # Test script với mock data
├── requirements.txt        # Dependencies
├── ket_qua.json           # Dữ liệu bảng điểm được crawl
├── analysis_result.json   # Kết quả phân tích của AI
├── knowledge_base/        # Thư mục chứa documents đã convert
│   ├── document_1.txt     # Thông tin sinh viên
│   ├── document_2.txt     # Tổng kết điểm GPA
│   ├── document_3.txt     # Học kỳ 1
│   ├── document_4.txt     # Học kỳ 2
│   ├── document_5.txt     # Học kỳ 3
│   └── document_6.txt     # Phân tích hiệu quả học tập
└── gpa_advisor.log        # Log file để debug
```

## Các vấn đề đã được giải quyết

### 1. **Thay thế JSONKnowledgeBase bằng DocumentKnowledgeBase**
- JSONKnowledgeBase không tương thích với cấu trúc dữ liệu crawl
- DocumentKnowledgeBase chuyển đổi JSON thành text có cấu trúc
- Dễ dàng control và debug hơn

### 2. **Fix timing issues**
- Thêm `time.sleep()` và file flush để đảm bảo JSON được ghi hoàn toàn
- Sử dụng `recreate=True` để force reload dữ liệu mới
- Verify file size trước khi load vào knowledge base

### 3. **Cải thiện error handling và logging**
- Debug logging đầy đủ cho mọi bước
- Verify file tồn tại và có content trước khi xử lý
- Exception handling chi tiết

### 4. **Cấu trúc dữ liệu tối ưu cho AI Agent**
- Chuyển đổi JSON thành text có cấu trúc rõ ràng
- Tách riêng thông tin sinh viên, GPA summary, từng học kỳ
- Tạo document phân tích riêng cho thế mạnh/yếu điểm

### 5. **AI Agent instructions tối ưu**
- Phân tích dữ liệu từ multiple documents
- Đưa ra recommendations dựa trên GPA thực tế
- Output format chuẩn với đầy đủ thông tin

## Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cài đặt Chrome browser (cho production)
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Hoặc cài chromedriver riêng
```

### 3. Chạy test với mock data
```bash
python test_gpa_advisor.py
```

### 4. Chạy hệ thống đầy đủ (cần Chrome)
```bash
python gpa_advisor.py
```

## Kết quả đầu ra

Hệ thống sẽ tạo ra:

### `ket_qua.json` - Dữ liệu crawl được
```json
{
  "student_info": {...},
  "academic_records": [...],
  "gpa_summary": {...}
}
```

### `analysis_result.json` - Phân tích AI
```json
{
  "nhan_xet": "Kết quả học tập khá với GPA 7.65...",
  "mon_can_cai_thien": ["Hệ điều hành", "Cơ sở dữ liệu"],
  "hoc_phan_uu_tien": ["Hệ điều hành", "Cơ sở dữ liệu", "An toàn thông tin"],
  "ke_hoach": {
    "thoi_gian": "2 học kỳ",
    "chien_luoc": "Cải thiện điểm các môn yếu, tăng cường ôn tập"
  }
}
```

## So sánh Before/After

### Before (Vấn đề)
```json
{
  "nhan_xet": "Không có dữ liệu bảng điểm cụ thể...",
  "mon_can_cai_thien": [],
  "hoc_phan_uu_tien": [],
  "ke_hoach": {
    "thoi_gian": "2 học kỳ",
    "chien_luoc": "Học nhóm, tăng thời gian tự học, tôn tổt cấm nang học"
  }
}
```

### After (Đã fix)
```json
{
  "nhan_xet": "Kết quả học tập khá với GPA 7.65. Đã phân tích 12 môn học...",
  "mon_can_cai_thien": ["Hệ điều hành", "Cơ sở dữ liệu", "An toàn thông tin"],
  "hoc_phan_uu_tien": ["Hệ điều hành", "Cơ sở dữ liệu", "An toàn thông tin"],
  "ke_hoach": {
    "thoi_gian": "2 học kỳ",
    "chien_luoc": "Cải thiện điểm các môn yếu, tăng cường ôn tập",
    "ghi_chu": "Ưu tiên cải thiện 3 môn học có điểm thấp"
  }
}
```

## Architecture

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│ TranscriptCrawler│───▶│ DocumentKnowledgeBase│───▶│ GPAAnalysisAgent   │
│ (Selenium)      │    │ (Convert JSON→Text)  │    │ (AI Analysis)      │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
        │                         │                           │
        ▼                         ▼                           ▼
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   ket_qua.json  │    │   knowledge_base/    │    │ analysis_result.json│
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
```

## Debug và Troubleshooting

### Log files
- `gpa_advisor.log` - Log chính cho debugging
- `gpa_advisor_test.log` - Log cho test runs

### Common issues
1. **Chrome driver not found**: Cài đặt chromedriver hoặc Chrome browser
2. **Permission denied**: Chạy với sudo nếu cần thiết
3. **File not found**: Kiểm tra paths và working directory
4. **Empty analysis**: Kiểm tra knowledge base loading trong logs

## Customization

### Thay đổi URL crawling
Sửa trong `TranscriptCrawler.crawl_transcript_data()` để trỏ đến portal thực tế.

### Tùy chỉnh AI analysis
Sửa logic trong `GPAAnalysisAgent._perform_analysis()` để thay đổi cách phân tích.

### Thêm document types
Mở rộng `_convert_json_to_documents()` để tạo thêm document types.