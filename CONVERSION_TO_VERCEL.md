# Converting Streamlit App to Vercel (Next.js/React)

## 🚨 Summary: This is a MAJOR Rewrite

Converting this Streamlit app to work on Vercel would require **rebuilding the entire application from scratch** in a modern JavaScript framework. This is essentially a complete rewrite, not a simple port.

**Estimated Effort**: 80-120+ hours for a full-stack developer  
**Complexity**: High  
**Recommended**: Only if you have specific reasons to avoid Streamlit Cloud

---

## 📋 What Needs to Be Rebuilt

### 1. **Frontend - Complete Rebuild Required**

#### Current Streamlit Components → New Implementation

| Streamlit Component | Vercel/Next.js Replacement | Effort |
|-------------------|---------------------------|--------|
| `st.sidebar` with filters | React sidebar component + state management | Medium |
| `st.columns()` layouts | CSS Grid/Flexbox layouts | Easy |
| `st.selectbox()` (9 filters) | HTML `<select>` or React Select library | Medium |
| `st.number_input()` | HTML `<input type="number">` | Easy |
| `st.text_area()` | HTML `<textarea>` | Easy |
| `st.radio()` navigation | React Router or Next.js routing | Medium |
| `st.table()` | HTML table or React Table library | Easy |
| `AgGrid` tables | AG Grid React or TanStack Table | Hard |
| `st_echarts` charts | ECharts React wrapper or Chart.js | Medium |
| `st.write()` markdown | React Markdown library | Easy |
| Auto-refresh (2 min) | `setInterval()` + React hooks | Easy |

**Total Frontend Components to Rebuild**: ~25-30 interactive components

---

### 2. **Backend - API Routes Required**

All data fetching currently happens in Python on the server. You'd need to create:

#### Required API Endpoints

```
/api/mmcc/listings          - Fetch & aggregate listings from 3 marketplaces
/api/mmcc/activity          - Fetch recent sales from Magic Eden
/api/mmcc/rewards           - Calculate rewards pool data
/api/mmcc/historic-charts   - Query PostgreSQL for historic data
/api/treasury/balances      - Fetch all wallet balances
/api/rewards/check          - Check rewards for user wallet(s)
/api/coingecko/sol-price    - Fetch SOL price
```

**Complexity**: Each endpoint needs to:
- Call multiple external APIs
- Aggregate and transform data
- Handle rate limiting
- Handle errors gracefully
- Return JSON responses

---

### 3. **Technology Stack Required**

#### Frontend
```json
{
  "framework": "Next.js 14+ (App Router)",
  "language": "TypeScript",
  "styling": "Tailwind CSS or Styled Components",
  "components": [
    "shadcn/ui or Material-UI",
    "@tanstack/react-table",
    "echarts-for-react",
    "react-hook-form",
    "zustand or Redux (state management)"
  ]
}
```

#### Backend (Vercel Serverless Functions)
```json
{
  "runtime": "Node.js 18+",
  "or": "Python (with limitations)",
  "libraries": [
    "axios or fetch",
    "pg (PostgreSQL client)",
    "node-cache (caching)"
  ]
}
```

---

## 📁 New Project Structure

```
kat-scanner-nextjs/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home/navigation page
│   ├── listings/
│   │   └── page.tsx            # MMCC listings page
│   ├── activity/
│   │   └── page.tsx            # MMCC activity page
│   ├── rewards/
│   │   └── page.tsx            # Rewards checker page
│   └── treasury/
│       └── page.tsx            # Treasury tracker page
│
├── components/                   # React components
│   ├── ui/                      # Base UI components
│   ├── Sidebar.tsx              # Filter sidebar
│   ├── ListingsTable.tsx        # NFT listings table
│   ├── OrderbookChart.tsx       # ECharts orderbook
│   ├── PriceVsRankChart.tsx     # Scatter chart
│   ├── RewardsTable.tsx         # Rewards display
│   └── Navigation.tsx           # Page navigation
│
├── lib/                         # Utility functions
│   ├── api.ts                   # API client functions
│   ├── utils.ts                 # Helper functions
│   └── types.ts                 # TypeScript types
│
├── api/                         # Vercel serverless functions
│   ├── mmcc/
│   │   ├── listings.ts          # Aggregate marketplace data
│   │   ├── activity.ts          # Recent sales
│   │   └── rewards.ts           # Rewards calculation
│   ├── treasury/
│   │   └── balances.ts          # Wallet balances
│   └── rewards/
│       └── check.ts             # User rewards lookup
│
├── public/                      # Static assets
│   ├── favicon.png
│   └── KatLogo.png
│
├── styles/                      # CSS/styling
│   └── globals.css
│
└── package.json                 # Dependencies
```

---

## 🔨 Step-by-Step Conversion Process

### Phase 1: Setup (4-8 hours)
```bash
# Create Next.js project
npx create-next-app@latest kat-scanner-nextjs --typescript --tailwind --app

# Install dependencies
npm install @tanstack/react-table echarts-for-react
npm install axios date-fns pg
npm install @types/pg
```

### Phase 2: API Routes (20-30 hours)

#### Example: `/api/mmcc/listings.ts`
```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // 1. Fetch from Solanart
    const saResponse = await fetch('https://api.solanart.io/get_nft?...');
    const saData = await saResponse.json();
    
    // 2. Fetch from Magic Eden
    const meResponse = await fetch('https://api-mainnet.magiceden.dev/...');
    const meData = await meResponse.json();
    
    // 3. Fetch from Digitaleyes
    const deResponse = await fetch('https://us-central1-digitaleyes-prod...');
    const deData = await deResponse.json();
    
    // 4. Aggregate and transform data
    const listings = aggregateListings(saData, meData, deData);
    
    // 5. Return JSON
    return NextResponse.json({ listings, success: true });
    
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch listings', success: false },
      { status: 500 }
    );
  }
}

function aggregateListings(sa: any, me: any, de: any) {
  // Complex data transformation logic here
  // (Convert from current Python logic to TypeScript)
}
```

**Repeat for each API endpoint** - Each one requires similar complexity.

### Phase 3: Frontend Components (30-40 hours)

#### Example: Listings Table Component
```typescript
// components/ListingsTable.tsx
'use client';

import { useTable, useSortBy, useFilters } from '@tanstack/react-table';
import { useState, useEffect } from 'react';

export function ListingsTable({ filters }: { filters: ListingFilters }) {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchListings() {
      setLoading(true);
      const response = await fetch('/api/mmcc/listings');
      const data = await response.json();
      setListings(data.listings);
      setLoading(false);
    }
    fetchListings();
    
    // Auto-refresh every 2 minutes
    const interval = setInterval(fetchListings, 2 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  // Table configuration
  const columns = [
    { Header: 'Price', accessor: 'price' },
    { Header: 'Rank', accessor: 'rank' },
    { Header: 'ID', accessor: 'id' },
    { Header: 'Market', accessor: 'market' },
    // ... more columns
  ];

  const table = useTable(
    { columns, data: listings },
    useFilters,
    useSortBy
  );

  if (loading) return <div>Loading...</div>;

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        {/* Table implementation */}
      </table>
    </div>
  );
}
```

#### Example: Filter Sidebar Component
```typescript
// components/Sidebar.tsx
'use client';

import { useState } from 'react';

interface SidebarProps {
  onFiltersChange: (filters: Filters) => void;
}

export function Sidebar({ onFiltersChange }: SidebarProps) {
  const [rankType, setRankType] = useState('Howrare.is');
  const [maxRank, setMaxRank] = useState(9999);
  const [market, setMarket] = useState('All');
  const [background, setBackground] = useState('All');
  const [fur, setFur] = useState('All');
  // ... 6 more filter states

  useEffect(() => {
    onFiltersChange({
      rankType, maxRank, market, background, fur,
      // ... all filters
    });
  }, [rankType, maxRank, market, background, fur]);

  return (
    <aside className="w-64 bg-gray-100 p-4">
      <h2 className="text-xl font-bold mb-4">Attribute Filters</h2>
      
      <div className="mb-4">
        <label>Ranking Method</label>
        <select
          value={rankType}
          onChange={(e) => setRankType(e.target.value)}
          className="w-full p-2 border rounded"
        >
          <option>Howrare.is</option>
          <option>MoonRank</option>
        </select>
      </div>

      <div className="mb-4">
        <label>Max Rank</label>
        <input
          type="number"
          value={maxRank}
          onChange={(e) => setMaxRank(Number(e.target.value))}
          className="w-full p-2 border rounded"
          min={1}
          max={9999}
        />
      </div>

      {/* Repeat for all 8+ filters */}
    </aside>
  );
}
```

#### Example: ECharts Integration
```typescript
// components/OrderbookChart.tsx
'use client';

import ReactECharts from 'echarts-for-react';

export function OrderbookChart({ data }: { data: any[] }) {
  const option = {
    title: {
      left: 'center',
      text: 'Meerkat Order Book'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    // ... rest of ECharts configuration
    // (Port from existing st_echarts code)
  };

  return <ReactECharts option={option} style={{ height: '500px' }} />;
}
```

### Phase 4: Pages (15-20 hours)

#### Example: Listings Page
```typescript
// app/listings/page.tsx
'use client';

import { useState } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { ListingsTable } from '@/components/ListingsTable';
import { OrderbookChart } from '@/components/OrderbookChart';

export default function ListingsPage() {
  const [filters, setFilters] = useState({});

  return (
    <div className="flex min-h-screen">
      <Sidebar onFiltersChange={setFilters} />
      
      <main className="flex-1 p-8">
        <h1 className="text-3xl font-bold mb-6">
          MMCC Market Listings
        </h1>
        
        <div className="mb-8">
          {/* Floor prices display */}
        </div>
        
        <ListingsTable filters={filters} />
        
        <div className="mt-8">
          <OrderbookChart data={[]} />
        </div>
      </main>
    </div>
  );
}
```

### Phase 5: State Management & Optimization (10-15 hours)
- Implement global state management (Zustand/Redux)
- Add request caching
- Optimize re-renders
- Add loading states
- Error handling
- Rate limiting

### Phase 6: Styling & Polish (10-15 hours)
- Match current design
- Responsive design
- Dark mode (optional)
- Animations/transitions
- Accessibility

### Phase 7: Testing & Deployment (5-10 hours)
- Test all features
- Environment variables setup
- Deploy to Vercel
- Monitor performance

---

## ⚠️ Major Challenges

### 1. **Data Aggregation Complexity**
The current app fetches from 3 marketplaces simultaneously and aggregates data. In Vercel:
- Serverless functions have 10-60 second timeouts
- Multiple API calls might exceed timeout
- Need to implement caching strategy

### 2. **PostgreSQL Connection Pooling**
Vercel serverless functions can't maintain persistent DB connections:
- Need to use connection pooling service (e.g., Supabase Pooler, PgBouncer)
- Or switch to serverless-friendly database (e.g., PlanetScale, Neon)

### 3. **CSV Data Files**
Current app loads CSV files (`MMCC_ranks.csv`):
- Need to convert to API endpoints or database tables
- Or load from static storage (Vercel Blob)

### 4. **Auto-refresh Strategy**
Streamlit auto-refreshes server-side. In Next.js:
- Client-side polling with `setInterval()`
- Or implement WebSocket connections
- Or use SWR library for smart refetching

### 5. **State Persistence**
Streamlit maintains session state. In Next.js:
- Use URL query parameters for filters
- Or local storage
- Or global state management

---

## 💰 Cost Comparison

### Streamlit Community Cloud
- **Cost**: FREE (with public repo)
- **Limitations**: Public repository required
- **Effort**: 0 hours (already working)

### Vercel Conversion
- **Development Cost**: 80-120 hours × your hourly rate
- **Vercel Hosting**: FREE hobby tier or $20/mo Pro
- **Learning Curve**: High (if not familiar with Next.js/React)

---

## 📊 Feature Parity Checklist

After conversion, you'd need to ensure:

- [ ] Multi-page navigation (4 pages)
- [ ] MMCC Listings with 9 filter controls
- [ ] Interactive data tables with sorting/pagination
- [ ] Custom link renderers in tables
- [ ] ECharts orderbook visualization
- [ ] ECharts price vs rank scatter plot
- [ ] Rewards checker with wallet input
- [ ] Real-time balance fetching
- [ ] Auto-refresh every 2 minutes
- [ ] Treasury/royalty tracking
- [ ] Recent sales activity display
- [ ] PostgreSQL historic data charts
- [ ] Responsive layouts
- [ ] Error handling for API failures

---

## 🎯 Recommendation

### If you need Vercel specifically:
**Proceed with conversion** - Budget 80-120+ hours

### If you just want it deployed:
**Use Streamlit Cloud** - Already working, 0 additional hours

### Alternative Hybrid Approach:
Keep Streamlit for the main app, build a lightweight Next.js landing page on Vercel that:
- Embeds the Streamlit app in an iframe
- Adds custom branding/landing content
- Gets Vercel domain benefits

**Effort**: 4-8 hours instead of 80-120 hours

---

## 📝 Example Package.json for Next.js Version

```json
{
  "name": "kat-scanner-nextjs",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-table": "^8.10.0",
    "echarts": "^5.4.3",
    "echarts-for-react": "^3.0.2",
    "axios": "^1.6.0",
    "date-fns": "^2.30.0",
    "pg": "^8.11.0",
    "swr": "^2.2.0",
    "zustand": "^4.4.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/pg": "^8.10.0",
    "typescript": "^5.2.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

---

## 🚀 Final Verdict

**Converting to Vercel is technically feasible but extremely time-consuming.**

**Before starting, ask yourself:**
1. Do I have 80-120+ hours to invest in this?
2. Am I comfortable with Next.js/React/TypeScript?
3. Do I have a specific reason to avoid Streamlit Cloud?
4. Is the conversion worth the opportunity cost?

**If the answer to any of these is "No", stick with Streamlit Cloud.** ✅

The app is already fixed and working. Streamlit Cloud is purpose-built for this use case, free, and requires zero additional work.

