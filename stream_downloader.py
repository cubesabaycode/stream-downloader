import os
import re
import json
import time
import subprocess
from urllib.parse import urlparse, quote

import requests
import yt_dlp
from flask import Flask, request, jsonify, Response, render_template

app = Flask(__name__)

class StreamDownloader:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
    def get_video_info(self, url):
        """Get video information using yt-dlp Python module"""
        try:
            if self.is_facebook_url(url):
                return {
                    'success': False, 
                    'error': 'វីដេអូ Facebook មិនត្រូវបានគាំទ្រទេ ដោយសារការរឹតត្បិតវេទិកា។ សូមសាកល្បង YouTube, Instagram, ឬ TikTok វិញ។'
                }
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    if not info:
                        return {'success': False, 'error': 'មិនមានព័ត៌មានវីដេអូរកឃើញទេ។'}
                    
                    return {
                        'success': True,
                        'title': info.get('title', 'វីដេអូ'),
                        'duration': self.format_duration(info.get('duration', 0)),
                        'thumbnail': info.get('thumbnail', ''),
                        'uploader': info.get('uploader', 'មិនស្គាល់'),
                        'view_count': info.get('view_count', 0),
                        'description': info.get('description', '')[:100] + '...' if info.get('description') else ''
                    }
                except yt_dlp.DownloadError as e:
                    error_msg = str(e)
                    if 'No video formats found' in error_msg:
                        platform = self.get_platform_name(url)
                        return {'success': False, 'error': f'{platform} វីដេអូមិនអាចចូលប្រើបានទេ។ សូមសាកល្បងវីដេអូផ្សេង។'}
                    elif 'Private video' in error_msg or 'Sign in' in error_msg:
                        return {'success': False, 'error': 'វីដេអូនេះជាឯកជន ឬតម្រូវឲ្យចូលគណនី។'}
                    return {'success': False, 'error': f'កំហុសក្នុងការទាញយកព័ត៌មាន៖ {error_msg}'}
        except Exception as e:
            return {'success': False, 'error': f'កំហុសដែលមិនបានរំពឹងទុក៖ {str(e)}'}
    
    def is_facebook_url(self, url):
        return 'facebook.com' in url.lower() or 'fb.watch' in url.lower()
    
    def get_platform_name(self, url):
        url_lower = url.lower()
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower: return 'YouTube'
        if 'instagram.com' in url_lower: return 'Instagram'
        if 'tiktok.com' in url_lower: return 'TikTok'
        if 'facebook.com' in url_lower or 'fb.watch' in url_lower: return 'Facebook'
        return 'វេទិកានេះ'
    
    def format_duration(self, seconds):
        if not seconds: return 'មិនស្គាល់'
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
    
    def get_direct_stream_url(self, url, quality='best'):
        """Get direct stream URL using yt-dlp Python module"""
        try:
            if self.is_facebook_url(url):
                return {'success': False, 'error': 'វីដេអូ Facebook មិនត្រូវបានគាំទ្រទេ។'}
            
            # Format selection
            if quality == 'audio':
                format_spec = 'bestaudio[ext=m4a]/bestaudio/best'
            elif quality in ['360p', '480p', '720p', '1080p']:
                height = quality.replace('p', '')
                format_spec = f'best[height<={height}]/best'
            else:
                format_spec = 'best'
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': format_spec,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info and 'url' in info:
                    return {
                        'success': True,
                        'stream_url': info['url'],
                        'format': quality,
                        'ext': info.get('ext', 'mp4'),
                        'title': info.get('title', 'វីដេអូ')
                    }
                return {'success': False, 'error': 'គ្មានតំណស្ទ្រីមដែលអាចប្រើបានទេ។'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

downloader = StreamDownloader()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video-info', methods=['POST'])
def video_info():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
    return jsonify(downloader.get_video_info(data['url']))

@app.route('/get-download-link', methods=['POST'])
def get_download_link():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
    quality = data.get('quality', 'best')
    return jsonify(downloader.get_direct_stream_url(data['url'], quality))

def is_safe_url(url):
    """Basic SSRF protection"""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False
        # Block local/private IPs
        hostname = parsed.hostname.lower()
        if hostname in ['localhost', '127.0.0.1', '0.0.0.0', '::1']:
            return False
        # Simple check for private IP ranges
        if hostname.startswith('192.168.') or hostname.startswith('10.') or hostname.startswith('172.16.'):
            return False
        return True
    except:
        return False

@app.route('/stream-download')
def stream_download():
    """Stream download directly to user"""
    stream_url = request.args.get('url')
    filename = request.args.get('filename', 'video.mp4')
    
    if not stream_url or not is_safe_url(stream_url):
        return "Invalid or unsafe stream URL", 400
    
    def generate():
        try:
            # Add headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.youtube.com/'
            }
            with requests.get(stream_url, stream=True, timeout=60, headers=headers) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
        except Exception as e:
            app.logger.error(f"Streaming error: {e}")

    return Response(
        generate(),
        headers={
            'Content-Disposition': f'attachment; filename="{quote(filename)}"',
            'Content-Type': 'application/octet-stream'
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
