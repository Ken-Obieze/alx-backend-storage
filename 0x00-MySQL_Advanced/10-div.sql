-- SQL script that meets the following requirements:
-- Create a function SafeDiv
-- The function SafeDiv takes 2 arguments:
-- a (INT), b (INT)
-- Returns a / b or 0 if b == 0

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS INT
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END;

