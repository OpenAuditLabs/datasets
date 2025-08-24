class AuditEngineConnector:
    def fetch(self):
        # Fetch raw data from audit engine
        pass

    def parse(self, raw_data):
        # Parse audit engine data into intermediate format
        pass

    def run_pipeline(self):
        raw_data = self.fetch()
        parsed_data = self.parse(raw_data)
        return parsed_data
