# Appwrite Setup Guide for BuildLog

This guide will walk you through setting up all Appwrite services for BuildLog.

## Prerequisites

- Appwrite Cloud account at [cloud.appwrite.io](https://cloud.appwrite.io)
- Basic understanding of Appwrite concepts

## Step 1: Create Project

1. Log in to Appwrite Cloud
2. Click "Create Project"
3. Name: `BuildLog`
4. Copy your **Project ID** and **API Key**

## Step 2: Set Up Database

### Create Database

1. Go to "Databases" in the left sidebar
2. Click "Create database"
3. Name: `buildlog_db`
4. Database ID: `buildlog_db`

### Create Collections

#### Collection 1: projects

**Settings:**
- Collection ID: `projects`
- Name: Projects
- Permissions:
  - Create: Users
  - Read: Users
  - Update: Users
  - Delete: Users

**Attributes:**

```
name (String)
  - Key: name
  - Size: 200
  - Required: Yes
  - Array: No

description (String)
  - Key: description
  - Size: 5000
  - Required: No
  - Array: No

tech_stack (String)
  - Key: tech_stack
  - Size: 100
  - Required: No
  - Array: Yes

repository_url (URL)
  - Key: repository_url
  - Required: No
  - Array: No

demo_url (URL)
  - Key: demo_url
  - Required: No
  - Array: No

tags (String)
  - Key: tags
  - Size: 50
  - Required: No
  - Array: Yes

status (String)
  - Key: status
  - Size: 50
  - Required: Yes
  - Default: in_progress

user_id (String)
  - Key: user_id
  - Size: 100
  - Required: Yes

created_at (String)
  - Key: created_at
  - Size: 50
  - Required: Yes

updated_at (String)
  - Key: updated_at
  - Size: 50
  - Required: Yes
```

**Indexes:**
- Index 1:
  - Type: Key
  - Attribute: user_id
  - Order: ASC

#### Collection 2: build_logs

**Settings:**
- Collection ID: `build_logs`
- Name: Build Logs
- Permissions:
  - Create: Users
  - Read: Users
  - Update: Users
  - Delete: Users

**Attributes:**

```
project_id (String)
  - Key: project_id
  - Size: 100
  - Required: Yes

title (String)
  - Key: title
  - Size: 200
  - Required: Yes

content (String)
  - Key: content
  - Size: 10000
  - Required: Yes

log_type (String)
  - Key: log_type
  - Size: 50
  - Required: Yes
  - Default: update

code_snippets (String)
  - Key: code_snippets
  - Size: 5000
  - Required: No
  - Array: Yes

images (String)
  - Key: images
  - Size: 100
  - Required: No
  - Array: Yes

links (String)
  - Key: links
  - Size: 500
  - Required: No
  - Array: Yes

tags (String)
  - Key: tags
  - Size: 50
  - Required: No
  - Array: Yes

created_at (String)
  - Key: created_at
  - Size: 50
  - Required: Yes
```

**Indexes:**
- Index 1:
  - Type: Key
  - Attribute: project_id
  - Order: ASC

## Step 3: Set Up Storage

### Create Storage Bucket

1. Go to "Storage" in the left sidebar
2. Click "Create bucket"
3. Settings:
   - Bucket ID: `buildlog_files`
   - Name: BuildLog Files
   - Permissions:
     - Create: Users
     - Read: Any
     - Update: Users
     - Delete: Users

4. File Settings:
   - Maximum file size: `50MB` (50000000 bytes)
   - Allowed file extensions: `jpg,jpeg,png,gif,webp,svg,pdf,mp4,mov,avi,zip,tar,gz`
   - Compression: Enabled (optional)
   - Encryption: Enabled

## Step 4: Set Up Authentication

### Enable Email/Password Auth

1. Go to "Auth" in the left sidebar
2. Click "Settings"
3. Enable "Email/Password" authentication
4. Configure:
   - Email verification: Optional (enable for production)
   - Password dictionary: Enabled
   - Password history: 5 (optional)
   - Session length: 365 days

### Optional: Enable OAuth Providers

For better UX, you can enable:
- GitHub OAuth
- Google OAuth
- GitLab OAuth

## Step 5: Set Up Functions (Optional - AI Features)

### Create AI Text Generation Function

1. Go to "Functions" in the left sidebar
2. Click "Create function"
3. Settings:
   - Function ID: `ai_text_generator`
   - Name: AI Text Generator
   - Runtime: Python 3.9+
   - Entry point: `main.py`

4. Environment Variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Deploy the function code from `appwrite_functions/ai_text_generator/`

## Step 6: Configure Environment Variables

Update your `.env` file with the credentials:

```env
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id_here
APPWRITE_API_KEY=your_api_key_here

# Database IDs
APPWRITE_DATABASE_ID=buildlog_db

# Collection IDs
APPWRITE_PROJECTS_COLLECTION_ID=projects
APPWRITE_BUILD_LOGS_COLLECTION_ID=build_logs

# Storage Bucket ID
APPWRITE_STORAGE_BUCKET_ID=buildlog_files

# Application Settings
SECRET_KEY=your_random_secret_key_here
DEBUG=True
```

## Step 7: Test Your Setup

Run the following command to test your Appwrite connection:

```bash
python -c "from app.services.appwrite_service import appwrite_service; print('Connected to Appwrite!')"
```

## Troubleshooting

### Common Issues

**Issue: "Project not found"**
- Check your `APPWRITE_PROJECT_ID` in `.env`
- Ensure you're using the correct Appwrite endpoint

**Issue: "Collection not found"**
- Verify collection IDs match exactly
- Check that collections are created in the correct database

**Issue: "Permission denied"**
- Check collection permissions
- Ensure your API key has proper scopes

**Issue: "Storage bucket not found"**
- Verify bucket ID matches `.env` configuration
- Check bucket permissions

## Security Best Practices

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use API Key with minimal permissions** - Create a dedicated API key for the app
3. **Enable rate limiting** - Protect against abuse
4. **Use HTTPS only** - Ensure secure communication
5. **Implement proper authentication** - Don't skip user verification
6. **Regular backups** - Export your data regularly

## Production Deployment

When deploying to production:

1. **Set `DEBUG=False`** in your `.env`
2. **Use environment secrets** - Don't hardcode credentials
3. **Enable email verification** - For Auth
4. **Set up monitoring** - Use Appwrite's monitoring features
5. **Configure CORS** - Only allow your domain
6. **Enable 2FA** - For admin accounts
7. **Set up backups** - Schedule regular database backups

## Next Steps

After completing the setup:

1. Run the application: `python main.py`
2. Visit `http://localhost:8000`
3. Create your first project
4. Add build logs
5. Export to markdown
6. Generate your public portfolio

## Support

If you encounter issues:

1. Check [Appwrite Documentation](https://appwrite.io/docs)
2. Visit [Appwrite Discord](https://appwrite.io/discord)
3. Create an issue on the [BuildLog GitHub repo](https://github.com/yourusername/buildlog/issues)

---

**Happy Building with BuildLog and Appwrite!**
