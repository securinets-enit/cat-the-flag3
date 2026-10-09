FROM php:8.2-apache

COPY flag.txt /flag.txt
RUN chmod 0444 /flag.txt

COPY index.php style.css /var/www/html/
RUN chown -R root:root /var/www/html \
    && find /var/www/html -type f -exec chmod 0444 {} +

EXPOSE 80
