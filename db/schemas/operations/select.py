from sqlalchemy import select, and_, not_, or_, func

from db import constants
from db import types
from db.utils import get_pg_catalog_table

TYPES_SCHEMA = types.base.SCHEMA
TEMP_INFER_SCHEMA = constants.INFERENCE_SCHEMA
EXCLUDED_SCHEMATA = [TYPES_SCHEMA, TEMP_INFER_SCHEMA, "information_schema"]


def reflect_schema(engine, name=None, oid=None):
    # If we have both arguments, the behavior is undefined.
    try:
        assert name is None or oid is None
    except AssertionError as e:
        raise e
    pg_namespace = get_pg_catalog_table("pg_namespace", engine)
    sel = (
        select(pg_namespace.c.oid, pg_namespace.c.nspname.label("name"))
        .where(or_(pg_namespace.c.nspname == name, pg_namespace.c.oid == oid))
    )
    with engine.begin() as conn:
        schema_info = conn.execute(sel).fetchone()
    return schema_info


def get_mathesar_schemas_with_oids(engine):
    pg_namespace = get_pg_catalog_table("pg_namespace", engine)
    sel = (
        select(pg_namespace.c.nspname.label('schema'), pg_namespace.c.oid)
        .where(
            and_(
                *[pg_namespace.c.nspname != schema for schema in EXCLUDED_SCHEMATA],
                not_(pg_namespace.c.nspname.like("pg_%"))
            )
        )
    )
    with engine.begin() as conn:
        result = conn.execute(sel).fetchall()
    return result


def get_schema_description(oid, engine):
    with engine.begin() as conn:
        res = conn.execute(select(func.obj_description(oid, 'pg_namespace')))

    return res.fetchone()[0]
