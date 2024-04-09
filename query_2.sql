select students.name as student, avg(grade) as AverageGrade, s.name as study
from grades
left join students on grades.student_id=students.id
left join groups as g on students.group_id=g.id
left join studyes as s on grades.study_id = s.id
where s.id = 4
group by students.name, s.name
order by avg(grade) desc
limit 1