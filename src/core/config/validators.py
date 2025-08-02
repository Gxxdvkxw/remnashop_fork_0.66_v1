from pydantic import SecretStr
from pydantic_core.core_schema import FieldValidationInfo


def validate_not_change_me(value: object, info: FieldValidationInfo) -> None:
    if isinstance(value, SecretStr):
        value = value.get_secret_value()

    full_env_var_name = "UNKNOWN_FIELD"

    if info.config and hasattr(info.config, "get"):
        model_env_prefix = info.config.get("env_prefix", "")

        if isinstance(model_env_prefix, str):
            model_prefix_str = model_env_prefix.upper()
        else:
            model_prefix_str = ""

        if info.field_name:
            full_env_var_name = f"{model_prefix_str}{info.field_name.upper()}"
        else:
            full_env_var_name = "UNKNOWN_FIELD"

    if not value or str(value).strip().lower() in {"change_me", ""}:
        raise ValueError(f"{full_env_var_name} must be set and not equal to 'change_me'")
