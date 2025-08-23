# QuotaPath - Sales Commission Tracking Platform

An approximation of the QuotaPath sales commission and compensation tracking platform, built with Python/Django backend, React TypeScript frontend, and Pandas for data processing.

## 🚀 Features

### Dashboard & Analytics
- **Interactive Dashboard** with real-time sales metrics and commission data
- **Sales Pipeline Analysis** with stage-by-stage breakdown
- **Commission Trends** and performance analytics
- **Quota Attainment Tracking** with visual progress indicators
- **Revenue Forecasting** and projections

### Sales Management
- **Deal Management** with full CRUD operations
- **Sales Activities** tracking and logging
- **Pipeline Stage Management** with probability tracking
- **Quota Setting** and performance monitoring

### Commission Management
- **Flexible Compensation Plans** (flat rate, percentage, tiered, quota-based)
- **Automated Commission Calculations** using Pandas for performance
- **Bulk Processing** of commission calculations
- **Commission Analytics** with historical trends
- **Payout Management** and tracking

### User Management
- **Role-based Access Control** (Admin, Manager, Sales Rep)
- **Team Management** with hierarchical structure
- **User Authentication** and authorization

## 🛠 Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Pandas** - Data processing and analytics
- **PostgreSQL** - Primary database
- **Redis** - Caching and task queue
- **Celery** - Background task processing

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Material-UI v5** - Component library
- **Recharts** - Data visualization
- **Axios** - HTTP client

### DevOps
- **Docker & Docker Compose** - Containerization
- **Gunicorn** - WSGI server

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quotapath
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Django Admin: http://localhost:8000/admin

4. **Create a superuser** (in a new terminal)
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

### Local Development Setup

#### Backend Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run development server**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

## 📊 Data Models

### Core Models

- **User** - Extended Django user with sales roles
- **Deal** - Sales opportunities with stages and amounts
- **Quota** - Sales targets by period
- **CompensationPlan** - Commission calculation rules
- **Commission** - Individual commission records
- **SalesActivity** - Activity tracking

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/me/` - Current user info

### Sales
- `GET /api/sales/deals/` - List deals
- `POST /api/sales/deals/` - Create deal
- `GET /api/sales/dashboard-stats/` - Dashboard metrics
- `GET /api/sales/pipeline-analysis/` - Pipeline data

### Commissions
- `GET /api/commissions/commissions/` - List commissions
- `POST /api/commissions/calculate/` - Calculate commissions
- `GET /api/commissions/analytics/` - Commission analytics
- `GET /api/commissions/trends/` - Trend analysis

## 🧮 Commission Calculation

The platform supports multiple commission types:

1. **Flat Rate** - Fixed amount per deal
2. **Percentage** - Percentage of deal value
3. **Tiered** - Different rates for different deal sizes
4. **Quota-based** - Rate changes based on quota attainment

### Pandas Integration

Commission calculations leverage Pandas for:
- **Bulk Processing** - Vectorized operations for performance
- **Analytics** - Statistical analysis and aggregations
- **Trend Analysis** - Time-series data processing
- **Forecasting** - Predictive analytics

## 🎨 UI Components

### Dashboard
- Metric cards with key performance indicators
- Interactive charts (Bar, Line, Pie)
- Real-time data updates
- Responsive design for mobile/desktop

### Data Grids
- Sortable and filterable tables
- Inline editing capabilities
- Bulk operations
- Export functionality

## 🔐 Security Features

- **Token-based Authentication**
- **Role-based Access Control**
- **CORS Configuration**
- **Input Validation**
- **SQL Injection Protection**

## 📈 Performance Features

- **Database Query Optimization**
- **Pandas Vectorization** for calculations
- **Caching** with Redis
- **Background Tasks** with Celery
- **Frontend Code Splitting**

## 🧪 Testing

```bash
# Backend tests
python manage.py test

# Frontend tests
cd frontend && npm test
```

## 📦 Deployment

The application is containerized and can be deployed using:

- **Docker Swarm**
- **Kubernetes**
- **Cloud platforms** (AWS, GCP, Azure)

### Environment Variables

- `DEBUG` - Django debug mode
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection string

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is a demonstration/approximation and is intended for educational purposes.

## 🙋‍♂️ Support

For questions or issues, please create an issue in the repository.

---

**Note**: This is an approximation of the QuotaPath platform created for demonstration purposes. The actual QuotaPath platform may have different features and implementation details.
