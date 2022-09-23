select distinct name
from authors natural join conferences
where area='systems'
except
select name
from authors natural join conferences
where year>=1990 or area!='systems'
order by name;
