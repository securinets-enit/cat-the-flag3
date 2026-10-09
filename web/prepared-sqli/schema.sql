USE shop;

CREATE TABLE products (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  title  VARCHAR(128) NOT NULL,
  price  DECIMAL(10,2) NOT NULL,
  active TINYINT NOT NULL DEFAULT 1
);

INSERT INTO products (title, price, active) VALUES
  ('Aegis Firewall License', 499.00, 1),
  ('Sentinel VPN Seat',       79.00, 1),
  ('Warden EDR Agent',       129.00, 1),
  ('Cipher Vault',           249.00, 1),
  ('Beacon SIEM Connector',  349.00, 1),
  ('Relay Mail Gateway',     199.00, 0);

CREATE TABLE internal_notes (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  secret VARCHAR(128) NOT NULL
);
