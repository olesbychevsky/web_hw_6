SELECT s.name AS student, avg(grade) AS AverageGrade
FROM grades AS g
JOIN students AS s ON g.student_id = s.id
GROUP BY s.name
ORDER BY avg(grade) DESC
LIMIT 5