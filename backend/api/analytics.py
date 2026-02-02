import pandas as pd
import os

def process_csv(file_path):
    """
    Reads a CSV file and returns summary statistics and data for visualization.
    """
    try:
        df = pd.read_csv(file_path)
        
        # specific columns required
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        if not all(col in df.columns for col in required_columns):
             return {"error": f"Missing columns. Required: {required_columns}"}

        # Summary Statistics
        stats = {
            "total_count": int(len(df)),
            "average_flowrate": float(df['Flowrate'].mean()),
            "average_pressure": float(df['Pressure'].mean()),
            "average_temperature": float(df['Temperature'].mean()),
        }

        # Type Distribution
        type_dist = df['Type'].value_counts().to_dict()
        
        # Data for charts (can be refined based on frontend needs)
        # For now, sending the raw data as records for the table
        data_records = df.to_dict(orient='records')

        return {
            "stats": stats,
            "type_distribution": type_dist,
            "data": data_records
        }

    except Exception as e:
        return {"error": str(e)}
