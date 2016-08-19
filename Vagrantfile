# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.hostname = "ocr-with-django.local"

  config.vm.network "forwarded_port", guest: 80, host: 8000
  config.vm.network "forwarded_port", guest: 8000, host: 8001

  config.vm.synced_folder ".", "/home/ubuntu/ocr_with_django/"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 1
    vb.name = "ocr-with-django"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y git build-essential python3 python3.5-venv python3-dev nginx supervisor
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv-3.5 --without-pip ocr_with_django_venv
    source ocr_with_django_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

    pip install Cython==0.24.1
    pip install -r ocr_with_django/requirements.txt

    cd ocr_with_django/ocr_with_django/

    python manage.py migrate
    python manage.py collectstatic --noinput
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    echo '
upstream ocr_with_django_upstream {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name localhost;

    client_max_body_size 4G;

    access_log /home/ubuntu/ocr_with_django/nginx_access.log;
    error_log /home/ubuntu/ocr_with_django/nginx_error.log;

    location /static/ {
        alias /home/ubuntu/ocr_with_django/ocr_with_django/static/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://ocr_with_django_upstream;
            break;
        }
    }
}
    ' > /etc/nginx/conf.d/ocr_with_django.conf
    /bin/systemctl restart nginx.service
SHELL

config.vm.provision "shell", inline: <<-SHELL
  echo '
[program:ocr_with_django]
user = ubuntu
directory = /home/ubuntu/ocr_with_django/ocr_with_django/
command = /home/ubuntu/ocr_with_django_venv/bin/gunicorn ocr_with_django.wsgi
autostart = true
autorestart = true
stderr_logfile = /home/ubuntu/ocr_with_django/gunicorn_stderr.log
stdout_logfile = /home/ubuntu/ocr_with_django/gunicorn_stdout.log
stopsignal = INT
  ' > /etc/supervisor/conf.d/ocr_with_django.conf
  /bin/systemctl restart supervisor.service
SHELL
end
