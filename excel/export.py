import pandas as pd

def dict_to_excel(output_filename='output_data.xlsx'):
    # 1. Create your python dictionary
    # Nested structure: sheets -> trials -> data
    input_dict = {
        "Sheet1": {
            "trial_1": {"count": 3, "latencies": [0.5, 1.0, 1.5], "durations": [0.2, 0.3, 0.4]},
            "trial_4": {"count": 1, "latencies": [0.6], "durations": [0.2]},
            "trial_6": {"count": 0, "latencies": [], "durations": []}
        },
        "Sheet2": {
            "trial_2": {"count": 4, "latencies": [0.7, 1.2, 1.7, 1.5], "durations": [0.2, 0.3, 0.4, 0.5]},
            "trial_6": {"count": 3, "latencies": [0.8, 1.3, 1.8], "durations": [0.2, 0.3, 0.4]}
        }
    }

    print("Original Dictionary:")
    print(input_dict)
    print("-" * 30)

    # 3. Export to Excel file
    # Ensure you have 'openpyxl' installed (pip install openpyxl)
    
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        for sheet_name, behavior_data in input_dict.items():
            num_trials = len(behavior_data)
            # Find max lengths for latencies and durations
            max_latencies = max((len(v["latencies"]) for v in behavior_data.values()), default=0)
            max_durations = max((len(v["durations"]) for v in behavior_data.values()), default=0)
            
            # Row labels
            row_labels = [""] + ["count"] + \
                         [f"latency {i+1}" for i in range(max_latencies)] + \
                         [f"duration {i+1}" for i in range(max_durations)]
            
            # Data dict
            data = {}
            for trial_key, trial_data in behavior_data.items():
                trial_name = f"{trial_key} out of {num_trials}"
                count = trial_data["count"]
                latencies = trial_data["latencies"] + [""] * (max_latencies - len(trial_data["latencies"]))
                durations = trial_data["durations"] + [""] * (max_durations - len(trial_data["durations"]))
                data[trial_name] = [trial_key, count] + latencies + durations
            
            df = pd.DataFrame(data, index=row_labels)
            df.index.name = ""
            df.to_excel(writer, sheet_name=sheet_name, index=True)
            print(f"Sheet '{sheet_name}' DataFrame:")
            print(df)
            print("-" * 30)
    
    print(f"Successfully saved to {output_filename}!")    

if __name__ == "__main__":
    dict_to_excel()
