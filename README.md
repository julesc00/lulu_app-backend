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

## AWS EC2 Ubuntu Linux configuration
1. Update OS `sudo apt udpate && sudo apt upgrade -y` 
2. Install pipenv `python3 install pipenv` 
3. Create new environment `python3 -m venv env`
4. Activate virtual environment `source env/bin/activate`
5. Create ssh keys to connect to GitHub account `ssh-keygen -t ed25519 -C "your_email@example.com"`
6. Cat the public key `cat ~/.ssh/id_ed25519.pub`