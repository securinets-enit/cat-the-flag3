FROM php:8.2-apache

COPY flag.txt /flag.txt
RUN chmod 0644 /flag.txt

COPY index.php /var/www/html/index.php
COPY pages/ /var/www/html/pages/
COPY style.css /var/www/html/style.css

RUN chown -R root:root /var/www/html \
	&& find /var/www/html -type d -exec chmod 0555 {} + \
	&& find /var/www/html -type f -exec chmod 0444 {} +

EXPOSE 80
 