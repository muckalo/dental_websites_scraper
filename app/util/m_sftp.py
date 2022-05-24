import paramiko
from stat import S_ISDIR, S_ISREG

from app.config.config import SFTP_HOSTNAME, SFTP_USERNAME, SFTP_PASSWORD


def upload_file_to_server(local_fp, remote_fp):
    transport = paramiko.Transport((SFTP_HOSTNAME, 22))
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.put(local_fp, remote_fp)

    sftp.close()
    transport.close()


def download_file_from_server(remote_folder_path, input_csv_file_name, local_fp):
    transport = paramiko.Transport((SFTP_HOSTNAME, 22))
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    for entry in sftp.listdir_attr(remote_folder_path):
        mode = entry.st_mode
        if S_ISREG(mode):
            file_name = entry.filename
            # print(entry.filename + " is file")
            if file_name == input_csv_file_name:
                remote_fp = '{}{}'.format(remote_folder_path, input_csv_file_name)
                sftp.get(remote_fp, local_fp)
                print('downloaded file')
    sftp.close()
    transport.close()
