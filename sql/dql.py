queries = {
    "hired_employees_summary": """
        SELECT 
            d.department,
            j.job,
            COUNT(CASE WHEN EXTRACT(quarter FROM he.datetime) = 1 THEN 1 END) AS Q1,
            COUNT(CASE WHEN EXTRACT(quarter FROM he.datetime) = 2 THEN 1 END) AS Q2,
            COUNT(CASE WHEN EXTRACT(quarter FROM he.datetime) = 3 THEN 1 END) AS Q3,
            COUNT(CASE WHEN EXTRACT(quarter FROM he.datetime) = 4 THEN 1 END) AS Q4
        FROM 
            public.hired_employees he
        JOIN
            departments d 
            ON he.department_id = d.id
        JOIN 
            jobs j 
            ON he.job_id = j.id
        WHERE 
            CAST(EXTRACT(year FROM he.datetime) AS INT) = 2021
        GROUP BY 
            d.department, 
            j.job
        ORDER BY 
            d.department DESC, 
            j.job DESC;
    """,
    "hired_by_department": """
        WITH total_hired_per_department AS (
            SELECT 
                d.id AS department_id,
                d.department,
                COUNT(*) AS total_hired
            FROM 
                public.hired_employees he
            JOIN 
                departments d 
                ON he.department_id = d.id
            WHERE 
                CAST(EXTRACT(year FROM he.datetime) AS INT) = 2021
            GROUP BY 
                d.id, d.department
        ),
        average_hired AS (
            SELECT 
                AVG(total_hired) AS avg_hired
            FROM 
                total_hired_per_department
        )
        SELECT 
            thpd.department_id AS id,
            thpd.department,
            thpd.total_hired AS hired
        FROM 
            total_hired_per_department thpd,
            average_hired ah
        WHERE 
            thpd.total_hired > ah.avg_hired
        ORDER BY 
            thpd.total_hired DESC;
        
    """
}