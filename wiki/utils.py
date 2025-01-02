from functools import wraps

from pydantic import BaseModel, TypeAdapter, ValidationError


def flatten_to_schema(model: BaseModel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_data = func(*args, **kwargs)

            def flatten(item):
                # Extract fields present in the model
                model_fields = model.model_fields.keys()
                return {
                    field: item.get(field, {}).get("value", None)
                    for field in model_fields
                }

            if isinstance(raw_data, list):
                # Flatten all items
                flattened_data = [flatten(item) for item in raw_data]

                # Prepare a TypeAdapter for a list of the model
                model_adapter = TypeAdapter(list[model])
                try:
                    # Batch validate all items
                    validated_models = model_adapter.validate_python(flattened_data)
                    # Convert validated models to dictionaries
                    return [model.model_dump() for model in validated_models]
                except ValidationError as e:
                    # Log batch validation errors
                    print(f"Batch validation error: {e}")
                    return []

            elif isinstance(raw_data, dict):
                # Single item validation
                flattened = flatten(raw_data)
                try:
                    validated_model = model.model_validate(flattened)
                    return validated_model.model_dump()
                except ValidationError as e:
                    print(f"Validation error for single item: {e}")
                    return None

            # If data is not a list or dict, return as is
            return raw_data

        return wrapper

    return decorator
