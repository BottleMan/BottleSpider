# start nginx
service nginx start

# start uwsgi
uwsgi --ini uwsgi.ini

# prevent container from exiting
tail -f /var/log/nginx/error.log
