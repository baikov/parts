from .ftp import connect_to_ftp, get_csv_from_ftp, close_ftp, get_data_from_csv
from parts.models import Part

def import_parts(filename):
    '''
    Create parts from local csv file
    '''
    data = get_data_from_csv(filename)
    for row in data:
        print(row)
        # _, created = Part.objects.get_or_create(
        #     vin = row[0],
        #     code = row[1],
        #     name = row[2],
        #     unit = row[3],
        #     count = row[4],
        #     )

def __main__ (self):
    import_parts()