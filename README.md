# File Searcher

Advanced File Search Tool
Advanced File Search Tool / Công cụ Tìm kiếm File Nâng cao
A powerful, bilingual desktop application for searching text within documents and images.
Một ứng dụng desktop song ngữ mạnh mẽ để tìm kiếm văn bản bên trong tài liệu và hình ảnh.

English Version
A powerful desktop application built with Python and Tkinter that allows you to search for text within various file types, including .txt, .docx, .pdf, and even images (.png, .jpg) using OCR technology.

Screenshot
(Please add your application screenshot here. Save it as screenshot.png in the project folder.)
<img src="screenshot.png" alt="Application Screenshot" width="600"/>

Features
Intuitive Graphical User Interface (GUI): Easy to use for everyone, no command-line knowledge needed.
Multi-Format Search: Finds text in plain text files (.txt), Microsoft Word documents (.docx), and PDFs (.pdf).
Image Search with OCR: Extracts and searches for text within image files (.png, .jpg, .jpeg).
Responsive & Stable: Uses multi-threading to perform heavy tasks in the background, preventing the UI from freezing ("Not Responding").
Bilingual Support (English/Vietnamese): Switch between languages with a single click.
Automatic Dependency Installation: Automatically checks and installs required Python libraries using pip.

Requirements
Before running the application, you need to have the following installed on your system.
Python 3.6+
Tesseract OCR Engine: This is crucial for searching inside images. The script cannot install this for you.

Windows:
Download the installer from UB-Mannheim Tesseract GitHub.
Important: During installation, make sure to check the box to "Add Tesseract to system PATH".

macOS:
Use Homebrew: brew install tesseract

Linux (Debian/Ubuntu):
Use apt-get: sudo apt-get install tesseract-ocr

How to Run
Download the code: Clone this repository or download the .py file to your computer.
Open a terminal: Open Command Prompt (on Windows) or Terminal (on macOS/Linux).
Navigate to the folder: Use the cd command to go to the directory where you saved the file.

bash
cd path/to/your/folder
Run the script:

bash
python your_script_name.py
(Replace your_script_name.py with the actual name of the file.)

Automatic Installation: The first time you run the script, it will check for required Python libraries (python-docx, PyMuPDF, pytesseract, Pillow) and install them if they are missing. Please ensure you have an active internet connection.

How to Use the Application
Select a folder to search in: Click the "Browse..." button to choose the root folder you want to search.
Enter the phrase to find: Type the exact word or phrase you are looking for in this text box.
Select file types to search: Check the boxes for the file extensions you want to include in the search.
Start Search: Click this button to begin the search process. The UI will remain responsive.
Reset: Clears all inputs and results to start a new search.
Search Results: This area will display a real-time log of the files being scanned and any matches found.
Language Toggle: The button in the top-right corner allows you to switch the UI language.

For Developers
The application's core logic is designed to be non-blocking. It utilizes:
threading: The entire file search operation runs in a separate worker thread to keep the GUI responsive.
queue: A thread-safe queue is used for communication between the worker thread and the main GUI thread.
State Management: A state flag (self.is_searching) properly manages the lifecycle of the queue-checking loop, preventing resource leaks and crashes on subsequent runs.

License
This project is licensed under the MIT License.

Phiên bản Tiếng Việt
Đây là một ứng dụng desktop mạnh mẽ được xây dựng bằng Python và Tkinter, cho phép bạn tìm kiếm văn bản bên trong nhiều loại file khác nhau, bao gồm .txt, .docx, .pdf, và thậm chí cả file ảnh (.png, .jpg) nhờ công nghệ OCR.

Ảnh chụp màn hình
(Vui lòng thêm ảnh chụp màn hình ứng dụng của bạn tại đây. Lưu ảnh với tên screenshot.png trong thư mục dự án.)
<img src="screenshot.png" alt="Ảnh chụp màn hình ứng dụng" width="600"/>

Tính năng
Giao diện đồ họa (GUI) trực quan: Dễ sử dụng cho mọi người, không cần kiến thức về dòng lệnh.
Tìm kiếm đa định dạng: Tìm văn bản trong các file văn bản thuần túy (.txt), tài liệu Microsoft Word (.docx), và PDF (.pdf).
Tìm kiếm trong ảnh với OCR: Trích xuất và tìm kiếm văn bản bên trong các file ảnh (.png, .jpg, .jpeg).
Phản hồi nhanh & Ổn định: Sử dụng đa luồng để thực hiện các tác vụ nặng trong nền, giúp giao diện không bị treo ("Not Responding").
Hỗ trợ Song ngữ (Anh/Việt): Chuyển đổi ngôn ngữ chỉ với một cú nhấp chuột.
Tự động cài đặt thư viện: Tự động kiểm tra và cài đặt các thư viện Python cần thiết thông qua pip.

Yêu cầu
Trước khi chạy ứng dụng, bạn cần cài đặt các thành phần sau trên hệ thống của mình.
Python 3.6+
Tesseract OCR Engine: Đây là thành phần cốt lõi để tìm kiếm trong ảnh. Script không thể tự cài đặt Tesseract cho bạn.

Windows:
Tải bộ cài đặt từ GitHub của Tesseract tại UB-Mannheim.
Quan trọng: Trong quá trình cài đặt, hãy đảm bảo bạn đã tích vào ô "Add Tesseract to system PATH".

macOS:
Sử dụng Homebrew: brew install tesseract
Linux (Debian/Ubuntu):
Sử dụng apt-get: sudo apt-get install tesseract-ocr
Để nhận dạng tiếng Việt, cài thêm gói ngôn ngữ: sudo apt-get install tesseract-ocr-vie

Cách chạy
Tải mã nguồn: Clone repository này hoặc tải file .py về máy tính của bạn.
Mở terminal: Mở Command Prompt (trên Windows) hoặc Terminal (trên macOS/Linux).
Đi đến thư mục: Sử dụng lệnh cd để di chuyển đến thư mục bạn đã lưu file.

bash
cd duong/dan/den/thu_muc
Chạy script:

bash
python ten_file_cua_ban.py
(Thay thế ten_file_cua_ban.py bằng tên thật của file.)

Cài đặt tự động: Lần đầu tiên chạy, script sẽ kiểm tra các thư viện Python cần thiết (python-docx, PyMuPDF, pytesseract, Pillow) và tự động cài đặt nếu thiếu. Hãy đảm bảo bạn có kết nối Internet.

Cách sử dụng Ứng dụng
Chọn thư mục để tìm kiếm: Nhấn nút "Chọn Thư Mục..." để mở cửa sổ và chọn thư mục gốc bạn muốn tìm kiếm.
Nhập cụm từ cần tìm: Gõ từ hoặc cụm từ chính xác bạn muốn tìm vào ô văn bản này.
Chọn loại file để tìm kiếm: Tích vào các ô tương ứng với các loại file bạn muốn tìm kiếm.
Bắt đầu Tìm kiếm: Nhấn nút này để bắt đầu quá trình tìm kiếm. Giao diện sẽ luôn phản hồi.
Làm lại: Xóa toàn bộ các lựa chọn và kết quả để bắt đầu một lượt tìm kiếm mới.
Kết quả tìm kiếm: Khu vực này sẽ hiển thị nhật ký thời gian thực về các file đang được quét và các kết quả tìm thấy.
Chuyển đổi Ngôn ngữ: Nút ở góc trên bên phải cho phép bạn chuyển đổi ngôn ngữ của toàn bộ giao diện.

Ghi chú cho Lập trình viên
Logic cốt lõi của ứng dụng được thiết kế để không gây tắc nghẽn giao diện. Nó tận dụng:
threading: Toàn bộ hoạt động tìm kiếm file chạy trên một luồng nền riêng biệt để giữ cho GUI luôn phản hồi.
queue: Một hàng đợi an toàn cho luồng được sử dụng để giao tiếp giữa luồng nền và luồng GUI chính.
Quản lý Trạng thái: Một cờ trạng thái (self.is_searching) được sử dụng để quản lý vòng đời của vòng lặp kiểm tra hàng đợi, ngăn chặn rò rỉ tài nguyên và sự cố khi chạy nhiều lần.
Giấy phép
Dự án này được cấp phép theo Giấy phép MIT.
