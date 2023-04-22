import os


def revert_to_client_mode():
    # Stop and disable hostapd and dnsmasq services
    os.system("sudo systemctl stop hostapd")
    os.system("sudo systemctl disable hostapd")
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo systemctl disable dnsmasq")

    # Restore original dhcpcd.conf file
    os.system("sudo cp /etc/dhcpcd.conf.orig /etc/dhcpcd.conf")
    print("Original dhcpcd.conf has been restored.")

    # Restore original hostapd.conf file
    os.system("sudo cp /etc/hostapd/hostapd.conf.orig /etc/hostapd/hostapd.conf")
    print("Original hostapd.conf has been restored.")

    # Restore original dnsmasq.conf file
    os.system("sudo cp /etc/dnsmasq.conf.orig /etc/dnsmasq.conf")
    print("Original dnsmasq.conf has been restored.")

    # Restart the dhcpcd service
    os.system("sudo systemctl restart dhcpcd")
    print("dhcpcd service has been restarted.")
    # Restore original hostapd.conf file


revert_to_client_mode()