# 🎮 GameAnnouncer

**Modern platform for game announcements and gaming event management**

## 🚀 Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/) (usually pre-installed on macOS/Linux)

### Launch in 1 command 🎯

```bash
# Clone repository
git clone https://github.com/AlexxMoran/GameAnnouncer.git
cd GameAnnouncer

# Start the entire project (API + Database + PgAdmin)
make project-up
```

**Done!** 🎉 Your project is running:
- 📱 **API**: http://localhost:3000
- 📊 **API Docs**: http://localhost:3000/docs  
- 🗄️ **PgAdmin**: http://localhost:5050

## 🛠️ Development Commands

### 🐳 Docker Commands

| Command | Description |
|---------|-------------|
| `make project-up` | 🚀 Start entire project (recommended) |
| `make backend-up` | 🔧 Start backend only (API + DB) |
| `make project-down` | 🛑 Stop all containers |
| `make project-logs` | 📊 Show backend logs |
| `make project-status` | 📋 Show all containers status |
| `make project-shell` | 🐚 Enter backend container |
| `make project-reset` | 🧹 Full reset (deletes all data!) |

### 🐍 Backend Commands (from backend/ folder)

```bash
cd backend

# Development
make dev          # 🔧 Start dev server (locally)
make test         # 🧪 Run tests
make format       # 🎨 Format code
make lint         # 🔍 Lint code

# Database
make migrate      # 📊 Apply migrations
make makemigrations MSG="description"  # 📝 Create new migration

# Dependencies
make install      # 📦 Install dependencies
```

## 📁 Project Structure

```
GameAnnouncer/
├── backend/           # 🐍 FastAPI backend
│   ├── api/          # REST API endpoints
│   ├── core/         # Configuration and settings
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── alembic/      # Database migrations
├── frontend/         # 🅰️ Angular frontend
├── docker-compose.yml # 🐳 Docker configuration
└── Makefile          # 🛠️ Development commands
```

## 🔧 Environment Setup

### Backend (.env file)
The `backend/.env` file is created automatically from `backend/.env.template` on first run.

**⚠️ Important**: Never commit your `.env` file with real credentials to version control!

Main settings:
```env
# Database
DB__SERVER=your_db_host
DB__PORT=your_db_port
DB__DATABASE=your_database_name
DB__USER=your_username
DB__PASSWORD=your_password

# CORS
CORS__BACKEND_CORS_ORIGINS=["http://localhost:3000"]
CORS__FRONTEND_HOST=http://localhost:4200
```

```

## 🔒 Security & Environment Variables

### Environment Setup
1. Copy the template: `cp backend/.env.template backend/.env`
2. Update `.env` with your actual credentials
3. **Never commit `.env` files to git** (already in .gitignore)
4. Use strong passwords for production
5. Generate new AUTH secrets for production

### Template Check
Make sure `backend/.env.template` contains only placeholder values, not real credentials!

### Production Deployment
- Change default passwords
- Generate secure random keys for AUTH_* variables
- Use environment-specific database credentials
- Enable HTTPS and proper CORS settings

## 🌐 API Documentation

After starting the project, API documentation is available at:
- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc
- **OpenAPI JSON**: http://localhost:3000/openapi.json

## 🗄️ Database

### PostgreSQL Connection
- **Host**: localhost:5433 (external connection)
- **Database**: your_database_name
- **User**: your_username
- **Password**: your_password

### PgAdmin (Web Interface)
1. Open http://localhost:5050
2. Login with credentials from your .env file
3. Add server:
   - Host: db
   - Port: 5432
   - Database: your_database_name
   - Username: your_username
   - Password: your_password

## 🐛 Troubleshooting

### Startup Issues
```bash
# Check containers status
make project-status

# View logs
make project-logs

# Full restart
make project-down
make project-up
```

### Database Reset
```bash
# Careful! Deletes ALL data
make project-reset
```

### Migration Issues
```bash
# Enter container and check
make project-shell
uv run alembic current
uv run alembic upgrade head
```

## 🧪 Development

### Local Backend Development
If you want to run backend locally (not in Docker):

```bash
cd backend

# Start only database in Docker
make backend-up  # or docker compose up -d db

# Configure .env for local development
# Update DB settings for external connection

# Start dev server
make dev
```

### Hot Reload
- Backend: Automatically reloads on file changes
- Frontend: Will be configured in the future

## 📝 Git Workflow

```bash
# Create new branch
git checkout -b feature/amazing-feature

# Commits
git add .
git commit -m "feat: add amazing feature"

# Push and PR
git push origin feature/amazing-feature
# Create Pull Request on GitHub
```

## 🎯 Main API Endpoints

- `GET /api/v1/games/` - List games
- `GET /api/v1/announcements/` - List announcements  
- `POST /api/v1/announcements/` - Create announcement
- `GET /docs` - API documentation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Need help?** 💬 Create an [Issue](https://github.com/AlexxMoran/GameAnnouncer/issues) or ask the team!
