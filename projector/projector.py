from projector.field_resolver import FieldResolver

class Projector:
    def __init__(self, config: dict):
        self.config = config
        self.resolver = FieldResolver()

    def project(self, candidate) -> dict:
        result = {}
        fields = self.config.get("fields", [])
        on_missing = self.config.get("on_missing", "null")
        
        for field in fields:
            output_path = field["path"]
            source_path = field.get("from", output_path)
            
            value, found = self.resolver.resolve(candidate, source_path)
            
            if hasattr(value, "model_dump"):
                value = value.model_dump()
            elif isinstance(value, list):
                value = [v.model_dump() if hasattr(v, "model_dump") else v for v in value]

            if not found or value is None or (isinstance(value, list) and len(value) == 0):
                if on_missing == "omit":
                    continue
                elif on_missing == "error":
                    raise ValueError(f"Required field missing: {source_path}")
                else:
                    value = None
            else:
                normalize_type = field.get("normalize")
                if normalize_type:
                    value = self._apply_normalize(value, normalize_type)
            
            result[output_path] = value
            
        if self.config.get("include_confidence", False):
            result["overall_confidence"] = candidate.overall_confidence
            
        if self.config.get("include_provenance", False):
            result["provenance"] = [{k: v for k, v in p.model_dump().items() if k != "value"} for p in candidate.provenance]
            
        return result

    def _apply_normalize(self, value, normalize_type: str):
        if isinstance(value, list):
            return [self._apply_normalize(v, normalize_type) for v in value]
        
        if normalize_type == "E164":
            from normalizers.phone_normalizer import normalize_phone
            return normalize_phone(str(value))
        elif normalize_type == "canonical":
            from normalizers.skill_normalizer import normalize_skill
            return normalize_skill(str(value))
        elif normalize_type == "lowercase":
            return str(value).lower()
        return value
