from functools import wraps

from pydantic import BaseModel, ValidationError


def flatten_to_model(model: BaseModel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_data = func(*args, **kwargs)

            def flatten(item):
                try:
                    # Extract fields present in the model
                    model_fields = model.model_fields.keys()
                    flattened = {
                        field: item.get(field, {}).get("value", None)
                        for field in model_fields
                    }
                    # Validate with Pydantic model
                    validated = model.model_validate(flattened)
                    return validated.model_dump()
                except ValidationError as e:
                    # Log validation error
                    print(f"Validation error for item {item}: {e}")
                    return None

            # Process list or single dict
            if isinstance(raw_data, list):
                return [
                    result for item in raw_data if (result := flatten(item)) is not None
                ]
            elif isinstance(raw_data, dict):
                return flatten(raw_data)
            return raw_data

        return wrapper

    return decorator
