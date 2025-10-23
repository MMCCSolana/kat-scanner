# Kat Scanner - MMCC & NMBC Tracker

A Streamlit-based dashboard for tracking Meerkat Millionaires Country Club (MMCC) and Naked Meerkat Beach Club (NMBC) NFT sales, listings, and royalties on the Solana blockchain.

## Features

- **Rewards Checker**: Check your weekly rewards from MMCC holdings
- **ClubDAO Treasury**: View current treasury balances and royalty pools
- **MMCC Listings**: Browse current marketplace listings with advanced filtering
- **MMCC Activity**: Track recent sales and market activity

## Setup

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd kat-scanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the application:
```bash
streamlit run KatScan.py
```

The application will be available at `http://localhost:8501`

## Deployment

### Vercel Deployment

⚠️ **Note**: Vercel's serverless functions have limitations that may not be compatible with long-running Streamlit apps. Consider using **Streamlit Community Cloud** instead.

### Recommended: Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add environment variables in the app settings:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
5. Deploy!

### Alternative: Heroku

The app includes a `Procfile` and `setup.sh` for Heroku deployment:

```bash
heroku create your-app-name
heroku config:set DB_HOST=your-host DB_NAME=your-db DB_USER=your-user DB_PASSWORD=your-pass
git push heroku main
```

## Configuration

### Environment Variables

- `DB_HOST`: PostgreSQL database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password

## Data Sources

- Solanart API
- Magic Eden API
- Digitaleyes API
- Solscan API
- CoinGecko API

## Pages

### Rewards Checker
Enter your Solana wallet address to see:
- Weekly holder rewards
- Minter rewards
- Total SOL and USD value received

### ClubDAO Treasury
Real-time view of:
- MMCC & NMBC royalty balances
- DAO treasury assets
- Reward pool calculations

### MMCC Listings
Filter and browse marketplace listings by:
- Rank (Howrare.is or MoonRank)
- Marketplace (Solanart, Digitaleyes, Magic Eden)
- Attributes (Background, Fur, Eyes, etc.)

### MMCC Activity
Track recent sales including:
- Sale price and timestamp
- Buyer and seller information
- Token transfer history

## Development

### Project Structure
```
kat-scanner/
├── KatScan.py          # Main Streamlit app
├── MMCC.py             # MMCC listings page
├── MMCC_act.py         # MMCC activity page
├── check.py            # Rewards checker page
├── royalty_check.py    # Treasury/royalty tracking
├── check_data.py       # Historical rewards data
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku configuration
├── setup.sh           # Streamlit setup script
└── runtime.txt        # Python version
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

## Support

For issues or questions, contact @JG#4765 in the Meerkat Discord.

