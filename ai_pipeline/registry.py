class ModelRegistry:
    def __init__(self):
        self.models = {}
    def register(self, name: str, version: str, model_instance):
        self.models[f"{name}:{version}"] = model_instance
    def get(self, name: str, version: str = "latest"):
        matching = [k for k in self.models.keys() if k.startswith(f"{name}:")]
        return self.models[sorted(matching)[-1]] if matching else None

model_registry = ModelRegistry()
