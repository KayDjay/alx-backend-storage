--  SQL script that creates a trigger that decreases in quantity.
DELIMITER $$
CREATE TRIGGER decrease
AFTER INSERT ON orders
FOR EACH ROW
	BEGIN
		UPDATE items
		SET quantity = quantity - NEW.number
		WHERE name = NEW.item_name;
	END;
$$
DELIMITER ;