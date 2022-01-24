import yamale

def validate(config_path: str, schema_path: str):
    yamale.validate(yamale.make_schema(schema_path), yamale.make_data(config_path))

