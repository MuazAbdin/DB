select distinct name
from authors
except
select distinct name
from authors natural join conferences
where year >= 1990 or area != 'systems'
order by name;