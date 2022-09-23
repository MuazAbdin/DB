select distinct institution, name
from (
     select name, conference, year, institution
    from authors a1 natural join institutions i
    where adjustedcount >= 2 and country = 'il'
    order by name, conference, year, institution
         ) as a natural join conferences
where area = 'ai' or subarea = 'db'
order by institution, name;