# 📦 Buyer-Seller
## 📖 Overview
Welcome to the Buyer-Seller Management System! 
This is a web application with role-based functionality that displays different dashboards based on the 
user's role (Buyer, Seller, or Superadmin). Buyers and Sellers see KPI cards with key information related to their 
purchases or sales, while Superadmins can manage buyers and sellers.

The system is built with Django, providing a robust backend to handle all inventory operations while leveraging 
RESTful API architecture for frontend integrations.
![GitHub](https://img.shields.io/badge/GitHub-Buyer_seller_management-blue?style=flat-square&logo=github)
![Django](https://img.shields.io/badge/Django-Python-yellow?style=flat-square&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-green?style=flat-square&logo=postgresql)
![Postman](https://img.shields.io/badge/Postman-Testing-blueviolet?style=flat-square&logo=postman)

## ✨ Features
- **Buyer KPI Dashboard**: Displays total purchases, purchases in process, approved purchases, and rejected purchases.
- **Seller KPI Dashboard**: Displays total sale requests, in-process sale requests, approved sale requests, and rejected sale requests.
- **Superadmin Role**: Can view and manage both buyers and sellers.
- **JWT Authentication**: Secure API requests using JWT tokens.
- **Unit Testing**: Comprehensive test coverage to ensure code quality and functionality.

## 🛠️ Technologies Used
- 🐍**Python & Django:** A high-level Python web framework that encourages rapid development.
- 🌐**Django REST Framework:** For building Web APIs. 
- 🗄️**PostgreSQL:** Robust database system for data storage.  ️
- 🔐**JWT (JSON Web Tokens):** For user authentication.

## 🚀 Quick Start
Follow the steps below to get the project running on your local machine.
## 🔧 Installation
Make sure you have Python 3.x installed. Clone the repository and navigate to the project directory. Install the required dependencies using the `requirements.txt` file.
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Onkar-Kul/Buyer-Seller.git

2. **Create Virtual Environment**
   ```bash
    python -m venv venv
    source venv/bin/activate  
    # On Windows: venv\Scripts\activate

3. **Install all dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set up the database**

   Create a PostgreSQL database and update your settings.py with the database configuration.

5.  **Set up the environment variables**

    Create a .env file and set all the environment variable described in dist file

6. **Create and Run migrations**
    ```bash
   python manage.py makemigrations
   python manage.py migrate

7. **Run development server**
    ```bash
   python manage.py runserver
