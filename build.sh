VERSION="2.0.4"
rm -rf "build/StreamChat FX-$VERSION-Windows-x64"
python -m nuitka\
    --file-description="Custom Themes & Effects for Live Stream Chats"\
    --include-data-files="config.example.json=config.json"\
    --windows-icon-from-ico="assets/icon/icon.ico"\
    --output-filename="streamchatfx.exe"\
    --include-data-dir="static=static"\
    --include-data-dir="theme=theme"\
    --product-name="StreamChat FX"\
    --product-version="$VERSION"\
    --file-version="$VERSION"\
    --output-dir="build"\
    --remove-output\
    --show-progress\
    --standalone\
    --deployment\
    --lto=yes\
    src/main.py
mv build/main.dist "build/StreamChat FX-$VERSION-Windows-x64"