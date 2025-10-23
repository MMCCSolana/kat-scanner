# Deployment Guide

## ⚠️ Important: Streamlit + Vercel Limitations

**Streamlit is NOT recommended for Vercel deployment** due to:
- WebSocket requirements (Streamlit needs persistent connections)
- Serverless function timeouts (10-60 seconds max)
- Streamlit's architecture requiring long-running processes

## ✅ Recommended Deployment Options

### Option 1: Streamlit Community Cloud (BEST)

**Pros**: Free, designed for Streamlit, easy setup, automatic SSL
**Cons**: Public repository required (or paid plan)

**Steps**:
1. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Click "New app" and connect your GitHub repository

4. Configure your app:
   - Repository: `your-username/kat-scanner`
   - Branch: `main`
   - Main file: `KatScan.py`

5. Add secrets (if needed):
   Click "Advanced settings" → "Secrets" and add:
   ```toml
   DB_HOST = "your-database-host"
   DB_NAME = "your-database-name"
   DB_USER = "your-database-user"
   DB_PASSWORD = "your-database-password"
   ```

6. Click "Deploy"!

Your app will be live at: `https://your-username-kat-scanner.streamlit.app`

### Option 2: Heroku

**Pros**: Supports long-running processes, reliable
**Cons**: Requires payment (no free tier as of 2022)

**Steps**:
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create a new Heroku app:
   ```bash
   heroku create your-kat-scanner
   ```

4. Set environment variables:
   ```bash
   heroku config:set DB_HOST=your-database-host
   heroku config:set DB_NAME=your-database-name
   heroku config:set DB_USER=your-database-user
   heroku config:set DB_PASSWORD=your-database-password
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

Your app will be live at: `https://your-kat-scanner.herokuapp.com`

### Option 3: Railway.app

**Pros**: Free tier available, easy deployment, great for Streamlit
**Cons**: Limited free hours

**Steps**:
1. Go to [railway.app](https://railway.app)

2. Click "New Project" → "Deploy from GitHub repo"

3. Connect your GitHub repository

4. Railway will auto-detect the Streamlit app

5. Add environment variables in the dashboard:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`

6. Railway will automatically deploy!

### Option 4: Render.com

**Pros**: Free tier, designed for web apps, good documentation
**Cons**: Free tier has spin-down after inactivity

**Steps**:
1. Go to [render.com](https://render.com)

2. Click "New +" → "Web Service"

3. Connect your GitHub repository

4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run KatScan.py --server.port=$PORT --server.address=0.0.0.0`

5. Add environment variables in the dashboard

6. Click "Create Web Service"

## 🔧 Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your credentials

# Run the app
streamlit run KatScan.py
```

## 📝 Environment Variables

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | `ec2-xxx.compute-1.amazonaws.com` |
| `DB_NAME` | Database name | `d8moers639v8ep` |
| `DB_USER` | Database user | `username` |
| `DB_PASSWORD` | Database password | `your-secure-password` |

## 🚀 Performance Tips

1. **API Rate Limits**: The app calls multiple external APIs. Consider implementing caching with `@st.cache_data`

2. **Auto-refresh**: The app auto-refreshes every 2 minutes. Adjust in `MMCC.py`:
   ```python
   st_autorefresh(interval=2 * 60 * 1000, key="dataframerefresh")
   ```

3. **Database Connection**: Consider using connection pooling for better performance

## 🔒 Security Notes

- Never commit `.env` file to git
- Use environment variables for all sensitive data
- Consider rotating database credentials regularly
- Use read-only database users when possible

## 📊 Monitoring

After deployment, monitor:
- API response times
- Database connection pool
- Memory usage (especially with large dataframes)
- External API rate limits

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Database connection issues
- Verify environment variables are set correctly
- Check database allows connections from your deployment platform
- Verify database credentials are valid

### App is slow
- Check API response times
- Consider adding `@st.cache_data` to expensive operations
- Reduce auto-refresh frequency

### Streamlit WebSocket errors
- Ensure your platform supports WebSockets
- Check firewall/security group settings
- Verify CORS settings if needed

