import sys
import gus.args as args
import gus.out as out
import gus.urls as urls


class Gus:
    def __init__(self, options):
        self.source = options.source
        self.wanted = options.wanted
        self.output = options.output
        self.ignore = options.ignore
        self.urlist = []
        self.get_url_status()

    def get_url_status(self):
        self.urlist = urls.get_list(self.source, self.ignore)
        self.urlist = urls.process_list(self.urlist, self.wanted, self.output)

    def tavo(self):
        send_results = out.to_rtf if self.output == "rtf" else out.to_console
        send_results(self.urlist, self.output)


def main():
    a = args.get_parsed()
    if a.source == "":
        sys.exit(0)
    gus = Gus(a)
    gus.tavo()


if __name__ == "__main__":
    main()
