rm build -rf
python -m nuitka\
    --standalone\
    --output-filename="yt_chat_stream.exe"\
    --product-name="YT Chat Stream"\
    --product-version="2.0.0"\
    --file-version="2.0.0"\
    --file-description="Alat untuk mengalirkan data live chat dari YouTube."\
    --lto=yes\
    --report="build/nuitka-report.xml"\
    --output-dir="build"\
    --show-progress\
    src/main.py