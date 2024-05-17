import pandas as pd

def export_to_excel(data, filename):
    # Define the column names
    columns = ["Question", "Answer", "EmbeddingID", "EmbeddingModel", "GenerativeModel", "Context", "Time"]

    # Create a DataFrame from the new data
    df_new = pd.DataFrame(data, columns=columns)

    try:
        # Try to read the existing data
        df_existing = pd.read_excel(filename)

        # Append the new data
        df = pd.concat([df_existing, df_new], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, use the new data
        df = df_new

    # Write the DataFrame to the Excel file
    df.to_excel(filename, index=False)
