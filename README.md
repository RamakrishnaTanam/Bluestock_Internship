# Bluestock IPO Management System

A Django-based web application for managing IPO listings and applications.

## Features

- Admin dashboard with statistics
- IPO listing management
- User profile management
- Application tracking
- Import/export functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bluestock.git
cd bluestock
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python backend/manage.py migrate
```

5. Create a superuser:
```bash
python backend/manage.py createsuperuser
```

6. Run the development server:
```bash
python backend/manage.py runserver
```

## Project Structure

```
bluestock/
├── backend/
│   ├── bluestock/          # Project settings
│   ├── dashboard/          # Admin dashboard app
│   ├── ipo/               # IPO management app
│   ├── users/             # User management app
│   └── manage.py
├── frontend/              # Frontend assets
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 