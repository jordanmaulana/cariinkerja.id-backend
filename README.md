# CariInKerja.id Backend

🇮🇩 **Indonesia's First Open Source Job Searching Assistant and Profile Assessment Platform**

A comprehensive Django-powered backend system that revolutionizes job searching and career development in Indonesia. This platform combines intelligent job matching, automated profile assessment, and career guidance tools to help Indonesian job seekers find their perfect career opportunities.

## 🌟 Key Features

- **Smart Job Search**: AI-powered job matching based on skills, experience, and preferences
- **Profile Assessment**: Comprehensive career profile evaluation and recommendations
- **Job Management**: Complete job posting and application tracking system
- **User Profiles**: Detailed professional profile management with skill assessments
- **RESTful API**: Full API support for mobile and web applications
- **Admin Dashboard**: Comprehensive admin panel for platform management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for Tailwind CSS)
- n8n (for job data automation and feeding the jobs database)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cariinkerja.id-backend
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   source ./bin/install-tailwind.sh
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and settings
   ```

5. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Configure n8n workflows**
   ```bash
   # Import the available n8n workflow nodes from n8n_nodes/ folder
   # These workflows will automatically feed job data into your database
   ```

## 🏃‍♂️ Running the Application

1. **Start Tailwind CSS (in one terminal)**
   ```bash
   npm run tw
   ```

2. **Start Django server (in another terminal)**
   ```bash
   python manage.py runserver
   ```

## 🔗 Important URLs

- **Admin Panel**: http://localhost:8000/admin
- **API Documentation (Swagger)**: http://localhost:8000/swagger/
- **API Documentation (ReDoc)**: http://localhost:8000/redoc/
- **Main Dashboard**: http://localhost:8000/dashboard

## 🤖 n8n Integration

This project requires **n8n** to automatically feed job data into the database. The platform uses n8n workflows to scrape and process job listings from various sources.

### Available Workflow Nodes

The `n8n_nodes/` folder contains pre-built workflow configurations:
- **weworkremotely.json**: Workflow for scraping remote job listings from WeWorkRemotely
- **indeed.json**: Workflow for scraping job listings from Indeed

### Setting up n8n Workflows

1. Install and set up n8n on your system
2. Import the workflow files from the `n8n_nodes/` folder into your n8n instance
3. Configure the workflows with your database connection details
4. Schedule the workflows to run periodically for automatic job data updates

**Note**: These workflows are essential for populating the jobs database. Without n8n, you'll need to manually add job listings through the admin panel.

## 🛠️ Development

### Creating New Apps
```bash
cd apps/
../manage.py startapp your_app_name
```

### Useful Commands
```bash
# Run development server
python manage.py runserver

# Run Tailwind CSS watcher
npm run tw

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## 📄 License

This project is licensed under the Creative Commons Attribution 4.0 International License. See the [LICENSE](LICENSE) file for details.

**Attribution Required**: If you use this project, please provide appropriate credit to the original author.

## 🤝 Contributing

We welcome contributions to make this the best job searching platform for Indonesia! 

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🌟 About

This project aims to revolutionize the job market in Indonesia by providing the first open-source, comprehensive job searching and profile assessment platform. Built with modern technologies and designed for the Indonesian job market.

---

**Made with ❤️ for Indonesia's job seekers**
