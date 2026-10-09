<?php
$DB_HOST = getenv('DB_HOST') ?: 'prepared-sqli-db';
$DB_NAME = getenv('DB_NAME') ?: 'shop';
$DB_USER = getenv('DB_USER') ?: 'webapp';
$DB_PASS = getenv('DB_PASS') ?: 'webapp_pw_2024';

$pdo = new PDO(
    "mysql:host={$DB_HOST};dbname={$DB_NAME};charset=utf8mb4",
    $DB_USER,
    $DB_PASS,
    [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]
);
