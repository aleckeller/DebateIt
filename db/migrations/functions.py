from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

update_leader_function_query = """
RETURNS TRIGGER AS $$
DECLARE
   debate_id INT;
   response_id INT;
BEGIN
    IF TG_OP = 'INSERT' THEN
        response_id := NEW.response_id;
    ELSIF TG_OP = 'DELETE' THEN
        response_id := OLD.response_id;
    END IF;
   RAISE NOTICE 'Debug message: Variable value = %', debate_id;

   SELECT rv.debate_id INTO debate_id
   FROM responses_view AS rv
   WHERE rv.id = response_id;

   UPDATE debate AS d
   SET leader_id = (
       SELECT
           CASE
               WHEN COUNT(*) > 1 THEN NULL
               ELSE rv.created_by_id
           END
       FROM responses_view AS rv
       WHERE d.id = rv.debate_id
       GROUP BY rv.vote_difference, rv.created_by_id
       ORDER BY rv.vote_difference DESC
       LIMIT 1
   )
   WHERE d.id = debate_id;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

update_leader_function = PGFunction(
    schema="public",
    signature="update_leader_function()",
    definition=update_leader_function_query,
)

update_leader_on_vote_creation_trigger = PGTrigger(
    schema="public",
    signature="update_leader_on_vote_creation_trigger",
    on_entity="public.vote",
    is_constraint=False,
    definition="""
    AFTER INSERT OR DELETE ON vote
    FOR EACH ROW
    EXECUTE FUNCTION update_leader_function();
    """,
)
