# To run this app
cd to the frontend directiory 
and run: npm run dev

# For the backend
cd to the backend directory in a new terminal
,activate the virtual environment and type : python manage.py runserver 8001
open another terminal, activate the virtual environment and type: redis-server
open another terminal, activate the virtual environment and type: celery -A backend worker --loglevel=info 


# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Backend setup:

1. Enter backend directory
2. Create a virtual environment using the command `python3 -m venv ./venv`
3. Enter the Python virtual environment using the command `source venv/bin/activate` on MacOS, or `source venv/scripts/activate` on Windows
4. Install Django
5. Run the backend using `python manage.py runserver 8001`