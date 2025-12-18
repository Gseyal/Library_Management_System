# 📚 Library Management System

A comprehensive web-based Library Management System built with Flask that enables efficient management of library operations, including book cataloging, user management, and book issue/return tracking.

## ✨ Features

### 👨‍💼 Admin Features
- **Section Management**: Create, update, and delete library sections
- **Book Management**: Add books to sections with details (title, author, content, images, PDF files)
- **User Management**: View and manage registered users
- **Request Handling**: Approve or reject book issue requests from users
- **Issue Tracking**: Monitor all issued books with due dates and days remaining
- **Revoke Access**: Revoke issued books when necessary
- **Analytics Dashboard**: View statistics with charts showing:
  - Books per section (Bar chart)
  - Section distribution (Donut chart)
  - Books issued vs available
- **Search Functionality**: Search sections and books

### 👥 User Features
- **User Registration & Login**: Secure user authentication
- **Browse Sections**: View all available library sections
- **Browse Books**: Explore books in each section
- **Request Books**: Submit requests to borrow books
- **Track Requests**: Monitor status of book requests (Under Process, Accepted, Rejected)
- **My Books**: View currently issued books with return dates
- **Return Books**: Return borrowed books
- **Search**: Search for specific sections and books
- **Read Online**: Access book content directly through the platform

## 🛠️ Technology Stack

### Backend
- **Flask 3.1.2** - Web framework
- **SQLAlchemy 2.0.45** - ORM for database operations
- **Flask-SQLAlchemy 3.1.1** - Flask extension for SQLAlchemy

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5.3.2** - Responsive UI framework
- **Jinja2 3.1.6** - Template engine

### Data Visualization
- **Matplotlib 3.10.8** - Generate charts and graphs
- **NumPy 2.3.5** - Numerical operations

### Database
- **SQLite** - Lightweight database for data persistence

## 📁 Project Structure

```
Library_Management_System/
│
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── template.html              # Template for dynamically created section pages
│
├── application/               # Application package
│   ├── config.py             # Configuration settings
│   ├── database.py           # Database initialization
│   ├── models.py             # Database models (Admin, User, Section, Books, etc.)
│   └── controllers.py        # Route handlers and business logic
│
├── info_base/                # Database storage
│   └── library.db           # SQLite database file
│
├── static/                   # Static files
│   ├── background4.jpg      # Background image
│   ├── image.png           # Generated bar chart
│   └── image2.png          # Generated donut chart
│
└── templates/               # HTML templates
    ├── Login_2.html        # Login page
    ├── signup.html         # User registration
    ├── admin_dashboard.html # Admin dashboard
    ├── user_dashboard.html  # User dashboard
    ├── request.html        # Book requests page
    ├── action.html         # Book issue tracking
    ├── user_book_show.html # User's issued books
    ├── stat.html           # Statistics page
    └── [Section].html      # Dynamically created section pages
```

## 🗄️ Database Schema

### Tables

1. **admin**
   - `admin_id` (Primary Key)
   - `username` (Unique)
   - `password` (Unique - design limitation in current implementation)

2. **user**
   - `user_id` (Primary Key)
   - `username` (Unique)
   - `password` (Unique - design limitation in current implementation)
   - `books_issued` (Integer)

3. **section**
   - `section_id` (Primary Key)
   - `admin_id` (Foreign Key → admin)
   - `title` (Unique)
   - `date`
   - `image`
   - `description`

4. **books**
   - `book_id` (Primary Key)
   - `sec_id` (Foreign Key → section)
   - `section`
   - `user_issued` (Foreign Key → user)
   - `Title`
   - `Author`
   - `Content`
   - `Image`
   - `file` (PDF link/path)

5. **book_issue**
   - `issue_id` (Primary Key)
   - `title` (String, Foreign Key → books.book_id, Unique)
   - `user_id` (Integer, Foreign Key → user, Unique)
   - `admin_id` (Integer)
   - `date_issue` (Date)
   - `date_return` (Date)
   - `days_left` (Integer)
   - `book_id` (Integer)

6. **allotment**
   - `req_id` (Primary Key)
   - `book_id` (Integer)
   - `title` (Integer, Foreign Key → books.Title)
   - `user_id` (Integer, Foreign Key → user)
   - `status` (String, default='UnderProcess')
   - `date` (Date)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gseyal/Library_Management_System.git
   cd Library_Management_System
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   The database will be automatically created when you first run the application.
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## 📖 Usage Guide

### For Administrators

1. **Login**
   - Navigate to the homepage
   - Click on "ADMIN" login
   - Enter admin credentials

2. **Manage Sections**
   - Click "Add Section" to create a new library section
   - Provide section title, date, image URL, and description
   - Delete sections using the delete button

3. **Manage Books**
   - Navigate to a section
   - Click "Add Book" to add new books
   - Provide book details: title, author, content, image URL, and PDF file link
   - Delete books using the delete option

4. **Handle Requests**
   - View all pending book requests in the "Requests" section
   - Approve or reject requests
   - Approved books are automatically issued for 7 days

5. **Monitor Issued Books**
   - Navigate to "Actions" to see all issued books
   - View days remaining for each book
   - Revoke books if needed

6. **View Analytics**
   - Click "Statistics" to view:
     - Books per section distribution
     - Issued vs available books
     - Visual charts and graphs

### For Users

1. **Register**
   - Click "Sign Up" on the login page
   - Create an account with username and password

2. **Login**
   - Select "USER" login
   - Enter your credentials

3. **Browse Books**
   - Explore different sections
   - Click on sections to view available books
   - Use search to find specific books

4. **Request Books**
   - Click "Request" on any available book
   - Track your requests in "My Requests"
   - See status: Under Process, Accepted, or Rejected

5. **Manage Your Books**
   - View issued books in "My Books"
   - Check return dates and days remaining
   - Return books when finished

6. **Read Books**
   - Click "View" to read book content online
   - Access PDF files directly

## 🛣️ API Routes

### Authentication Routes
- `GET /` - Login page
- `POST /login?client=[ADMIN|USER]` - Login handler
- `POST /register` - User registration
- `GET /logout` - Logout handler

### Admin Routes
- `GET /Homepage?client=ADMIN` - Admin dashboard
- `POST /add?client=ADMIN` - Add new section
- `GET /delete_section?title=<title>&client=ADMIN` - Delete section
- `GET /delete_section_book?section=<section>&book=<book>&client=ADMIN` - Delete book
- `POST /add_books?section=<section>&client=ADMIN` - Add book to section
- `GET /issued?bookid=<id>&reqid=<id>&client=ADMIN` - Approve book request
- `GET /rejected?reqid=<id>&client=ADMIN` - Reject book request
- `GET /action` - View all issued books
- `GET /revoke?issid=<id>&who=ADMIN` - Revoke issued book

### User Routes
- `GET /Homepage?client=USER` - User dashboard
- `GET /section_books?page=<section>&who=USER&sect_id=<id>` - View section books
- `GET /user_requested?client=USER&user_id=<id>&title=<title>&bookid=<id>` - Request book
- `GET /request?client=USER` - View user's requests
- `GET /user_book?client=USER` - View user's issued books
- `GET /revoke?issid=<id>&who=USER` - Return book
- `GET /view?bookid=<id>` - View book content

### Analytics & Search Routes
- `GET /stat?client=[ADMIN|USER]` - View statistics
- `POST /search?client=[ADMIN|USER]` - Search sections
- `POST /search_book?client=[ADMIN|USER]&which=<section>` - Search books

## 🔒 Security Features

- Password-based authentication for both admins and users
- Session management for maintaining user state
- Role-based access control (Admin vs User privileges)
- Input validation through form submissions
- SQL injection prevention through SQLAlchemy ORM

## 📊 Analytics

The system generates real-time analytics including:
- **Bar Chart**: Shows total books and issued books per section
- **Donut Chart**: Displays section-wise book distribution
- Automatically updates when data changes

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Test your changes before submitting
- Update documentation as needed

## 📝 Future Enhancements

Potential improvements for the system:
- Email notifications for due dates and approvals
- Advanced search with filters (author, date, availability)
- Book reviews and ratings
- Fine calculation for overdue books
- Export reports to PDF/Excel
- Multi-language support
- Mobile application
- Barcode scanning for physical books
- Book reservation system
- Reading history and recommendations

## 🐛 Known Issues

- User limit for book issues is tracked but not enforced with a hard limit
- Password storage should use hashing (currently stored as plain text)
- Passwords are marked as unique in the database schema, which is unnecessary
- Foreign key relationships in book_issue and allotment tables have naming inconsistencies
- File upload functionality stores only URLs/paths (no actual file upload)

## 📄 License

This project is open source. Please check with the repository owner for license details.

## 👤 Author

**Gseyal**
- GitHub: [@Gseyal](https://github.com/Gseyal)
- Repository: [Library_Management_System](https://github.com/Gseyal/Library_Management_System)

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap for the responsive UI framework
- Matplotlib for data visualization capabilities
- SQLAlchemy for robust database ORM

---

**Note**: This is an educational project. For production use, implement proper security measures including password hashing, CSRF protection, and secure session management.

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/Gseyal/Library_Management_System/issues) page
2. Create a new issue with detailed information
3. Contact the repository maintainer

---

<div align="center">
Made with ❤️ by Gseyal
</div>
