FROM php:7.4-apache

COPY flag.txt /flag.txt
RUN chmod 0644 /flag.txt && chown root:root /flag.txt

COPY index.php   /var/www/html/index.php
COPY gadgets.php /var/www/html/gadgets.php
COPY uploads/    /var/www/html/uploads/
COPY style.css   /var/www/html/style.css
RUN chown -R root:root /var/www/html \
    && find /var/www/html -type d -exec chmod 0555 {} + \
    && find /var/www/html -type f -exec chmod 0444 {} + \
    && chown -R www-data:www-data /var/www/html/uploads \
    && chmod 0777 /var/www/html/uploads

EXPOSE 80
