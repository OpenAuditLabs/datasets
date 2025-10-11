from openauditbenchmark.schemas.schemas import UnifiedContractSchema
from pydantic import ValidationError

class SCBenchConnector:
    def fetch(self):
        # Fetch raw data from SC-Bench source
        # return raw_data
        pass

    def parse(self, raw_data):
        # Parse raw_data into intermediate format and validate against schema
        try:
            validated_data = UnifiedContractSchema(**raw_data)
            return validated_data.model_dump()
        except ValidationError as e:
            print(f"Schema validation error: {e.json()}")
            raise


    def run_pipeline(self):
        # Pipeline: fetch -> parse -> return parsed data
        raw_data = self.fetch()
        parsed_data = self.parse(raw_data)
        return parsed_data
