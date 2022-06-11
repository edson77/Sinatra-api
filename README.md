# Clone the project

### `git clone https://github.com/edson77/Sinatra-api.git`

# create a virtual environment

### `# python -m venv .env`

Then you have to source this virtual environment

### `# source  .env/Scripts/activate`

if you are under windows, you must use git bash as terminal
NB: it is important to source the environment throughout the process

## reinstall Django dependencies

We reinstall our version of Django and the dependencies of our project, we use the requirement file

### `# pip install -r requirements.txt`

### enter the src folder `# cd Sinatra-api/src`

### run server `# python manage.py runserver`
NB: for the database, you have to run the command `# python manage.py makemigrations` and `# python manage.py migrate`
Runs the app in the development mode.\
Open [http://localhost:8000](http://localhost:8000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.


## Learn More

for this application to work, you need a frontend, this frontend is made with React + Redux [https://github.com/edson77/chat-app](https://github.com/edson77/chat-app).

