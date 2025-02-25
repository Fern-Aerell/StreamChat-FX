rm build -rf
python -m nuitka\
    --standalone\
    --output-filename="yt_live_chat_service.exe"\
    --product-name="YT Live Chat Service"\
    --product-version="1.0.0"\
    --file-version="1.0.0"\
    --file-description="A live chat service for YouTube live chat streams."\
    --lto=yes\
    --report="build/nuitka-report.xml"\
    --output-dir="build"\
    --show-progress\
    src/main.py