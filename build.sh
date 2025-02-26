rm build -rf
python -m nuitka\
    --file-description="A tool to get live stream chat data from YouTube."\
    --windows-icon-from-ico="assets/icon/icon.ico"\
    --output-filename="yt_chat_stream.exe"\
    --report="build/nuitka-report.xml"\
    --product-name="YT Chat Stream"\
    --product-version="2.0.0"\
    --file-version="2.0.0"\
    --output-dir="build"\
    --show-progress\
    --standalone\
    --lto=yes\
    src/main.py