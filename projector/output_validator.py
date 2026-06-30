class OutputValidator:
    def validate(self, output: dict, config: dict) -> bool:
        errors = []
        for field in config.get("fields", []):
            path = field["path"]
            required = field.get("required", False)
            
            if required and (path not in output or output[path] is None):
                errors.append(f"Required field '{path}' is missing or null.")
                
            if path in output and output[path] is not None:
                expected_type = field.get("type")
                actual_value = output[path]
                
                if expected_type == "string" and not isinstance(actual_value, str):
                    errors.append(f"Field '{path}' expected string, got {type(actual_value).__name__}")
                elif expected_type == "string[]" and not (isinstance(actual_value, list) and all(isinstance(x, str) for x in actual_value)):
                    errors.append(f"Field '{path}' expected array of strings")
                elif expected_type == "number" and not isinstance(actual_value, (int, float)):
                    errors.append(f"Field '{path}' expected number, got {type(actual_value).__name__}")
                elif expected_type == "object" and not isinstance(actual_value, dict):
                    errors.append(f"Field '{path}' expected object, got {type(actual_value).__name__}")
                elif expected_type == "object[]" and not (isinstance(actual_value, list) and all(isinstance(x, dict) for x in actual_value)):
                    errors.append(f"Field '{path}' expected array of objects")
                    
        if errors:
            raise ValueError("Output validation failed: " + "; ".join(errors))
        return True
