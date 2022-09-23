select distinct institution,name
from conferences natural join authors natural join institutions
where country='il' and adjustedcount>=2 and (area='ai' or subarea='db')
order by institution,name;
