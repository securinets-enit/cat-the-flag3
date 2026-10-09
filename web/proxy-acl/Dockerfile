FROM nginx:1.25-alpine

COPY www/public/ /var/www/protected/public/
COPY www/files/  /var/www/protected/files/
COPY www/secret/ /var/www/protected/secret/
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
