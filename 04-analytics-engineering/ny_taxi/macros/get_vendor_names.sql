{% macro get_vendor_names(vendor_id) -%}
case {{ vendor_id }}
    when 1 then 'Creative Mobile Technologies'
    when 2 then 'VeriFone Inc.'
    when 4 then 'Digital Dispatch Systems'
    when 5 then 'Sigmet'
    when 6 then 'Mobile Knowledge'
    else 'Unknown'
end 
{% endmacro %}