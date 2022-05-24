import os
import time
# from datetime import datetime
import datetime

import googleapiclient.discovery

from app.util import query_data_from_psql, create_tables, insert_data_into_psql, get_current_utc_date_or_datetime, check_does_date_exist, get_current_utc_date_obj, add_days_to_date_obj, get_current_utc_datetime_obj, add_hours_to_datetime_obj


def current_datetime():
    return datetime.datetime.now()


def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def start_instance(compute, project, zone, name):
    return compute.instances().start(
        project=project,
        zone=zone,
        instance=name).execute()


def stop_instance(compute, project, zone, name):
    return compute.instances().stop(
        project=project,
        zone=zone,
        instance=name
    ).execute()


def create_db_and_tables_if_not_exists():
    """ Create db and table """
    sql = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        jobs_date DATE DEFAULT NULL UNIQUE,
        started BOOLEAN NOT NULL DEFAULT FALSE,
        finished BOOLEAN NOT NULL DEFAULT FALSE
    )
    """.format(table_name=table_name)
    create_tables(sql)


def insert_today_date():
    current_utc_date = get_current_utc_date_or_datetime(only_date=True)
    data_to_insert = {"jobs_date": current_utc_date}
    insert_data_into_psql('status', data_to_insert, 'jobs_date')


def insert_some_date(days):
    current_date_obj = datetime.datetime.utcnow().strptime(get_current_utc_date_or_datetime(only_date=True), "%Y-%m-%d")
    some_date_obj = current_date_obj + datetime.timedelta(days=days)
    # if days > 0:
    #     some_date_obj = current_date_obj + datetime.timedelta(days=3)
    # else:
    #     some_date_obj = current_date_obj - datetime.timedelta(days=3)
    data_to_insert = {"jobs_date": some_date_obj}
    insert_data_into_psql('status', data_to_insert, 'jobs_date')


def main(project, zone):
    create_db_and_tables_if_not_exists()

    compute = googleapiclient.discovery.build('compute', 'v1')

    """ List all instances """
    instances = list_instances(compute, project, zone)
    # print('instances: {}'.format(instances))

    for instance in instances:
        instance_name = instance["name"]
        instance_status = instance["status"]

        """ Skip if instance not for checking """
        if instance_name not in INSTANCE_LST:
            continue
        print('{} - {}'.format(instance_name, instance_status))

        """ Get or create date from DB so we know is job for that day started or not """
        # @TODO: Get or create date from new table in db
        # insert_some_date(-5)  # @TODO: DELETE AFTER TEST

        date_exist = check_does_date_exist(table_name)
        # If date not exists, insert today date (first run)
        if not date_exist or date_exist is None:
            print('date not exist')
            insert_today_date()
            date_exist = check_does_date_exist(table_name)
        # jobs_date = date_exist["jobs_date"]
        last_jobs_date = date_exist["jobs_date"]
        started = date_exist["started"]
        finished = date_exist["finished"]
        last_restart = date_exist["last_restart"]
        print('last_jobs_date: {} - started: {} - finished: {} - last_restart: {}'.format(last_jobs_date, started, finished, last_restart))
        current_date_obj = get_current_utc_date_obj()
        # print('current_date_obj: {} {}'.format(type(current_date_obj), current_date_obj))
        # Minus 1 day to give scrapers 2 days to finish job
        # current_date_obj_minus_one_day = add_days_to_date_obj(current_date_obj, -1)
        # print('current_date_obj_minus_one_day: {} {}'.format(type(current_date_obj_minus_one_day), current_date_obj_minus_one_day))
        # Insert today date to db table "status"
        if last_jobs_date < current_date_obj:
            # if last_jobs_date < current_date_obj_minus_one_day:
            print('inserting new date')
            insert_today_date()
            date_exist = check_does_date_exist(table_name)
        last_jobs_date = date_exist["jobs_date"]
        started = date_exist["started"]
        finished = date_exist["finished"]
        last_restart = date_exist["last_restart"]
        print('last_jobs_date: {} - started: {} - finished: {} - last_restart: {}'.format(last_jobs_date, started, finished, last_restart))

        current_utd_datetime = get_current_utc_datetime_obj()
        current_utd_datetime_minus_one_hour = add_hours_to_datetime_obj(current_utd_datetime, -1)

        """
        instance_status == "TERMINATED" AND finished = False -> turn on vm
        instance_status == "RUNNING" AND finished = True -> turn off vm
        """
        if instance_status == "TERMINATED" and not finished:
            print('Staring instance')
            """ OS COMMAND """
            os_command = "gcloud compute instances start {instance_name} --zone={instance_zone}".format(
                instance_name=instance_name, instance_zone=gcloud_zone
            )
            os.system(os_command)
        elif instance_status == "RUNNING" and finished:
            print('Shutting down instance')
            """ OS COMMAND """
            os_command = "gcloud compute instances stop {instance_name} --zone={instance_zone}".format(
                instance_name=instance_name, instance_zone=gcloud_zone
            )
            os.system(os_command)
        # elif last_restart < current_utd_datetime_minus_one_hour:
        #     if instance_status == "TERMINATED":
        #         print('Restarting instance (start)')
        #         """ OS COMMAND """
        #         os_command = "gcloud compute instances start {instance_name} --zone={instance_zone}".format(
        #             instance_name=instance_name, instance_zone=gcloud_zone
        #         )
        #         os.system(os_command)
        #     else:
        #         print('Restarting instance (start)')
        #         """ OS COMMAND """
        #         os_command = "gcloud compute instances reset {instance_name} --zone={instance_zone}".format(
        #             instance_name=instance_name, instance_zone=gcloud_zone
        #         )
        #         os.system(os_command)


table_name = "status"

INSTANCE_LST = [
    'instance-scraping-dental-supply-2'
]


if __name__ == '__main__':
    # GOOGLE_APPLICATION_CREDENTIALS = "/home/muckalo/PycharmProjects/Projects/Nikunj/dental/app/monitor/dental-supply-scraping-2bb87a52c1a6.json"  # LOCAL
    GOOGLE_APPLICATION_CREDENTIALS = "/home/muckalo/monitor_scrapers/dental-supply-scraping-2bb87a52c1a6.json"  # DOCKER
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

    gcloud_project_id = 'dental-supply-scraping'
    gcloud_zone = 'europe-west2-a'

    main(gcloud_project_id, gcloud_zone)

    current_local_datetime = current_datetime()
    print('current_local_datetime: {}'.format(current_local_datetime))
    print('-' * 50)

    del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
