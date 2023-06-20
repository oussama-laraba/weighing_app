

-- go the mysql shell 
\sql
\connect root@localhost
CREATE DATABASE weighing;
\use weighing

SHOW TABLES;  -- return all the table of the database;


CREATE TABLE uom (
    id INT  NOT NULL  AUTO_INCREMENT,
    uom_name VARCHAR(20),   
    PRIMARY KEY (id),
    CONSTRAINT UNIQUE_UOM_NAME UNIQUE (name)
  
);

CREATE TABLE product (
    id INT  AUTO_INCREMENT  NOT NULL,
    odoo_id   INT NOT NULL,
    product_name  VARCHAR(255) NOT NULL,
    tracking VARCHAR(40) NOT NULL,

    PRIMARY KEY (id)
);


CREATE TABLE product_uom   (
    product_id INT  NOT NULL,
    uom_id INT NOT NULL,
    
    PRIMARY KEY (product_id , uom_id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (uom_id) REFERENCES uom(id)
 
);

CREATE TABLE company   (
    id INT  NOT NULL  AUTO_INCREMENT,
    odoo_id   INT NOT NULL,
    company_name VARCHAR(20),   
    PRIMARY KEY (id)
);


CREATE TABLE location   (
    id INT  NOT NULL  AUTO_INCREMENT,
    odoo_id   INT NOT NULL,
    location_name VARCHAR(255) , 
    company_id INT  NOT NULL,   
    PRIMARY KEY (id),
    FOREIGN KEY (company_id) REFERENCES company(id)
);

CREATE TABLE lot  (
    id INT  NOT NULL  AUTO_INCREMENT,
    odoo_id INT NOT NULL, 
    product_id INT NOT NULL,
    location_id INT NOT NULL,
    date DATETIME NOT NULL, 
    weight FLOAT , 
    quantity INT ,
    barcode VARCHAR(255) , 
    extra_information VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (location_id) REFERENCES location(id)

);

CREATE TABLE server   (
    id INT  NOT NULL  AUTO_INCREMENT,
    url VARCHAR(255) NOT NULL, 
    port INT NOT NULL,
    database_name VARCHAR(50) NOT NULL ,
    
    PRIMARY KEY (id)
);

CREATE TABLE user   (
    id INT  NOT NULL  AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL, 
    password VARCHAR(255) NOT NULL,
    server_id INT NOT NULL , 
    PRIMARY KEY (id),
    FOREIGN KEY (server_id) REFERENCES server(id)
);

CREATE TABLE stock_location    (
    server_id INT  NOT NULL,
    location_id INT  NOT NULL,
    product_id INT  NOT NULL,
    
    quantity INT ,
     
    PRIMARY KEY (server_id, location_id, product_id),
    FOREIGN KEY (server_id) REFERENCES server(id),
    FOREIGN KEY (location_id) REFERENCES location(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);


CREATE TABLE user_location (
    user_id INT  NOT NULL,
    location_id INT  NOT NULL,
    PRIMARY KEY (user_id, location_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (location_id) REFERENCES location(id)
);