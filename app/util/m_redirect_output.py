from app.util import create_folder_if_not_exists


def redirect_output(script_name, msg):
    output_folder_path = '/mnt/files/thread_logs/'
    create_folder_if_not_exists(output_folder_path)
    fp = "{}{}.log".format(output_folder_path, script_name)
    with open(fp, 'a') as f:
        print(msg, file=f)
    print(msg)
