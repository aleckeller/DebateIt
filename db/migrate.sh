alembic_check=$(alembic check)

if [[ $alembic_check == *"New upgrade operations detected"* ]]; then
  alembic revision --autogenerate
  alembic upgrade heads
fi