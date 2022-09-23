select distinct name
from authors a1
where not exists
                (select *
                from conferences natural join authors a2
                where a2.name='Noam Nisan' and area='ai' and 
                conference not in(select conference
                               from authors a3
                               where a3.name=a1.name
                               )
                )
order by name;
