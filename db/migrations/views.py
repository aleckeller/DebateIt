from alembic_utils.pg_view import PGView

debates_view_definition = """
        SELECT d.id, d.title, ARRAY_AGG(DISTINCT dc.name) as category_names,
        d.summary, d.picture_url, COUNT(r.id) as response_count,
        d.created_at, ucbi.username as created_by, ul.username as leader,
            (
                CASE
                    WHEN NOW() > d.end_at THEN 'Finished'
                    WHEN EXTRACT(DAY FROM d.end_at - NOW()) > 0 THEN
                        EXTRACT(DAY FROM d.end_at - NOW()) || 'd ' ||
                        EXTRACT(HOUR FROM d.end_at - NOW()) || 'h ' ||
                        EXTRACT(MINUTE FROM d.end_at - NOW()) || 'm'
                    WHEN EXTRACT(HOUR FROM d.end_at - NOW()) > 0 THEN
                        EXTRACT(HOUR FROM d.end_at - NOW()) || 'h ' ||
                        EXTRACT(MINUTE FROM d.end_at - NOW()) || 'm'
                    ELSE
                        EXTRACT(MINUTE FROM d.end_at - NOW()) || 'm'
                END
            ) AS end_at
        FROM debate d
        LEFT JOIN debate_debate_category_table ddct ON ddct.debate_id = d.id
        LEFT JOIN debate_category dc ON dc.id = ddct.debate_category_id
        LEFT JOIN response r ON r.debate_id = d.id
        LEFT JOIN "user" ucbi ON ucbi.id = d.created_by_id
        LEFT JOIN "user" ul ON ul.id = d.leader_id
        GROUP BY d.id, ucbi.username, ul.username
        ORDER BY d.id
                          """

debates_view = PGView(
    schema="public",
    signature="debates_view",
    definition=debates_view_definition,
)

responses_view_definition = """
        WITH vote_counts AS (
            SELECT
                v.response_id,
                SUM(CASE WHEN v.vote_type = 'agree' THEN 1 ELSE 0 END) AS agree_count,
                SUM(CASE WHEN v.vote_type = 'disagree' THEN 1 ELSE 0 END) AS disagree_count
            FROM vote v
            GROUP BY v.response_id
        )
        
        SELECT r.id, r.debate_id, r.body, ucbi.username as created_by, COALESCE(vc.agree_count, 0) as agree, 
        COALESCE(vc.disagree_count, 0) as disagree
        FROM response r
        JOIN "user" ucbi ON ucbi.id = r.created_by_id
        LEFT JOIN vote_counts vc ON vc.response_id = r.id
        ORDER BY r.id
                          """

responses_view = PGView(
    schema="public",
    signature="responses_view",
    definition=responses_view_definition,
)
