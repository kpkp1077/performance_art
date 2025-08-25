# QuotaPath - Quick Start Guide

Get the QuotaPath sales commission platform running in minutes with our exact tech stack.

## 🛠 Our Tech Stack
- **Backend**: Python, Django, Pandas
- **Frontend**: React, TypeScript, @material-ui/core
- **Database**: PostgreSQL
- **Development**: Docker, Docker Compose
- **Production**: Google App Engine (Flexible Environment)

## 🚀 Quick Start (5 minutes)

### 1. Clone and Start
```bash
git clone <repository-url>
cd quotapath
docker-compose up --build
```

### 2. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

### 3. Create Admin User
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 4. Demo Login
- **Username**: demo
- **Password**: demo123

## 📊 Key Features Ready to Use

### Dashboard
- Real-time sales metrics
- Commission summaries
- Pipeline analysis
- Quota tracking

### Sales Management
- Deal tracking with stages
- Activity logging
- Quota management
- Performance analytics

### Commission Engine
- Multiple plan types (flat, percentage, tiered, quota-based)
- Automated calculations using Pandas
- Bulk processing capabilities
- Historical analytics

## 🔧 Development Workflow

### Backend Development
```bash
# Run Django development server
docker-compose exec backend python manage.py runserver

# Create migrations
docker-compose exec backend python manage.py makemigrations

# Run migrations
docker-compose exec backend python manage.py migrate

# Access Django shell
docker-compose exec backend python manage.py shell
```

### Frontend Development
```bash
# Frontend is already running in development mode
# Access at http://localhost:3000

# Install new packages
cd frontend && npm install <package-name>

# Build for production
cd frontend && npm run build
```

## 🚀 Production Deployment (Google App Engine)

### Prerequisites
- Google Cloud account
- Google Cloud SDK installed
- Project with billing enabled

### Deploy Steps
```bash
# 1. Setup Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Create Cloud SQL instance
gcloud sql instances create quotapath-db \
  --database-version=POSTGRES_14 \
  --region=us-central1

# 3. Create database
gcloud sql databases create quotapath --instance=quotapath-db

# 4. Setup Redis (Memorystore)
gcloud redis instances create quotapath-redis \
  --size=1 \
  --region=us-central1

# 5. Deploy
./deploy.sh
```

## 📈 Performance Features

### Pandas Integration
- **Vectorized Operations**: Bulk commission calculations
- **Data Analytics**: Statistical analysis of sales data
- **Time Series**: Trend analysis and forecasting
- **Memory Efficient**: Optimized for large datasets

### Caching Strategy
- **Redis Backend**: Session and query caching
- **Database Optimization**: Connection pooling
- **Static Files**: Optimized delivery

## 🎯 Next Steps

1. **Customize Commission Plans**: Create your specific compensation structures
2. **Import Data**: Use Django admin or API to import existing sales data
3. **Configure Integrations**: Connect to your CRM/ERP systems
4. **Set Up Monitoring**: Configure logging and monitoring in production
5. **Scale**: Adjust App Engine settings based on usage

## 📚 API Examples

### Get Dashboard Stats
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/sales/dashboard-stats/
```

### Calculate Commissions
```bash
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/commissions/calculate/
```

### Get Commission Analytics
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/commissions/analytics/
```

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

**Frontend Build Issues**
```bash
# Clear node modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Permission Errors**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

---

🎉 **You're ready to go!** The platform is now running with the complete tech stack and ready for customization.