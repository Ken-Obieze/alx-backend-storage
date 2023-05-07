-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- That computes and store the average weighted score for a student


DROP procedure IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
  IN user_id INT
)
BEGIN
  DECLARE weighted_avg_score DECIMAL(10,2);
  DECLARE total_weight INT;
  SELECT SUM(score*weight) INTO weighted_avg_score, SUM(weight) INTO total_weight FROM corrections WHERE user_id = user_id;
  UPDATE users SET average_weighted_score = weighted_avg_score/total_weight WHERE id = user_id;

END //

DELIMITER ;

