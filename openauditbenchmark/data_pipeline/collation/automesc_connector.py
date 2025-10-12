from openauditbenchmark.schemas.schemas import UnifiedContractSchema
from pydantic import ValidationError

class AutoMESCConnector:
    def fetch(self):
        # Fetch raw data from AutoMESC source
        pass

    def parse(self, raw_data):
        # Parse AutoMESC data into intermediate format and validate against schema
        try:
            validated_data = UnifiedContractSchema(**raw_data)
            return validated_data.model_dump()
        except ValidationError as e:
            print(f"Schema validation error: {e.json()}")
            raise


    def run_pipeline(self):
        raw_data = self.fetch()
        parsed_data = self.parse(raw_data)
        return parsed_data
