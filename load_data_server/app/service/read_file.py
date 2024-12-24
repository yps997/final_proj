import csv
def read_csv(csv_path: str):
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


terror_data_path1 = r"C:\Users\rozen\PycharmProjects\final_test\csv_to_db\app\data\merge.csv"














