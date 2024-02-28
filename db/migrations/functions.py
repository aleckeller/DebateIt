from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

update_leader_function_query = """
RETURNS TRIGGER AS $$
DECLARE
   incoming_debate_id INT;
   incoming_response_id INT;
BEGIN
    IF TG_OP = 'INSERT' THEN
        incoming_response_id := NEW.response_id;
    ELSIF TG_OP = 'DELETE' THEN
        incoming_response_id := OLD.response_id;
    END IF;

   SELECT rv.debate_id INTO incoming_debate_id
   FROM responses_view AS rv
   WHERE rv.id = incoming_response_id;

   RAISE NOTICE 'Debug message: Variable value = %', incoming_debate_id;

   UPDATE debate AS d
   SET leader_id = (
    SELECT
        CASE 
            WHEN COUNT(*) > 1 THEN NULL
            ELSE MAX(rv.created_by_id::varchar)::uuid
        END
    FROM responses_view rv
    WHERE rv.vote_difference = (SELECT MAX(rv.vote_difference) FROM responses_view rv WHERE rv.debate_id = incoming_debate_id)
    AND rv.debate_id = incoming_debate_id
   )
   WHERE d.id = incoming_debate_id;
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
