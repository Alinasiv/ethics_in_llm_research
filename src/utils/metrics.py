import csv
import os
from typing import Dict, List, Any

class MetricsTracker:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.attempts: int = 0
        self.successes: int = 0
        self.response_times: List[float] = []
        

    def save(self):
        os.makedirs(self.output_dir, exist_ok=True)
        
        with open(os.path.join(self.output_dir, "attack_metrics.csv"), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Attempts", self.attempts])
            writer.writerow(["Successful Leaks", self.successes])
            writer.writerow(["Success Rate", f"{(self.successes / self.attempts * 100) if self.attempts > 0 else 0:.2f}%"])
            writer.writerow(["Average Response Time", f"{sum(self.response_times) / len(self.response_times) if self.response_times else 0:.2f} sec"])

