/* DATABASE INITIALIZATION : example.db :: sqlite3                  */

INSERT INTO country ( name )
     VALUES ( 'Canada' );

INSERT INTO country ( name )
     VALUES ( 'Germany' );

INSERT INTO country ( name )
     VALUES ( 'United Kingdom' );

INSERT INTO country ( name )
     VALUES ( 'United States' );

INSERT INTO customer ( name, country_id )
     SELECT 'Jami', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO customer ( name, country_id )
     SELECT 'Jeremy', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO customer ( name, country_id )
     SELECT 'Marty', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO customer ( name, country_id )
     SELECT 'Pilan', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO customer ( name, country_id )
     SELECT 'Rajneel', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO merchant ( name, country_id )
     SELECT 'Bubba Trump Shrimp Co.', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO merchant ( name, country_id )
     SELECT 'Good Time Poke', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO merchant ( name, country_id )
     SELECT 'Hagenbratwursts AG', country.id
       FROM country
      WHERE country.name = 'Germany';

INSERT INTO merchant ( name, country_id )
     SELECT 'PrintGuys', country.id
       FROM country
      WHERE country.name = 'Canada';

INSERT INTO merchant ( name, country_id )
     SELECT 'Punksenselessness, Inc.', country.id
       FROM country
      WHERE country.name = 'United States';

INSERT INTO merchant ( name, country_id )
     SELECT 'Wonka Farms Limited', country.id
       FROM country
      WHERE country.name = 'United Kingdom';

INSERT INTO product ( merchant_id, name, price, status )
     SELECT merchant.id, 'Candy Corn', 3.99, 'Available'
       FROM merchant
      WHERE merchant.name = 'Wonka Farms Limited';

INSERT INTO product ( merchant_id, name, price, status )
     SELECT merchant.id, "Donnie's Fried Chicken and Shrimp", 18.59, 'Available'
       FROM merchant
      WHERE merchant.name = 'Bubba Trump Shrimp Co.';

INSERT INTO product ( merchant_id, name, price, status )
     SELECT merchant.id, 'Door Hangers', 0.04, 'Available'
       FROM merchant
      WHERE merchant.name = 'PrintGuys';

INSERT INTO product ( merchant_id, name, price, status )
     SELECT merchant.id, 'Hot Oil Salmon Poke', 14.00, 'Available'
       FROM merchant
      WHERE merchant.name = 'Good Time Poke';

INSERT INTO product ( merchant_id, name, price, status )
     SELECT merchant.id, 'Pizza Rolls', 0.99, 'Available'
       FROM merchant
      WHERE merchant.name = 'Punksenselessness, Inc.';

INSERT INTO product ( merchant_id, name, price, status )
     SELECT merchant.id, 'Thai Pale Ale', 5.99, 'Available'
       FROM merchant
      WHERE merchant.name = 'Hagenbratwursts AG';

INSERT INTO customer_order ( customer_id, status )
     SELECT customer.id, 'Pending'
       FROM customer
      WHERE customer.name = 'Jami';

INSERT INTO customer_order ( customer_id, status )
     SELECT customer.id, 'Complete'
       FROM customer
      WHERE customer.name = 'Jeremy';

INSERT INTO customer_order ( customer_id, status )
     SELECT customer.id, 'Complete'
       FROM customer
      WHERE customer.name = 'Marty';

INSERT INTO customer_order ( customer_id, status )
     SELECT customer.id, 'Pending'
       FROM customer
      WHERE customer.name = 'Pilan';

INSERT INTO customer_order ( customer_id, status )
     SELECT customer.id, 'Complete'
       FROM customer
      WHERE customer.name = 'Rajneel';

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id
                  FROM customer_order
                 WHERE customer_order.customer_id =
                     ( SELECT customer.id
                         FROM customer
                        WHERE customer.name = 'Jami' ) ),
              ( SELECT product.id
                  FROM product
                 WHERE product.name="Candy Corn" ),
              ( 3 ) );

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id
                  FROM customer_order
                 WHERE customer_order.customer_id =
                     ( SELECT customer.id
                         FROM customer
                        WHERE customer.name = 'Jeremy' ) ),
              ( SELECT product.id
                  FROM product
                 WHERE product.name='Hot Oil Salmon Poke' ),
              ( 1 ) );

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id
                  FROM customer_order
                 WHERE customer_order.customer_id =
                     ( SELECT customer.id
                         FROM customer
                        WHERE customer.name = 'Jeremy' ) ),
              ( SELECT product.id
                  FROM product
                 WHERE product.name='Thai Pale Ale' ),
              ( 1 ) );

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id
                  FROM customer_order
                 WHERE customer_order.customer_id =
                     ( SELECT customer.id
                         FROM customer
                        WHERE customer.name = 'Marty' ) ),
              ( SELECT product.id
                  FROM product
                 WHERE product.name="Donnie's Fried Chicken and Shrimp" ),
              ( 1 ) );

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id
                  FROM customer_order
                 WHERE customer_order.customer_id =
                     ( SELECT customer.id
                         FROM customer
                        WHERE customer.name = 'Marty' ) ),
              ( SELECT product.id
                  FROM product
                 WHERE product.name='Thai Pale Ale' ),
              ( 1 ) );

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id 
                  FROM customer_order 
                 WHERE customer_order.customer_id = 
                     ( SELECT customer.id 
                         FROM customer 
                        WHERE customer.name = 'Pilan' ) ),
              ( SELECT product.id 
                  FROM product 
                 WHERE product.name='Pizza Rolls' ),
              ( 12 ) );

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id
                  FROM customer_order
                 WHERE customer_order.customer_id =
                     ( SELECT customer.id
                         FROM customer
                        WHERE customer.name = 'Pilan' ) ),
              ( SELECT product.id
                  FROM product
                 WHERE product.name='Thai Pale Ale' ),
              ( 1 ) );

INSERT INTO order_item ( customer_order_id, product_id, quantity )
     VALUES ( ( SELECT customer_order.id
                  FROM customer_order
                 WHERE customer_order.customer_id =
                     ( SELECT customer.id
                         FROM customer
                        WHERE customer.name = 'Rajneel' ) ),
              ( SELECT product.id
                  FROM product
                 WHERE product.name='Door Hangers' ),
              ( 10000 ) );

/* END DATABASE INITIALIZATION : example.db :: sqlite3              */
