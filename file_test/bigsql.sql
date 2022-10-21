show create table tb_entity_data

select qipu_id,display_name
from tb_entity_data
where data_json like '%"useBlockchain":true%'
and qipu_id not in (5278752631632101,6705003508842601,7359570840565901);