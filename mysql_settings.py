# MySQL Configuration Template
# Copy these settings to your settings.py when you have MySQL set up

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rh_db',  # Replace with your database name
        'USER': 'root',   # Replace with your MySQL username
        'PASSWORD': '',   # Replace with your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Make sure to install mysqlclient: pip install mysqlclient
# And create the database in MySQL before running migrations