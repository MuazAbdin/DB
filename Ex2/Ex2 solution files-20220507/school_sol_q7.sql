select distinct year,name
from authors 
where institution='Hebrew University of Jerusalem' and conference='focs' and year>=2000 and year<=2020
except
select a2.year,a2.name
from authors a1, authors a2
where a1.institution='Hebrew University of Jerusalem' and a2.institution='Hebrew University of Jerusalem' and a1.conference='focs' and a2.conference='focs' and  a1.count>a2.count and a1.year=a2.year
order by year,name;
