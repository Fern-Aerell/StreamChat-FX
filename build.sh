python -m nuitka\
    --file-description="Custom Themes & Effects for Live Stream Chats"\
    --windows-icon-from-ico="assets/icon/icon.ico"\
    --output-filename="streamchatfx.exe"\
    --report="build/nuitka-report.xml"\
    --product-name="StreamChat FX"\
    --product-version="2.0.0"\
    --file-version="2.0.0"\
    --output-dir="build"\
    --show-progress\
    --standalone\
    --lto=yes\
    src/main.py
cp config.example.json build/main.dist/config.json
cp -r static build/main.dist/static
cp -r theme build/main.dist/theme