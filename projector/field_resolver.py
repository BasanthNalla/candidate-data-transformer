class FieldResolver:
    def resolve(self, candidate, path: str):
        if not path:
            return None, False

        if "[]." in path:
            array_part, rest = path.split("[].", 1)
            array_val, found = self._resolve_simple(candidate, array_part)
            if not found or not isinstance(array_val, list):
                return None, False
            results = []
            for item in array_val:
                val, item_found = self._resolve_simple(item, rest)
                if item_found:
                    results.append(val)
            return results, True

        return self._resolve_simple(candidate, path)

    def _resolve_simple(self, obj, path: str):
        parts = path.split(".")
        current = obj
        for part in parts:
            if current is None:
                return None, False
            
            if "[" in part and part.endswith("]"):
                attr_name = part[:part.index("[")]
                idx_str = part[part.index("[")+1:-1]
                try:
                    idx = int(idx_str)
                except ValueError:
                    return None, False
                
                if attr_name:
                    if hasattr(current, attr_name):
                        current = getattr(current, attr_name)
                    elif isinstance(current, dict) and attr_name in current:
                        current = current[attr_name]
                    else:
                        return None, False
                
                if isinstance(current, list) and 0 <= idx < len(current):
                    current = current[idx]
                else:
                    return None, False
            else:
                if hasattr(current, part):
                    current = getattr(current, part)
                elif isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None, False
        return current, True
