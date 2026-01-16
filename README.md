# 🌩️ Kuya Cloud

**Transform your raw data into actionable insights with automated cleaning and analysis.**

Kuya Cloud is a modern SaaS platform that lets you upload CSV/Excel files and instantly get:
- ✨ **Automated Data Cleaning** - Handle missing values, fix data types, remove duplicates
- 📊 **Exploratory Data Analysis** - Summary stats, correlations, distributions
- 📈 **Beautiful Visualizations** - Charts and graphs generated automatically
- 📄 **PDF Reports** - Professional downloadable reports
- 🔐 **User Authentication** - Google OAuth login
- 💳 **Subscription Plans** - Free & Pro tiers with Cashfree payments

## 🚀 Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + Custom Glassmorphism
- **Components**: Custom ShadCN-style components
- **Animations**: Framer Motion
- **Authentication**: NextAuth.js with Google OAuth
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI (Python)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **PDF Generation**: ReportLab
- **Database**: MongoDB (Motor async driver)

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway
- **Database**: MongoDB Atlas
- **Payments**: Cashfree

## 📂 Project Structure

```
kuya-cloud/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   │   ├── page.tsx     # Landing page
│   │   │   ├── upload/      # File upload page
│   │   │   ├── result/      # Analysis results
│   │   │   ├── dashboard/   # User dashboard
│   │   │   ├── pricing/     # Pricing page
│   │   │   └── api/         # API routes (NextAuth)
│   │   ├── components/      # React components
│   │   │   ├── ui/          # Base UI components
│   │   │   ├── layout/      # Header, Footer
│   │   │   ├── landing/     # Landing page sections
│   │   │   ├── upload/      # Upload components
│   │   │   └── result/      # Result components
│   │   ├── lib/             # Utilities
│   │   └── types/           # TypeScript types
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── main.py              # App entry point
│   ├── routers/             # API routes
│   │   ├── upload.py        # File upload & processing
│   │   ├── report.py        # PDF generation
│   │   ├── payment.py       # Cashfree webhooks
│   │   └── auth.py          # User authentication
│   ├── services/            # Business logic
│   │   ├── cleaner.py       # Data cleaning
│   │   ├── eda.py           # Exploratory analysis
│   │   └── graphs.py        # Chart generation
│   └── utils/               # Utilities
│       ├── db.py            # MongoDB connection
│       ├── pdf_generator.py # PDF reports
│       └── storage.py       # File storage
│
└── README.md
```

## 🛠️ Local Development Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB (local or Atlas)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp env.example .env.local

# Edit .env.local with your values:
# - NEXTAUTH_SECRET (generate with: openssl rand -base64 32)
# - GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET
# - MONGODB_URI
# - NEXT_PUBLIC_API_URL

# Start development server
npm run dev
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp env.example .env

# Edit .env with your values:
# - MONGODB_URI
# - CASHFREE_APP_ID & CASHFREE_SECRET_KEY

# Start development server
uvicorn main:app --reload --port 8000
```

## 🔑 Environment Variables

### Frontend (.env.local)

| Variable | Description |
|----------|-------------|
| `NEXTAUTH_URL` | Your app URL (http://localhost:3000) |
| `NEXTAUTH_SECRET` | Random secret for NextAuth |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `MONGODB_URI` | MongoDB connection string |
| `NEXT_PUBLIC_API_URL` | Backend API URL |
| `CASHFREE_APP_ID` | Cashfree App ID |
| `CASHFREE_SECRET_KEY` | Cashfree Secret Key |

### Backend (.env)

| Variable | Description |
|----------|-------------|
| `MONGODB_URI` | MongoDB connection string |
| `DATABASE_NAME` | Database name (default: kuya_cloud) |
| `CASHFREE_APP_ID` | Cashfree App ID |
| `CASHFREE_SECRET_KEY` | Cashfree Secret Key |
| `CASHFREE_API_URL` | API URL (sandbox or production) |
| `STORAGE_PATH` | File upload directory |

## 🌐 Deployment

### Frontend on Vercel

1. Push your code to GitHub
2. Import project to [Vercel](https://vercel.com)
3. Set root directory to `frontend`
4. Add environment variables in Vercel dashboard
5. Deploy!

### Backend on Railway

1. Push your code to GitHub
2. Create new project on [Railway](https://railway.app)
3. Connect GitHub repository
4. Set root directory to `backend`
5. Add environment variables
6. Railway will auto-detect Python and deploy

### MongoDB Atlas

1. Create account on [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster (free tier available)
3. Create database user with read/write access
4. Whitelist IP addresses (0.0.0.0/0 for all)
5. Get connection string and add to environment variables

### Cashfree Setup

1. Create account on [Cashfree](https://merchant.cashfree.com/merchants/signup)
2. Get your App ID and Secret Key from the merchant dashboard
3. Whitelist your domain: `https://your-domain.com`
4. Configure webhook URL: `https://your-backend.railway.app/payment/webhook`
5. For sandbox testing, use sandbox credentials and URL
6. For production, switch to production credentials

## 📱 Features

### Landing Page
- Animated gradient hero section
- Feature cards with hover effects
- Pricing comparison table
- Testimonials and stats

### Upload Page
- Drag-and-drop file upload
- Support for CSV, XLS, XLSX
- Real-time upload progress
- File validation

### Result Page
- Summary statistics cards
- Missing values chart
- Correlation heatmap
- Distribution charts
- AI-generated insights
- CSV & PDF download

### Dashboard
- User profile and plan status
- Recent reports list
- Upload history
- Upgrade to Pro button

### Authentication
- Google OAuth login
- Session management
- Protected routes

### Payments
- Free tier (5 uploads/month)
- Pro tier (unlimited + PDF + API)
- Cashfree payment integration
- Webhook-based plan updates

## 🎨 Design System

### Colors
- **Primary**: Purple gradient (#8b5cf6 → #6366f1)
- **Accent**: Amber gradient (for Pro features)
- **Success**: Green (#22c55e)
- **Warning**: Orange (#f59e0b)
- **Error**: Red (#ef4444)

### Typography
- **Display**: Outfit (headings)
- **Body**: Inter (text)

### Components
- Glassmorphism cards with backdrop blur
- Gradient buttons with hover glow
- Smooth Framer Motion animations
- Responsive mobile-first design

## 🔒 Security

- All API endpoints validate input
- File type and size validation
- CORS configured for allowed origins
- Cashfree webhook signature verification
- MongoDB connection with authentication
- Environment variables for secrets

## 📄 API Endpoints

### Upload
- `POST /upload` - Upload and process file

### Reports
- `GET /report/{id}` - Download PDF report
- `GET /report/{id}/data` - Get report data

### Auth
- `POST /auth/register` - Register/update user
- `POST /auth/login` - Validate login
- `GET /auth/user/{email}` - Get user profile

### Payments
- `POST /payment/create-order` - Create Cashfree order
- `POST /payment/webhook` - Cashfree webhook
- `GET /payment/verify/{id}` - Verify payment

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 License

MIT License - feel free to use for your own projects!

---

Built with ❤️ using Next.js & FastAPI
