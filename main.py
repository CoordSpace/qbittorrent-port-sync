from qbittorrentapi import Client
from vyper import v
import schedule
import logging
from time import sleep

def init() -> None:
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

    logging.info("Setting config defaults.")
    v.set_default('host_source', 'client1.host.tld')
    v.set_default('port_source', '443')
    v.set_default('username_source', 'admin')
    v.set_default('password_source', 'adminadmin')

    v.set_default('host_dest', 'client2.host.tld')
    v.set_default('port_dest', '443')
    v.set_default('username_dest', 'admin')
    v.set_default('password_dest', 'adminadmin')

    logging.info("Reading config from file (if present).")
    v.set_config_name('config')
    v.set_config_type('yaml')
    v.add_config_path('.')
    v.add_config_path('/config')
    v.read_in_config()

def get_port() -> int:
    logging.info("Getting current port from the source qbit client.")
    source = Client(v.get_string("host_source"),
                    v.get_int("port_source"),
                    v.get_string("username_source"),
                    v.get_string("password_source"),
                    REQUESTS_ARGS={'timeout': (3.1, 5)},
                    SIMPLE_RESPONSES=True)
    port = source.application.preferences["listen_port"]    
    logging.info("Current source client port: {0}".format(port))
    return port


def set_port() -> None:
    logging.info("Starting set port...")
    port = get_port()
    dest = Client(v.get_string("host_dest"),
                    v.get_int("port_dest"),
                    v.get_string("username_dest"),
                    v.get_string("password_dest"),
                    REQUESTS_ARGS={'timeout': (3.1, 5)},
                    SIMPLE_RESPONSES=True)

    prev_port = dest.application.preferences["listen_port"]
    logging.info("Destination client previous port (before update): {0}".format(prev_port))
    dest.app_set_preferences({"listen_port": port})
    logging.info("Sleeping for a bit to let the port update sync...")
    sleep(5)
    current_port = int(dest.application.preferences["listen_port"])
    logging.info("Destination client current port (after update): {0}".format(current_port))
    if current_port == port:
        logging.info("Port synced successfully.")
    else:
        logging.error("Port did not update!")
    return False

def main() -> None:
    init()

    schedule.every(1).days.do(set_port)

    set_port()

    while True:
        n = schedule.idle_seconds()
        if n is None:
            logging.error("No outstanding jobs in the schedule!")
            break
        elif n > 0:
            logging.info("Sleeping {0} seconds till next job...".format(n))
            sleep(n)
        schedule.run_pending()
    logging.info("Infinite loop escaped. Program exiting..")

if __name__ == '__main__':
    main()
