class AutoMESCConnector:
    def fetch(self):
        # Fetch raw data from AutoMESC source
        pass

    def parse(self, raw_data):
        # Parse AutoMESC data into intermediate format
        pass

    def run_pipeline(self):
        raw_data = self.fetch()
        parsed_data = self.parse(raw_data)
        return parsed_data
