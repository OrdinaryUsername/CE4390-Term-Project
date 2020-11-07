import net_setup
import client
import server
import net_teardown

if __name__ == '__main__':
    net_setup.net_setup()
    client.client()
    server.server()
    net_teardown.net_teardown()