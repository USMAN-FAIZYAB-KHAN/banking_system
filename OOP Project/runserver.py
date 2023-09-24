import os
import webbrowser
try:
    import django
    print("Django is already installed")
except ImportError:
    print("Django not installed")
    print("Installing Django...")
    os.system("pip install django")
    print("Django installed")
finally:
    print("Running server...")
    webbrowser.open("http://127.0.0.1:8000/")
    os.system("python .\\banking_system\\manage.py runserver")