# InsureTech Django Backend

## Project Setup

### Prerequisites
- Python 3.11
- Docker
- Docker Compose

### Environment Setup
1. Copy `.env.example` to `.env`
2. Fill in the necessary environment variables

### Development
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`
- Start development server: `python manage.py runserver`

### Docker Deployment
- Build and run: `docker-compose up --build`

### Key Dependencies
- Django 4.2.9
- Django REST Framework
- PostgreSQL
- Gunicorn

### Project Structure
- `insuretech/`: Main Django project directory
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
