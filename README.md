# 📥 Modern Video Downloader

A modern, cross-platform GUI application for downloading videos from YouTube, Facebook, TikTok, and Instagram. Built with Python and Tkinter, featuring an Apple-inspired design with colorful, intuitive controls.

![Modern UI](https://img.shields.io/badge/UI-Modern-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)

## ✨ Features

### 🎨 Modern User Interface
- **Apple-inspired design** with clean, minimalist aesthetics
- **Two-column layout** for intuitive workflow
- **Colorful buttons** with hover effects
- **Responsive design** that scales beautifully

### 📥 Download Capabilities
- **Multi-platform support**: YouTube, Facebook, TikTok, Instagram
- **Batch downloading**: Process multiple URLs simultaneously
- **Video ID filenames**: Automatic naming using video IDs
- **Best quality**: Downloads highest available quality

### 🎯 Smart Controls
- **One-click operations**: Clear, paste, browse with colorful buttons
- **Real-time progress**: Live progress bar and status updates
- **Download counters**: Track total, success, and failed downloads
- **Comprehensive logging**: Detailed log with emoji indicators

### 🔧 Technical Features
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Threaded downloads**: Non-blocking UI during downloads
- **Auto-folder opening**: Automatically opens download folder when complete
- **Error handling**: Robust error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- yt-dlp executable

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd video-downloader
   ```

2. **Install yt-dlp**
   ```bash
   # Linux/macOS
   sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
   sudo chmod a+rx /usr/local/bin/yt-dlp
   
   # Windows
   # Download yt-dlp.exe from https://github.com/yt-dlp/yt-dlp/releases
   # Place it in the same folder as the script or add to PATH
   ```

3. **Run the application**
   ```bash
   python3 video_downloader.py
   ```

## 📖 How to Use

### Step-by-Step Guide

1. **Launch the Application**
   - Run `python3 video_downloader.py`
   - Check that yt-dlp status shows "✅ Ready"

2. **Add Video URLs**
   - Click **"📋 Paste Links"** (Blue button) to paste from clipboard
   - Or manually type URLs (one per line)
   - URL counter updates automatically

3. **Set Download Location**
   - Default: Your system's Downloads folder
   - Click **"Browse"** (Green button) to choose custom location

4. **Start Download**
   - Click **"🚀 Download All Videos"** (Purple button)
   - Monitor progress in real-time

5. **Monitor Progress**
   - Watch the progress bar advance
   - Check counters: Total, Success, Failed
   - Read detailed log messages

6. **Completion**
   - Success message appears when done
   - Download folder opens automatically
   - Check log for any issues

### Button Reference

| Button | Color | Purpose | Usage |
|--------|-------|---------|-------|
| 🗑️ Clear Links | Red | Remove all URLs | Start fresh or correct mistakes |
| 📋 Paste Links | Blue | Paste from clipboard | Quick URL input |
| 📁 Browse | Green | Choose folder | Custom download location |
| 🚀 Download All | Purple | Start download | Begin downloading all videos |
| ⏹️ Stop | Orange | Stop download | Cancel current operation |

## 🛠️ Technical Details

### Supported Platforms
- **YouTube**: `youtube.com`, `youtu.be` URLs
- **Facebook**: Video post URLs
- **TikTok**: Video page URLs
- **Instagram**: Post and reel URLs

### File Naming
- Uses video ID for filenames (e.g., `abc123.mp4`, `fb_xyz789.mp4`)
- Prevents duplicate filenames
- Maintains file extension based on format

### System Requirements
- **Python**: 3.8 or higher
- **Dependencies**: tkinter (usually included with Python)
- **Storage**: Enough space for downloaded videos
- **Network**: Internet connection for downloads

## 🔍 Troubleshooting

### Common Issues

**"yt-dlp not found" error**
```bash
# Reinstall yt-dlp
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

**App won't start**
```bash
# Install tkinter if missing (Ubuntu/Debian)
sudo apt update
sudo apt install python3-tk
```

**Download fails for specific videos**
- Check URL validity and accessibility
- Verify video isn't private or region-restricted
- Check log for specific error messages

**Permission errors**
```bash
# Ensure yt-dlp is executable
chmod +x /usr/local/bin/yt-dlp
```

### Log Messages Guide

- ✅ **Success**: Video downloaded successfully
- ❌ **Failed**: Download failed (check error message)
- 📥 **Downloading**: Currently downloading
- 🗑️ **Cleared**: URLs cleared from input
- 📋 **Pasted**: URLs pasted from clipboard
- 📁 **Folder set**: Download location changed
- 🛑 **Stopped**: Download stopped by user
- 📂 **Folder opened**: Download folder opened automatically

## 🎨 UI Overview

### Left Panel - Configuration
- **URL Input**: Large text area for video URLs
- **Action Buttons**: Clear, paste, and folder selection
- **Download Location**: Current save folder path

### Right Panel - Monitoring
- **Progress Tracking**: Real-time progress bar and status
- **Counters**: Large, colorful counters for tracking
- **Control Buttons**: Download and stop operations
- **Activity Log**: Detailed download history with timestamps

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **yt-dlp**: For the excellent video downloading backend
- **Python & Tkinter**: For the robust GUI framework
- **Apple Design**: Inspiration for the modern UI aesthetics

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the log messages for specific errors
3. Ensure yt-dlp is properly installed and accessible
4. Verify URLs are from supported platforms

---

**Happy Downloading!** 🎉
