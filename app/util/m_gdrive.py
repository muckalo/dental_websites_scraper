from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def download_file_from_gdrive(folder_id, input_csv_file_name, output_fp, settings_fp):
    """ DOWNLOAD FILE FROM GDRIVE """

    """ AUTHENTICATE"""
    # gauth = GoogleAuth()
    gauth = GoogleAuth(settings_file=settings_fp)
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    """ LIST ALL FILES IN DRIVE """
    file_list = drive.ListFile({'q': "'{folder_id}' in parents and trashed=false".format(folder_id=folder_id)}).GetList()
    for file in file_list:
        title = file['title']
        if title != input_csv_file_name:
            continue
        file.GetContentFile(output_fp)


"""
EXAMPLE OF USAGE:

folder_id_ex = '1VJspfj_8HqDWSq0udmdgZ3umHnL8Ic0q'
input_csv_file_name_ex = 'input_CSV.csv'
output_fp_ex = 'files/input_CSV.csv'
setting_fp = 'files/cred/settings.yaml'
download_file_from_gdrive(folder_id_ex, input_csv_file_name_ex, output_fp_ex, setting_fp)
"""
