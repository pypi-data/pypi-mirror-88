from firefox_profile import FirefoxProfile

# Note: most of the code from this module has been moved into the firefox_profile
# module, which is now a separate library.  This module/program is now kept as legacy
# and is deprecated in favor of firefox_profile.


__version__ = "0.1.3"


def get_firefox_urls(firefoxdir=os.path.expanduser("~/.mozilla/firefox")):
    for profile in FirefoxProfile.get_profiles(firefoxdir):
        recovery_data = profile.get_recovery_data()
        if recovery_data is None:
            continue
        for w, window in enumerate(recovery_data.windows):
            for t, tab in enumerate(window.tabs):
                yield profile.name, w, t, tab.url

def main():
    for p, w, t, url in get_firefox_urls():
        print("profile %s; window %d; tab %d: %s" % (p, w, t, url))


if __name__ == "__main__":
    main()
