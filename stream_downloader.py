from flask import Flask, request, jsonify, Response, render_template_string
import subprocess
import requests
import re
import time
from urllib.parse import quote
import json
import os

app = Flask(__name__)

# Install yt-dlp on startup if not available
def ensure_yt_dlp():
    try:
        # Try to import yt-dlp to check if it's available
        import yt_dlp
        print("✅ yt-dlp is available")
        return True
    except ImportError:
        print("❌ yt-dlp not found, installing...")
        try:
            subprocess.run([
                'pip', 'install', 'yt-dlp'
            ], check=True, capture_output=True)
            print("✅ yt-dlp installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install yt-dlp: {e}")
            return False

# Check on startup
ensure_yt_dlp()

class StreamDownloader:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
    def get_video_info(self, url):
        """Get video information using yt-dlp Python module"""
        try:
            import yt_dlp
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    
                    if info:
                        return {
                            'success': True,
                            'title': info.get('title', 'video'),
                            'duration': self.format_duration(info.get('duration', 0)),
                            'thumbnail': info.get('thumbnail', ''),
                            'uploader': info.get('uploader', 'Unknown'),
                            'view_count': info.get('view_count', 0),
                            'description': info.get('description', '')[:100] + '...' if info.get('description') else ''
                        }
                    else:
                        return {'success': False, 'error': 'No video information found'}
                        
                except yt_dlp.DownloadError as e:
                    return {'success': False, 'error': f'Video not available: {str(e)}'}
                except Exception as e:
                    return {'success': False, 'error': f'Error extracting info: {str(e)}'}
                    
        except ImportError:
            return {'success': False, 'error': 'yt-dlp not available'}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def format_duration(self, seconds):
        """Convert duration in seconds to readable format"""
        if not seconds:
            return 'Unknown'
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    def get_direct_stream_url(self, url, quality='best'):
        """Get direct stream URL using yt-dlp Python module"""
        try:
            import yt_dlp
            
            # Format selection based on quality
            if quality == 'audio':
                format_spec = 'bestaudio[ext=m4a]/bestaudio/best'
            elif quality == '360p':
                format_spec = 'best[height<=360]/best'
            elif quality == '480p':
                format_spec = 'best[height<=480]/best'
            elif quality == '720p':
                format_spec = 'best[height<=720]/best'
            elif quality == '1080p':
                format_spec = 'best[height<=1080]/best'
            else:
                format_spec = 'best'
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': format_spec,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    
                    if info and 'url' in info:
                        return {
                            'success': True,
                            'stream_url': info['url'],
                            'format': quality,
                            'ext': info.get('ext', 'mp4'),
                            'title': info.get('title', 'video')
                        }
                    else:
                        return {'success': False, 'error': 'No stream URL available'}
                        
                except yt_dlp.DownloadError as e:
                    return {'success': False, 'error': f'Cannot access video: {str(e)}'}
                except Exception as e:
                    return {'success': False, 'error': f'Error getting stream: {str(e)}'}
                    
        except ImportError:
            return {'success': False, 'error': 'yt-dlp not available'}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}

stream_downloader = StreamDownloader()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Direct Stream Downloader</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 1.1em;
            line-height: 1.5;
        }
        .platforms {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .platform-tag {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }
        .youtube { background: #FF0000; color: white; }
        .instagram { background: #E4405F; color: white; }
        .tiktok { background: #000000; color: white; }
        .facebook { background: #1877F2; color: white; }
        
        .input-section {
            margin-bottom: 25px;
        }
        .url-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 15px;
            transition: border-color 0.3s;
        }
        .url-input:focus {
            outline: none;
            border-color: #667eea;
        }
        .options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        .option-group {
            display: flex;
            flex-direction: column;
        }
        .option-group label {
            font-weight: 600;
            margin-bottom: 5px;
            color: #333;
        }
        .option-select {
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 14px;
            background: white;
        }
        .download-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .download-btn:hover {
            transform: translateY(-2px);
        }
        .download-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        .result.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .result.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .result.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .video-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            display: none;
        }
        .video-info img {
            max-width: 200px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .progress-bar {
            width: 100%;
            height: 6px;
            background: #e1e5e9;
            border-radius: 3px;
            margin: 15px 0;
            overflow: hidden;
            display: none;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
        }
        
        .direct-download-btn {
            display: inline-block;
            padding: 12px 25px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 10px;
            transition: background 0.3s;
        }
        .direct-download-btn:hover {
            background: #218838;
            color: white;
        }
        
        .feature-list {
            margin: 25px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .feature-list ul {
            list-style: none;
            padding: 0;
        }
        .feature-list li {
            padding: 8px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .feature-list li:before {
            content: "✅";
        }

        .error-details {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .options {
                grid-template-columns: 1fr;
            }
            .container {
                padding: 20px;
            }
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Direct Stream Downloader</h1>
            <p>Download videos directly to your device - No server storage used!</p>
            
            <div class="platforms">
                <div class="platform-tag youtube">YouTube</div>
                <div class="platform-tag instagram">Instagram</div>
                <div class="platform-tag tiktok">TikTok</div>
                <div class="platform-tag facebook">Facebook</div>
            </div>
        </div>

        <div class="feature-list">
            <ul>
                <li>Supports YouTube, Facebook, TikTok, Instagram</li>
                <li>No file saving on server — direct stream</li>
                <li>Render-compatible (Free Tier)</li>
                <li>Uses only free-tier services</li>
                <li>Auto "Save As..." download to user device</li>
                <li>Works cross-platform (Windows, Linux, macOS, mobile)</li>
            </ul>
        </div>

        <div class="input-section">
            <input type="url" class="url-input" id="videoUrl" 
                   placeholder="Paste video URL here (YouTube, Instagram, TikTok, Facebook)..."
                   value="https://www.youtube.com/watch?v=9bZkp7q19f0">
            
            <div class="options">
                <div class="option-group">
                    <label for="quality">📹 Quality:</label>
                    <select id="quality" class="option-select">
                        <option value="best">Best Quality</option>
                        <option value="1080p">1080p</option>
                        <option value="720p">720p</option>
                        <option value="480p">480p</option>
                        <option value="360p">360p</option>
                        <option value="audio">Audio Only (MP3/M4A)</option>
                    </select>
                </div>
                
                <div class="option-group">
                    <label for="platform">🌐 Platform:</label>
                    <select id="platform" class="option-select" disabled>
                        <option value="auto">Auto Detect</option>
                        <option value="youtube">YouTube</option>
                        <option value="instagram">Instagram</option>
                        <option value="tiktok">TikTok</option>
                        <option value="facebook">Facebook</option>
                    </select>
                </div>
            </div>

            <button class="download-btn" id="downloadBtn">🎬 Get Download Link</button>
            
            <div class="progress-bar" id="progressBar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            
            <div class="video-info" id="videoInfo">
                <div id="videoInfoContent"></div>
            </div>
            
            <div class="result" id="result"></div>
        </div>
    </div>

    <script>
        class StreamDownloader {
            constructor() {
                this.downloadBtn = document.getElementById('downloadBtn');
                this.videoUrl = document.getElementById('videoUrl');
                this.quality = document.getElementById('quality');
                this.result = document.getElementById('result');
                this.progressBar = document.getElementById('progressBar');
                this.progressFill = document.getElementById('progressFill');
                this.videoInfo = document.getElementById('videoInfo');
                this.videoInfoContent = document.getElementById('videoInfoContent');
                
                this.bindEvents();
                this.detectPlatform();
            }
            
            bindEvents() {
                this.downloadBtn.addEventListener('click', () => this.getDownloadLink());
                this.videoUrl.addEventListener('input', () => {
                    this.detectPlatform();
                    this.hideVideoInfo();
                });
                this.videoUrl.addEventListener('paste', () => setTimeout(() => this.detectPlatform(), 100));
            }
            
            detectPlatform() {
                const url = this.videoUrl.value.toLowerCase();
                let platform = 'auto';
                
                if (url.includes('youtube.com') || url.includes('youtu.be')) {
                    platform = 'youtube';
                } else if (url.includes('instagram.com')) {
                    platform = 'instagram';
                } else if (url.includes('tiktok.com')) {
                    platform = 'tiktok';
                } else if (url.includes('facebook.com') || url.includes('fb.watch')) {
                    platform = 'facebook';
                }
                
                document.getElementById('platform').value = platform;
            }
            
            hideVideoInfo() {
                this.videoInfo.style.display = 'none';
                this.result.style.display = 'none';
            }
            
            async getDownloadLink() {
                const url = this.videoUrl.value.trim();
                const quality = this.quality.value;
                
                if (!url) {
                    this.showResult('Please enter a video URL', 'error');
                    return;
                }
                
                if (!this.isValidUrl(url)) {
                    this.showResult('Please enter a valid URL', 'error');
                    return;
                }
                
                this.downloadBtn.disabled = true;
                this.downloadBtn.textContent = 'Getting video info...';
                this.progressBar.style.display = 'block';
                this.progressFill.style.width = '30%';
                this.hideVideoInfo();
                
                try {
                    // First get video info
                    this.showResult('🔍 Getting video information...', 'info');
                    
                    const infoResponse = await fetch('/video-info', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            url: url,
                            quality: quality
                        })
                    });
                    
                    const infoData = await infoResponse.json();
                    
                    if (infoData.success) {
                        this.progressFill.style.width = '60%';
                        this.showVideoInfo(infoData);
                        this.showResult('✅ Video info loaded! Getting download link...', 'success');
                        
                        // Now get download link
                        this.downloadBtn.textContent = 'Getting download link...';
                        
                        const downloadResponse = await fetch('/get-download-link', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                url: url,
                                quality: quality
                            })
                        });
                        
                        const downloadData = await downloadResponse.json();
                        this.progressFill.style.width = '100%';
                        
                        if (downloadData.success) {
                            this.showDownloadLink(downloadData, infoData);
                        } else {
                            this.showResult(`❌ Error getting download link: ${downloadData.error}`, 'error');
                        }
                    } else {
                        this.showResult(`❌ Error getting video info: ${infoData.error}`, 'error');
                    }
                    
                } catch (error) {
                    this.showResult(`❌ Network error: ${error.message}`, 'error');
                } finally {
                    this.resetUI();
                }
            }
            
            showVideoInfo(info) {
                let html = `
                    <h3>🎥 ${info.title}</h3>
                    <p><strong>Creator:</strong> ${info.uploader}</p>
                    <p><strong>Duration:</strong> ${info.duration}</p>
                    <p><strong>Views:</strong> ${info.view_count?.toLocaleString() || 'Unknown'}</p>
                `;
                
                if (info.thumbnail) {
                    html = `<img src="${info.thumbnail}" alt="Thumbnail" onerror="this.style.display='none'"><br>` + html;
                }
                
                this.videoInfoContent.innerHTML = html;
                this.videoInfo.style.display = 'block';
            }
            
            showDownloadLink(downloadData, infoData) {
                const fileExt = downloadData.format === 'audio' ? '.m4a' : '.mp4';
                const filename = this.sanitizeFilename(infoData.title) + fileExt;
                
                const downloadUrl = `/stream-download?url=${encodeURIComponent(downloadData.stream_url)}&filename=${encodeURIComponent(filename)}`;
                
                const message = `
                    <div style="text-align: center;">
                        <h3>✅ Ready to Download!</h3>
                        <p><strong>File:</strong> ${filename}</p>
                        <p><strong>Quality:</strong> ${downloadData.format}</p>
                        <p><strong>Format:</strong> ${downloadData.ext?.toUpperCase() || 'MP4'}</p>
                        <br>
                        <a href="${downloadUrl}" class="direct-download-btn" download="${filename}">
                            ⬇️ Download Now (Save As...)
                        </a>
                        <p style="margin-top: 10px; font-size: 0.9em; color: #666;">
                            Clicking will start direct download to your device
                        </p>
                    </div>
                `;
                
                this.showResult(message, 'success');
            }
            
            sanitizeFilename(name) {
                return name.replace(/[^a-z0-9]/gi, '_').substring(0, 50);
            }
            
            isValidUrl(string) {
                try {
                    new URL(string);
                    return true;
                } catch (_) {
                    return false;
                }
            }
            
            showResult(message, type) {
                this.result.innerHTML = message;
                this.result.className = `result ${type}`;
                this.result.style.display = 'block';
            }
            
            resetUI() {
                this.downloadBtn.disabled = false;
                this.downloadBtn.textContent = '🎬 Get Download Link';
                setTimeout(() => {
                    this.progressBar.style.display = 'none';
                    this.progressFill.style.width = '0%';
                }, 1000);
            }
        }
        
        // Initialize the downloader
        const downloader = new StreamDownloader();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video-info', methods=['POST'])
def video_info():
    """Get video information"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'})
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({'success': False, 'error': 'Invalid URL format'})
        
        info = stream_downloader.get_video_info(url)
        return jsonify(info)
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/get-download-link', methods=['POST'])
def get_download_link():
    """Get direct download link"""
    try:
        data = request.get_json()
        url = data.get('url')
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'})
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({'success': False, 'error': 'Invalid URL format'})
        
        stream_info = stream_downloader.get_direct_stream_url(url, quality)
        return jsonify(stream_info)
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/stream-download')
def stream_download():
    """Stream download directly to user"""
    try:
        stream_url = request.args.get('url')
        filename = request.args.get('filename', 'video.mp4')
        
        if not stream_url:
            return "No stream URL provided", 400
        
        # Validate stream URL
        if not stream_url.startswith(('http://', 'https://')):
            return "Invalid stream URL", 400
        
        # Stream the video directly to the user
        def generate():
            try:
                response = requests.get(
                    stream_url, 
                    stream=True, 
                    timeout=30,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
                response.raise_for_status()
                
                # Stream chunks to client
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
                    
            except requests.exceptions.RequestException as e:
                yield f"Error streaming video: {str(e)}".encode()
            except Exception as e:
                yield f"Unexpected error: {str(e)}".encode()
        
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'application/octet-stream'
        }
        
        return Response(
            generate(), 
            headers=headers, 
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'Direct Stream Downloader',
        'yt_dlp_available': ensure_yt_dlp()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Direct Stream Downloader Started!")
    print(f"📍 Open: http://localhost:{port}")
    print("🎯 Features:")
    print("   ✅ Supports: YouTube, Facebook, TikTok, Instagram") 
    print("   ✅ No file saving on server — direct stream")
    print("   ✅ Render-compatible (Free Tier)")
    print("   ✅ Uses only free-tier services")
    print("   ✅ Auto 'Save As...' download to user device")
    print("   ✅ Works cross-platform")
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # This allows gunicorn to find the app
    app = app