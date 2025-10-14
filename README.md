# BuildLog - AI-Powered Hackathon & Project Documentation Platform

![BuildLog Banner](https://img.shields.io/badge/Built%20with-Appwrite-F02E65?style=for-the-badge&logo=Appwrite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Test Coverage](https://img.shields.io/badge/Coverage-98%25-brightgreen?style=for-the-badge)

**Document your build journey with beautiful timelines, rich logging, AI-powered content generation, and automatic markdown exports.**

Built for the **Appwrite Hacktoberfest 2025 Hackathon**, BuildLog helps developers track their hackathon projects and side projects with rich documentation, beautiful visualizations, seamless exports, and AI-powered assistance for GitHub submissions.

🏆 **Features 98% test coverage** - Production-ready code with 114 passing tests!

---

## ✨ Features

### Core Features
- 📝 **Daily Build Logs**: Track your progress with rich text logs, code snippets, and notes
- 🎨 **Beautiful Timeline Views**: Visualize your project journey with stunning, color-coded timelines
- 📊 **Project Dashboard**: Manage multiple projects in one centralized location
- 📄 **Markdown Export**: One-click export to markdown for GitHub submissions and documentation
- 🌐 **Public Portfolios**: Generate beautiful, shareable portfolio pages for each project
- 📁 **File Uploads**: Store images, videos, and files securely with Appwrite Storage

### AI-Powered Features ✨
- 🤖 **AI Project Descriptions**: Automatically generate compelling project descriptions based on your project name and tech stack
- 📝 **AI Build Log Generation**: Get AI-powered content suggestions for your build logs based on log type and context
- 🎯 **Smart Content**: Leverage OpenAI's GPT-3.5 to create professional, context-aware documentation
- ⚡ **One-Click Generation**: Beautiful purple "Generate with AI" buttons integrated directly in forms
- 🔒 **Optional Feature**: AI features are completely optional - use them when you need them, skip when you don't

### Appwrite Integration
BuildLog leverages **Appwrite Cloud Services**:
- **Appwrite Databases**: Store projects and build logs with structured data
- **Appwrite Storage**: Secure file uploads and media management
- **Direct HTTP API**: Production-ready integration using HTTP requests

---

## 🚀 Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Frontend**: Jinja2 Templates, Tailwind CSS
- **Database**: Appwrite Cloud Databases (NYC Region)
- **Storage**: Appwrite Cloud Storage
- **AI**: OpenAI GPT-3.5 for content generation
- **Testing**: Pytest with 98% coverage (114 tests)
- **Deployment**: Ready for Appwrite Cloud Sites

---

## 📦 Getting Started

### Prerequisites

- Python 3.13 or higher
- Appwrite Cloud account (free at [cloud.appwrite.io](https://cloud.appwrite.io))
- pip (Python package manager)

### Quick Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SaiShashank12/buildlog.git
   cd buildlog
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file with your Appwrite credentials:
   ```env
   # Appwrite Configuration
   APPWRITE_ENDPOINT=https://nyc.cloud.appwrite.io/v1
   APPWRITE_PROJECT_ID=your_project_id
   APPWRITE_API_KEY=your_api_key
   APPWRITE_DATABASE_ID=buildlog_db
   APPWRITE_PROJECTS_COLLECTION_ID=projects
   APPWRITE_BUILD_LOGS_COLLECTION_ID=build_logs
   APPWRITE_STORAGE_BUCKET_ID=buildlog_files

   # Application Settings
   SECRET_KEY=your_secret_key_here
   DEBUG=True

   # AI Configuration (Optional - for AI-powered features)
   OPENAI_API_KEY=your_openai_api_key_here
   AI_ENABLED=True
   ```

   **Note**: AI features are optional. If you don't want to use AI features, simply set `AI_ENABLED=False` or leave out the OpenAI API key.

5. **Run the application**
   ```bash
   python3 main.py
   ```

6. **Open your browser**
   ```
   http://localhost:8000
   ```

---

## 🔧 Appwrite Setup

### 1. Create Appwrite Project

1. Go to [cloud.appwrite.io](https://cloud.appwrite.io)
2. Create a new project named "BuildLog"
3. Copy your Project ID and API Key
4. Note your region (e.g., NYC)

### 2. Create Database

Create a database named `buildlog_db` with the following collections:

#### Collection: `projects`
Attributes:
- `name` (String, required, max: 200)
- `description` (String, optional, max: 5000)
- `tech_stack` (String[], optional)
- `repository_url` (URL, optional)
- `demo_url` (URL, optional)
- `tags` (String[], optional)
- `status` (String, required, default: "in_progress")
- `user_id` (String, required)
- `created_at` (DateTime, required)
- `updated_at` (DateTime, required)

Indexes:
- `user_id` (key)

#### Collection: `build_logs`
Attributes:
- `project_id` (String, required)
- `title` (String, required, max: 200)
- `content` (String, required, max: 10000)
- `log_type` (String, required)
- `code_snippets` (String[], optional)
- `images` (String[], optional)
- `links` (String[], optional)
- `tags` (String[], optional)
- `created_at` (DateTime, required)

Indexes:
- `project_id` (key)

### 3. Create Storage Bucket

Create a storage bucket named `buildlog_files`:
- Max file size: 50MB
- Allowed file extensions: `jpg, jpeg, png, gif, pdf, mp4, mov, zip`
- Permissions: Read access for authenticated users

---

## 🏗️ Project Structure

```
buildlog/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration and settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   ├── routes/
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── appwrite_service.py # Appwrite HTTP API integration
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── dashboard.html
│       ├── project_detail.html
│       ├── project_form.html
│       ├── log_form.html
│       ├── export.html
│       └── portfolio.html
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_appwrite_service.py
│   ├── test_config.py
│   └── test_models.py
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
├── .env.example              # Environment variables template
├── .gitignore
└── README.md
```

---

## 📊 Testing

BuildLog features **98% test coverage** with 114 comprehensive tests:

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run tests with coverage report
python3 -m pytest tests/ -v --cov=app --cov=main --cov-report=term-missing

# Run with coverage threshold
python3 -m pytest tests/ -v --cov=app --cov=main --cov-report=term-missing --cov-fail-under=90
```

### Test Coverage Details
- `app/config.py`: 100%
- `app/models/schemas.py`: 100%
- `app/services/appwrite_service.py`: 99%
- `app/services/ai_service.py`: 100%
- `main.py`: 96%
- **Total**: 98%

---

## 📖 Usage

### Creating a Project

1. Click "New Project" in the navigation
2. Fill in project details:
   - Project name (required)
   - Description
   - Tech stack (comma-separated)
   - Repository URL (optional)
   - Demo URL (optional)
   - Tags (comma-separated)
3. Click "Create Project"

### Adding Build Logs

1. Open a project from your dashboard
2. Click "Add Log Entry"
3. Choose log type:
   - **Update**: Regular progress update
   - **Milestone**: Major achievement
   - **Feature**: New feature added
   - **Bug Fix**: Bug resolution
   - **Note**: General note
4. Write your content (supports markdown)
5. Add tags for organization
6. Click "Add Log Entry"

### Exporting to Markdown

1. Open a project
2. Click "Export" button
3. Copy the markdown or download as .md file
4. Use for GitHub submissions, documentation, or sharing

### Generating Portfolio

1. Each project has a public portfolio page
2. Access via `/portfolio/{project_id}`
3. Share this beautiful page with recruiters, judges, or teammates

### Using AI Features

**Generating Project Descriptions:**
1. When creating or editing a project, fill in the project name and tech stack
2. Click the purple "Generate with AI" button below the description field
3. AI will create a compelling, professional description based on your inputs
4. Review and edit the generated description as needed

**Generating Build Log Content:**
1. When creating a new build log, select the log type (update, milestone, feature, etc.)
2. Optionally add a title to provide context
3. Click the purple "Generate with AI" button below the content field
4. AI will generate context-aware content appropriate for the log type
5. Edit and customize the generated content to match your actual progress

**Note**: AI features require an OpenAI API key. If AI is not enabled, the buttons will display an error message prompting you to configure your API key.

---

## 🌐 API Endpoints

### Projects
- `GET /` - Homepage
- `GET /dashboard` - User dashboard
- `GET /projects/new` - New project form
- `POST /projects/new` - Create project
- `GET /projects/{id}` - View project
- `GET /projects/{id}/edit` - Edit project form
- `POST /projects/{id}/edit` - Update project
- `POST /projects/{id}/delete` - Delete project

### Build Logs
- `GET /projects/{id}/logs/new` - New log form
- `POST /projects/{id}/logs/new` - Create log
- `GET /projects/{id}/logs/{log_id}/edit` - Edit log form
- `POST /projects/{id}/logs/{log_id}/edit` - Update log
- `POST /projects/{id}/logs/{log_id}/delete` - Delete log

### Export & Portfolio
- `GET /projects/{id}/export` - Export to markdown
- `GET /portfolio/{id}` - Public portfolio page

### AI-Powered Endpoints
- `GET /ai/status` - Check if AI features are enabled
- `POST /ai/generate-description` - Generate project description with AI
- `POST /ai/generate-log-content` - Generate build log content with AI

### Utilities
- `POST /upload` - Upload file
- `GET /health` - Health check

---

## 🎯 Why BuildLog?

### 1. **AI-Powered Innovation**
- First-class AI integration for content generation
- OpenAI GPT-3.5 powered suggestions
- Smart, context-aware documentation assistance
- Optional features that enhance without overwhelming

### 2. **Comprehensive Testing**
- 98% test coverage
- 114 passing tests
- Production-ready code quality

### 3. **Appwrite Integration**
- Direct HTTP API implementation
- Robust error handling
- Secure file storage

### 4. **Solves a Real Problem**
Every hackathon participant struggles with documentation. BuildLog makes it effortless to:
- Track progress daily
- Generate compelling submission documents with AI assistance
- Create portfolio pieces
- Export to any format

### 5. **Meta Appeal**
Built FOR hackathons, IN a hackathon. Perfect for other developers!

### 6. **Beautiful Design**
Modern, responsive UI with Tailwind CSS that's both functional and stunning.

### 7. **Technical Excellence**
- Clean, well-documented code
- Proper error handling
- Modular architecture
- Best practices throughout

---

## 🚧 Future Enhancements

- ✅ **AI-Powered Features**: Auto-generate project descriptions and build logs (IMPLEMENTED)
- **Enhanced AI Features**: AI-powered markdown export summaries and suggestions
- **Real-time Collaboration**: Multiple team members on one project
- **Authentication**: Full user authentication with Appwrite Auth
- **Analytics**: Track progress metrics and time spent
- **Integrations**: GitHub, GitLab, Jira sync
- **Mobile App**: iOS and Android apps
- **Team Features**: Collaboration tools for hackathon teams

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Appwrite](https://appwrite.io) - The open-source backend server
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- Created for the **Appwrite Hacktoberfest 2025 Hackathon**

---

## 👤 Author

**Sai Shashank Mudliar**

- GitHub: [@SaiShashank12](https://github.com/SaiShashank12)
- Email: shashanksai.ss@gmail.com

---

## 📊 Project Stats

- **Lines of Code**: 2,500+ (25 files)
- **Test Coverage**: 98%
- **Tests**: 114 passing
- **Python Version**: 3.13+
- **Framework**: FastAPI
- **AI Integration**: OpenAI GPT-3.5
- **Database**: Appwrite Cloud

---

**Built with ❤️ using Appwrite** - AI-Powered Project Documentation Platform for Hacktoberfest 2025
