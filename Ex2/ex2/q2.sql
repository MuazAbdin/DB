select distinct institution, a.name
from authors a natural join institutions i
where country = 'il'
order by institution, a.name;