## Deploying the Flask App (Linux/EC2)

1. Install all packages

```bash
## Packages and their use cases:
## python3     -> I mean...Python
## python3-pip -> Package manager for Python
## gunicorn    -> We'll use this to run the Python server in prod
## git         -> bruh
## nginx       -> To host the service
sudo apt-get update -y  && sudo apt-get install python3 python3-pip gunicorn git anthropic nginx -y
```


2. Clone the GitHub Repository

```bash
git clone https://github.com/sreekeshiyer/tech-support-assist.git
cd tech-support-assist
```

3. Install all Python dependencies

```bash
pip install -r requirements.txt
```

4. Setup Nginx

While you will use gunicorn to run the app, it needs to be portforwarded to HTTP so that it can be served directly on a public IP (and then mapped to a domain if you wish to)
Here's where nginx comes in.

```bash
cd /etc/nginx/sites-enabled
# I use nano, but you can choose your favorite text editor. or vim.
sudo nano flaskapp

## Paste the following in the file. And obviously take out the hashes. <PUBLIC_IPV4> is your public IP address. It's easy to find in the Network settings for AWS EC2.
# server {
#     listen 80;
#     server_name <PUBLIC_IPV4>;
#     access_log  /var/log/nginx/example.log;

#     location / {
#         proxy_pass http://127.0.0.1:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#     }
#   }
##
# Restart and enable nginx
sudo systemctl restart nginx && sudo systemctl enable nginx

# Start the Python Server
# once you switch to the right directory
cd ~/tech-support-assist
gunicorn -w 1 wsgi:app
```

And you should be able to access the app directly from your public IPv4 address. 
