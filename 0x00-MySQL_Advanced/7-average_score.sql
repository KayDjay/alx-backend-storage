-- Script to create a stored procedure ComputeAverageScoreForUser

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10,2);
    
    -- Compute average score
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;
    
    -- Update average score for the user
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END;
//

DELIMITER ;