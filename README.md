# 🚀 Modern Video Downloader (Web Edition)

កម្មវិធីទាញយកវីដេអូទំនើបដែលបង្កើតឡើងដោយប្រើ Python Flask និង yt-dlp។ វាអនុញ្ញាតឱ្យអ្នកទាញយកវីដេអូពី YouTube, Instagram, និង TikTok ដោយផ្ទាល់តាមរយៈកម្មវិធីរុករក (Browser) របស់អ្នក។

## ✨ លក្ខណៈពិសេស (Features)

- **UI ទំនើប**: រចនាឡើងយ៉ាងស្អាត ងាយស្រួលប្រើ និងមានភាសាខ្មែរ។
- **គាំទ្រច្រើនវេទិកា**: YouTube, Instagram (Reels & Posts), និង TikTok។
- **គុណភាពចម្រុះ**: អាចជ្រើសរើសគុណភាពចាប់ពី 360p ដល់ 1080p ឬទាញយកតែសំឡេង។
- **ស្ទ្រីមផ្ទាល់**: មិនមានការរក្សាទុកឯកសារនៅលើម៉ាស៊ីនមេ (Server) ទេ — វីដេអូត្រូវបានបញ្ជូនដោយផ្ទាល់ទៅឧបករណ៍របស់អ្នក។
- **សុវត្ថិភាព**: បន្ថែមការការពារ SSRF និងការគ្រប់គ្រងកំហុសបានល្អប្រសើរ។

## 🚀 របៀបដំឡើង និងដំណើរការ (Quick Start)

### ១. ទាញយកកូដ (Clone Repository)
```bash
git clone https://github.com/cubesabaycode/stream-downloader.git
cd stream-downloader
```

### ២. ដំឡើងបណ្ណាល័យដែលត្រូវការ (Install Dependencies)
```bash
pip install -r requirements.txt
```

### ៣. ដំណើរការកម្មវិធី (Run Application)
```bash
python stream_downloader.py
```
បន្ទាប់មកបើក Browser ហើយចូលទៅកាន់ `http://localhost:5000`។

## 🛠️ បច្ចេកវិទ្យាដែលប្រើប្រាស់ (Tech Stack)

- **Backend**: Python, Flask
- **Core Engine**: yt-dlp
- **Frontend**: HTML5, CSS3 (Modern UI), JavaScript (Vanilla)
- **Deployment**: អាចដាក់ឱ្យដំណើរការលើ Render, Heroku ឬ VPS ផ្សេងៗ។

## 📝 ការកែសម្រួលថ្មីៗ (Recent Improvements)

- **Refactored Structure**: បំបែក HTML ចេញពីកូដ Python ទៅកាន់ `templates/`។
- **Enhanced UI**: រចនា UI ថ្មីឱ្យកាន់តែមានភាពទាក់ទាញ និងងាយស្រួលប្រើលើទូរស័ព្ទ។
- **Security Fix**: បន្ថែមការត្រួតពិនិត្យសុវត្ថិភាពលើ URL ដើម្បីការពារការវាយប្រហារ SSRF។
- **Khmer Localization**: កែសម្រួលសារជូនដំណឹង និងចំណុចប្រទាក់ជាភាសាខ្មែរឱ្យបានត្រឹមត្រូវ។

## 🤝 ការចូលរួម (Contributing)

យើងស្វាគមន៍រាល់ការចូលរួមចំណែក! ប្រសិនបើអ្នកមានបញ្ហា ឬចង់បន្ថែមមុខងារថ្មីៗ សូមបង្កើត Issue ឬ Pull Request។

## 📄 អាជ្ញាប័ណ្ណ (License)

គម្រោងនេះស្ថិតនៅក្រោមអាជ្ញាប័ណ្ណ [MIT License](LICENSE)។
