File Integrity Monitor (FIM)

A simple desktop application built using Python and `customtkinter` that allows you to monitor the integrity of important files by hashing and tracking their changes in a PostgreSQL database. It includes admin authentication and features a clean GUI interface.

## Features

-  **Admin Authentication** before sensitive actions
-  **Add or Update File Hashes** (SHA-256)
-  **Check Integrity** of monitored files
-  **View All Records** from the database
-  **Remove File Records** securely
-  Scrollable GUI built with `customtkinter`
-  PostgreSQL backend for persistent storage


 Prerequisites

- Python 3.10+
- PostgreSQL installed and running
- Git (if cloning the repo)

 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Yadhveer/File-Integrity-Monitor.git
   cd File-Integrity-Monitor

2. Install dependencies:
   
   ```bash
   pip install customtkinter psycopg2

4. Configure your PostgreSQL credentials:
5. Create the required database table:

   CREATE TABLE IF NOT EXISTS hash (
    name TEXT PRIMARY KEY,
    hash_value TEXT,
    last_modified TIMESTAMP
);

7. Run the application:

   python app.py

