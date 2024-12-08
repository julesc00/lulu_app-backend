# Lulu's App | Backend

## Organization

### Apps | Domains

- users
- api
- clients
- services or treatments
- support
- marketing
- payments
- ai_assistant

### Model Precedence 
1. User, allauth
2. Token
3. Client
4. Service
5. Marketing
6. Support
7. Payment
8. AIAssistant

### Model: User
Default user model

### Model Token 
- user, FK
- token Google Places API Autocomplete Library

## Terraform
1. Validate templates `terraform validate`
2. Create plan for review: `terraform plan -out=tfplan.plan -var-file="variables.tfvars"`
3. Provision infrastructure: `terraform apply tfplan.plan` ***Note:*** Don't need to add the var file if added to the plan

## AWS EC2 Ubuntu Linux instance creation
[Deploy a Django web app with Nginx to AWS EC2](https://www.youtube.com/watch?v=7O1H9kr1CsA)
Note project/root dir `elevate`

## AWS EC2 Ubuntu Linux configuration
1. Update OS `sudo apt udpate && sudo apt upgrade -y` 
2. Install pipenv `sudo apt install python3-venv  python3 install pipenv` 
3. Create new environment `python3 -m venv env`
4. Activate virtual environment `source env/bin/activate`
5. Create ssh keys to connect to GitHub account `ssh-keygen -t ed25519 -C "julesc00@protonmail.com"`
6. Cat the public key `cat ~/.ssh/id_ed25519.pub`
7. Clone repository `git clone git@github.com:julesc00/lulu_app-backend.git`  
    - Remember to update codebase if outside changes are made to the repository.
8. Install Nginx `sudo apt install nginx -y`
9. Install gunicorn `pip install gunicorn`, it should have already been installed from the requirements.txt file.

## Initial Django setup
1. Migrate default Django model `./manage.py migrate`
2. Make model migrations `./manage.py makemigrations clients` and then `./manage.py migrate clients`
3. Create superusers `./manage.py createsuperuser`, ***Note:*** Create strong passwords for prod environment.

## Install and configure supervisor
This app will make sure the Django server keeps running in the background
1. Install supervisor `sudo apt install supervisor`
2. Configure supervisor
    ```
   environment=PATH="/home/ubuntu/lulu_app-backend/env/bin",PYTHONPATH="/home/ubuntu/lulu_app-backend",HOME="/home/ubuntu"

   /home/ubuntu/lulu_app-backend/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/lulu_app-backend/backend/app.sock backend.wsgi:application

   
   
   # Switch to 
    cd /etc/supervisor/conf.d/
   
   # Create a new configuration file
    sudo touch gunicorn.conf
   
   # Edit file with sudo vim gunicorn.conf
   
   [program:gunicorn]
   directory=/home/ubuntu/lulu_app-backend
   command=/home/ubuntu/lulu_app-backend/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/lulu_app-backend/app.sock backend.wsgi.application
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/gunicorn/gunicorn.err.log
   stdout_logfile=/var/log/gunicorn/gunicorn.out.log
   user=ubuntu

   
   [group:guni]
   programs:gunicorn
   ```
3. Create dir `sudo mkdir /var/log/gunicorn`
4. Tell supervisor to reread `sudo supervisorctl reread` and `sudo supervisorctl update`
   ```aiignore
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl restart gunicorn
   ```

## Nginx configuration
1. Check nginx status `sudo systemctl restart nginx`
2. Restart service `sudo systemctl restart nginx`