# BrajPath - Clean Project Structure

## 📁 Project Files (Organized)

### 🚀 Quick Start
- **START_HERE.md** - Your first stop! Quick start guide
- **README.md** - Project overview and architecture

### 📖 Documentation
- **HOW_TO_USE.md** - Complete usage guide (local, Twilio, production)
- **BUG_REPORT.md** - Detailed bug analysis (for reference)
- **BUGS_FIXED.md** - All fixes documented
- **TODO.md** - Feature completion checklist
- **CONTRIBUTING.md** - Contribution guidelines
- **SECURITY.md** - Security policies
- **LICENSE** - MIT License

### 🧪 Test Scripts
- **quick_test.py** - 30-second bot test (3 messages)
- **demo_bot.py** - Full automated demo
- **test_bot.py** - Interactive chat mode

### ⚙️ Configuration
- **pyproject.toml** - Python project config & dependencies
- **requirements.txt** - Pip requirements (alternative)
- **uv.lock** - UV lock file
- **.env.example** - Environment variables template
- **.env** - Your local config (not in git)
- **.gitignore** - Git ignore patterns
- **pyrightconfig.json** - Type checking config

### 🐳 Deployment
- **Dockerfile** - Docker container config
- **.dockerignore** - Docker ignore patterns

### 📂 Directories

#### `/app` - Application Code
```
app/
├── api/              # FastAPI routes
│   └── webhook.py    # WhatsApp webhook endpoint
├── db/               # Database layer
│   ├── models.py     # SQLAlchemy models
│   ├── session.py    # Database session
│   └── seed.py       # Initial data seeding
├── services/         # Business logic
│   ├── state_machine.py      # Bot conversation logic
│   ├── temple_service.py     # Temple data service
│   ├── context_service.py    # Session context
│   └── timezone_utils.py     # Timezone utilities
├── data/             # Static data (translations, etc.)
├── config.py         # App configuration
└── main.py           # FastAPI app entry point
```

#### `/tests` - Test Suite
```
tests/
├── conftest.py           # Shared test fixtures
├── test_bot_flows.py     # Bot conversation tests
└── test_edge_cases.py    # Edge case & validation tests
```

#### `/scripts` - Utility Scripts
```
scripts/
├── init_db.py        # Initialize database tables
├── run_seed.py       # Seed initial data
├── check_db.py       # Check database contents
└── check_handlers.py # Verify state handlers
```

#### `/migrations` - Database Migrations
```
migrations/
└── (Alembic migration files)
```

#### `/docs` - Additional Documentation
```
docs/
├── meta-cloud-api-migration.md
└── twilio-production-deployment.md
```

### 🗄️ Database
- **brajpath.db** - SQLite database (not in git)

### 🚫 Ignored Files/Folders
- `.venv/` - Virtual environment
- `.uv-cache/` - UV cache
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python
- `*.db` - Database files
- `*.egg-info/` - Package info
- `.pytest_cache/` - Pytest cache
- `pytest-cache-files-*/` - Temp pytest files
- `server.*.log` - Server logs
- `.env` - Local environment

---

## 📊 File Count Summary

### Essential Files: 22
- Documentation: 8 files
- Test scripts: 3 files
- Configuration: 7 files
- Deployment: 2 files
- Database: 1 file (brajpath.db)
- Lock file: 1 file (uv.lock)

### Code Directories: 5
- `/app` - Main application
- `/tests` - Test suite
- `/scripts` - Utility scripts
- `/migrations` - DB migrations
- `/docs` - Documentation

---

## 🧹 Cleaned Up (Removed)

### Removed Files:
- ❌ BUGS_SUMMARY.txt (redundant)
- ❌ DEPLOYMENT_COMPLETE.md (redundant)
- ❌ FIXES_APPLIED.md (redundant)
- ❌ QUICK_START.txt (redundant)
- ❌ SERVER_RUNNING.md (redundant)
- ❌ braj_sahayak.db (duplicate)
- ❌ server.stderr.log (temporary)
- ❌ server.stdout.log (temporary)
- ❌ braj_sahayak.egg-info/ (duplicate)

### Why Removed:
- **Duplicate documentation** - Consolidated into START_HERE.md and HOW_TO_USE.md
- **Temporary files** - Log files and cache directories
- **Duplicate databases** - Only need brajpath.db
- **Build artifacts** - Duplicate egg-info directories

---

## 📝 Documentation Hierarchy

```
1. START_HERE.md          ← Start here!
   ├─ Quick test commands
   ├─ What is BrajPath
   └─ Links to other docs

2. HOW_TO_USE.md          ← Complete guide
   ├─ Local testing
   ├─ WhatsApp integration
   └─ Production deployment

3. README.md              ← Project overview
   ├─ Architecture
   ├─ Features
   └─ Technical details

4. BUG_REPORT.md          ← Bug analysis (reference)
5. BUGS_FIXED.md          ← Fix documentation
6. TODO.md                ← Feature checklist
```

---

## ✅ Clean Project Benefits

1. **Less Confusion** - Clear documentation hierarchy
2. **Faster Navigation** - Easy to find what you need
3. **Smaller Repo** - Removed redundant files
4. **Better Gitignore** - Prevents unnecessary files
5. **Professional** - Clean, organized structure

---

## 🎯 Where to Find Things

### Want to test the bot?
→ Run `python quick_test.py`

### Want to understand the project?
→ Read `START_HERE.md`

### Want to deploy to production?
→ See `HOW_TO_USE.md` section 3

### Want to understand the code?
→ Check `/app` directory structure above

### Want to run tests?
→ Run `pytest` in project root

### Want to add features?
→ Check `TODO.md` for planned features

---

**Project is now clean and organized! 🎉**
