# 🚀 Quick Start Guide

## Get Running in 5 Minutes

### Option 1: Local Testing (Recommended First)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run KatScan.py
```

Open your browser to `http://localhost:8501` 🎉

### Option 2: Deploy to Streamlit Cloud (BEST for Production)

**⚠️ Important: Do NOT use Vercel for Streamlit apps!** Use Streamlit Community Cloud instead.

#### Steps:

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/kat-scanner.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to: https://share.streamlit.io
   - Click "New app"
   - Select your repository
   - Main file: `KatScan.py`
   - Click "Deploy"

3. **Done!** Your app will be live at:
   `https://YOUR-USERNAME-kat-scanner.streamlit.app`

### Option 3: Other Platforms

See `DEPLOYMENT.md` for:
- Railway.app
- Render.com
- Heroku

## 📝 Need Database Access?

If you need the historic charts feature, add these environment variables:

**Streamlit Cloud**: Advanced settings → Secrets
```toml
DB_HOST = "your-host"
DB_NAME = "your-db"
DB_USER = "your-user"
DB_PASSWORD = "your-password"
```

**Local**: Create `.env` file
```bash
cp .env.example .env
# Edit .env with your values
```

## ❓ Problems?

### "Module not found"
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
streamlit run KatScan.py --server.port 8502
```

### Need help?
- Check `README.md` for detailed setup
- Check `DEPLOYMENT.md` for platform-specific guides
- Check `CHANGES.md` to see what was fixed

## 🎯 What You Get

✅ MMCC/NMBC NFT tracker  
✅ Rewards checker  
✅ Treasury monitoring  
✅ Marketplace listings  
✅ Sales activity tracker  

## 🚨 Remember

**DO NOT deploy to Vercel!** Streamlit needs WebSockets and long-running processes, which Vercel's serverless functions don't support.

Use Streamlit Community Cloud instead! 🎈

