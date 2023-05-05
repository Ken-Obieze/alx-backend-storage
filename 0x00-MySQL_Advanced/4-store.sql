-- creates a trigger to decreases the quantity of item after adding new order.
-- Quantity in the table items can be negative.

CREATE TRIGGER decrease_quantity_trigger
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  UPDATE items SET quantity = quantity - NEW.quantity WHERE id = NEW.item_id;
END;
