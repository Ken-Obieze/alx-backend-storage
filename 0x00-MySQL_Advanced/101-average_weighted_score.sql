-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- That computes and store the average weighted score for all students

DROP procedure IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE user_id INT;
  DECLARE weighted_avg_score DECIMAL(10,2);
  DECLARE total_weight INT;
  DECLARE cur_users CURSOR FOR SELECT id FROM users;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  OPEN cur_users;
  repeat
    FETCH cur_users INTO user_id;
    IF NOT done THEN
      SELECT SUM(score*weight) INTO weighted_avg_score, SUM(weight) INTO total_weight FROM corrections WHERE user_id = user_id;
      UPDATE users SET average_weighted_score = weighted_avg_score/total_weight WHERE id = user_id;
    END IF;
  until done END REPEAT;
  CLOSE cur_users;

END //

DELIMITER ;
