FROM php:8.2-apache

RUN docker-php-ext-install pdo_mysql

COPY index.php db.php style.css /var/www/html/

RUN apt-get update && apt-get install -y --no-install-recommends zip \
    && cd /var/www/html && zip -q source.zip index.php db.php style.css \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R root:root /var/www/html \
    && find /var/www/html -type d -exec chmod 0555 {} + \
    && find /var/www/html -type f -exec chmod 0444 {} +

EXPOSE 80
