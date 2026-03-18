-- INSERT INTO products
-- 	(
-- 		name,
-- 		price,
-- 		inventory
-- 	)
-- VALUES
-- 	(
-- 		'Tortilla',
-- 		4,
-- 		1000
-- 	);

-- INSERT INTO products
-- 	(
-- 		name,
-- 		price,
-- 		inventory
-- 	)
-- VALUES
-- 	(
-- 		'Laptop',
-- 		600,
-- 		25
-- 	),
-- 	(
-- 		'Bagpack',
-- 		75,
-- 		10
-- 	)
-- returning
-- 	*;

-- DELETE FROM
-- 	products
-- WHERE
-- 	id = 10;

-- DELETE FROM
-- 	products
-- WHERE
-- 	id = 12
-- returning
-- 	id, name;

-- DELETE FROM
-- 	products
-- WHERE
-- 	inventory = 0;


-- UPDATE
-- 	products
-- SET
-- 	name = 'Flour Tortilla',
-- 	price = 40,
-- 	created_at = NOW()
-- WHERE
-- 	id = 19
-- returning
-- 	*;

UPDATE
	products
SET
	is_sale = true
WHERE
	id > 15
returning
	*;