# TravelAgent Pro - Deployment Guide

## Deployment Options

### 1. Local Development
```bash
docker-compose up -d
```

### 2. Cloud Deployment (AWS/GCP/Azure)

#### Option A: Docker Container

**AWS ECS:**
```bash
# Build and push
docker build -t travelagent-backend:latest ./backend
docker tag travelagent-backend:latest ${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/travelagent
docker push ${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/travelagent

# Deploy via ECS task definition
aws ecs update-service --cluster prod --service travelagent --force-new-deployment
```

**Google Cloud Run:**
```bash
gcloud run deploy travelagent \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Option B: Kubernetes

**Apply manifests:**
```bash
kubectl apply -f kubernetes/
```

**kubernetes/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: travelagent-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: travelagent
  template:
    metadata:
      labels:
        app: travelagent
    spec:
      containers:
      - name: backend
        image: travelagent-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: travelagent-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: travelagent-service
spec:
  selector:
    app: travelagent
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 3. Serverless (AWS Lambda + API Gateway)

**Using Mangum:**
```python
# backend/app/lambda_handler.py
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

**Deploy:**
```bash
sam deploy --guided
```

### 4. Platform-as-a-Service

**Heroku:**
```bash
heroku create travelagent-pro
git push heroku main
```

**Render:**
- Connect GitHub repo
- Select "Web Service"
- Auto-deploy on push

## Environment Configuration

### Production .env
```bash
DEBUG=false
SECRET_KEY=${STRONG_SECRET_KEY}
DATABASE_URL=${PROD_DB_URL}
REDIS_URL=${PROD_REDIS_URL}

# External APIs
OPENAI_API_KEY=${YOUR_KEY}
GOOGLE_MAPS_API_KEY=${YOUR_KEY}
AMADEUS_API_KEY=${YOUR_KEY}
```

### Database Migration
```bash
# Using Alembic
alembic upgrade head
```

### SSL/TLS
- Use Let's Encrypt for certificates
- Configure Nginx as reverse proxy
- Enable HTTPS redirect

## Monitoring Setup

### Prometheus + Grafana
```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    volumes:
      - grafana-data:/var/lib/grafana
```

### Application Logs
```python
# Configure structured logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
```

## Scaling Strategy

### Horizontal Scaling
- Auto-scaling groups (AWS/GCP)
- Kubernetes HPA (Horizontal Pod Autoscaler)
- Load balancer (ALB/NGINX)

### Caching Layer
- Redis for API responses
- CDN for static assets
- Database query caching

### Database Optimization
- Read replicas for scalability
- Connection pooling
- Query optimization

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] Authentication implemented
- [ ] Secrets rotation enabled
- [ ] Firewall rules configured
- [ ] DDoS protection enabled

## Backup Strategy

### Database Backups
```bash
# Daily automated backups
pg_dump -U postgres travelagent > backup_$(date +%Y%m%d).sql

# Upload to S3
aws s3 cp backup_$(date +%Y%m%d).sql s3://travelagent-backups/
```

### Disaster Recovery
- RPO (Recovery Point Objective): 1 hour
- RTO (Recovery Time Objective): 4 hours
- Multi-region deployment for HA

## Cost Optimization

### Estimated Monthly Costs (AWS)
- **Compute** (ECS Fargate): $50-150
- **Database** (RDS PostgreSQL): $20-100
- **Cache** (ElastiCache Redis): $15-50
- **Load Balancer** (ALB): $20
- **Storage** (S3): $5-20
- **CDN** (CloudFront): $10-30
- **Total**: $120-370/month

### Cost Reduction Tips
- Use spot instances for non-critical workloads
- Enable auto-scaling to match demand
- Use CDN for static assets
- Optimize database queries
- Implement caching aggressively

## Performance Targets

- API Response Time: < 200ms (p95)
- Uptime: 99.9%
- Agent Planning: < 5 seconds
- Concurrent Users: 1000+

## Deployment Checklist

- [ ] Code tested locally
- [ ] Environment variables configured
- [ ] Database migrated
- [ ] Dependencies installed
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Alerts configured
- [ ] Backup system tested
- [ ] Load testing completed
- [ ] Documentation updated

---

**Support**: devops@travelagent.pro
