import os


"""
C H E C K   D O C K E R   I M A G E   T A G   N A M E   ! ! ! ! ! ! ! ! ! !
C H E C K   D O C K E R   I M A G E   T A G   N A M E   ! ! ! ! ! ! ! ! ! !
C H E C K   D O C K E R   I M A G E   T A G   N A M E   ! ! ! ! ! ! ! ! ! !
C H E C K   D O C K E R   I M A G E   T A G   N A M E   ! ! ! ! ! ! ! ! ! !
C H E C K   D O C K E R   I M A G E   T A G   N A M E   ! ! ! ! ! ! ! ! ! !
"""


def main():
    """ OS COMMAND """
    os_command = "sudo docker run -d -ti --rm -v /home/muckalo/dental_websites_scraper/docker_mnt:/mnt grcicsasa/dental:v7"
    os.system(os_command)


if __name__ == '__main__':
    main()
    # crontab command
    # @reboot sudo rm -rf /home/muckalo/dental_websites_scraper/docker_mnt/files/geckodriver_log.log ; /usr/bin/python3.6 /home/muckalo/dental_websites_scraper/start_scrapers.py > /home/muckalo/dental_websites_scraper/status.log 2>&1
