from telnetlib import Telnet
from ssl import _create_stdlib_context

""" This file implement the TelnetMail class. """

# Datetime Format : Sat, 25 Dec 2021 05:35:23 -0000

# Importance : low, normal, hight
# Priority : non-urgent, normal, urgent
# Sensibility : Personal, Private, Company-Confidential


class TelnetMail:

    """ This class send plaintext email (not secure) with Telnet """

    def __init__(
        self,
        host: str,
        port: int = None,
        from_: str = None,
        to: list = None,
        message: str = None,
        ehlo: str = "SimpleTelnetMail",
        pseudo: str = "",
        ssl: bool = True,
        debug: int = 0,
        **kwargs,
    ):

        self.host = host

        if port:
            self.port = port
        elif ssl:
            self.port = 465
        else:
            self.port = 25

        self.ehlo = ehlo
        self.from_ = from_
        self.to = to
        self.message = message
        self.headers = kwargs
        self.responses = b""
        self.pseudo = pseudo
        self.ssl = ssl
        self.debug = debug

    def __repr__(self):
        return f"<TelnetMail : SERVER={self.host}:{self.port} COMPUTERNAME={self.ehlo} FROM={self.from_} TO={self.to} SSL={self.ssl}>"

    def __str__(self):
        string = (
            f"{self.host}:{self.port}\n\tEHLO {self.ehlo}\n\tMAIL FROM: {self.from_}"
        )
        for t in self.to:
            string += f"\n\tRCPT TO: {t}"

        message = self.message.replace("\n", "\n\t\t")
        string += f"\n\tDATA:\n\t\t{message}"

        return string + "\bQUIT"

    def end_message(self):

        """ This method add "END" characters to close the mail. """

        self.message += "\n.\n"

    def add_headers(self):

        """ This method add headers in mail. """

        headers_string = ""

        for key, value in self.headers.items():
            key = key.replace("_", "-")
            headers_string += f"{key}: {value}\n"

        self.message = headers_string + self.message

    def get_response(self, client, starttls=False):

        """ Get response and return True if request is accepted or False if isn't. """

        responses = client.read_some().split(b"\r\n")
        while responses[-1] != b"":
            new_responses = client.read_some().split(b"\r\n")
            responses[-1] += new_responses[0]
            responses += new_responses[1:]

        for response in responses[:-1]:
            # print(responses) # DEBUG
            self.responses += response + b"\r\n"
            if response[:3] == b"220":
                if starttls:
                    return 6
                code = self.ehlo_and_helo(client)
                if code == 1:
                    code = 0  # New connection initalised
            elif response[:3] == b"250":
                if response[3] == b"-":  # For EHLO multilines responses
                    code = 5
                code = 1  # OK
            elif response[0] == 51:  # Error 3xy
                code = 2
            elif response[0] == 52:  # Error 4xy
                code = 3
            elif response[0] == 53:  # Error 5xy
                code = 4
            else:  # UNKNOW : not in RFC
                code = 7

        if code == 5:  # For EHLO multilines responses
            code = self.get_response(client)
        return code

    def ehlo_and_helo(self, client):

        """ Send ehlo and helo message to initialize the mail connection. """

        client.write(f"EHLO {self.ehlo}\r\n".encode())
        self.get_response(client)
        client.write(f"HELO {self.ehlo}\r\n".encode())
        return self.get_response(client)

    def starttls(self, client):
        client.write("STARTTLS\r\n".encode())
        response = self.get_response(client, starttls=True)
        if response == 6:
            print("Start TLS")
            context = _create_stdlib_context()
            client.sock = context.wrap_socket(client.sock, server_hostname=self.host)
            self.ehlo_and_helo(client)
            return True
        return False

    def send_mail(self):

        """ This method send mail with Telnet. """

        self.add_headers()
        self.end_message()

        client = Telnet(self.host, port=self.port)
        client.set_debuglevel(self.debug)
        self.get_response(client)

        if self.ssl:
            if self.starttls(client):
                print("SMTP connection over TLS")
        client.write(f"MAIL FROM:{self.pseudo}<{self.from_}>\r\n".encode())
        self.get_response(client)

        for address in self.to:
            client.write(f"RCPT TO:<{address}>\r\n".encode())
            self.get_response(client)

        client.write("DATA\r\n".encode())
        self.get_response(client)
        client.write(f"{self.message}".encode())
        self.get_response(client)
        client.write("QUIT\r\n".encode())

        self.responses += client.read_all()


def simple_usage():
    client = TelnetMail(
        "my.server.com",
        from_="my.address@domain.com",
        to=["receiver@domain.com"],
        message="Secret and not secure email with Telnet.",
        ssl=False,
    )
    client.send_mail()

    print(repr(client))
    print(client)
    print(client.responses.decode())


def advanced_usage():
    client = TelnetMail(
        "my.server.com",
        port=587,
        from_="my.address@domain.com",
        to=["receiver1@domain.com", "receiver2@domain.com"],
        message="Secret and secure email with Telnet.",
        ehlo="H4CK3R",
        pseudo="Mr_X",
        ssl=True,
        debug=4,
        Subject="Secret Email",
        Date="Sat, 19 Dec 2020 01:02:03 -0000",
        MIME_Version="1.0",
        Encrypted="ROT13",
        Fake="Fake hearder",
        Sender="PSEUDO <test@free.fr>",
        Comments="My comment",
        Keywords="Email, Secret",
        Expires="Sat, 25 Dec 2021 05:35:23 -0000",
        Language="en-EN, it-IT",
        Importance="hight",
        Priority="urgent",
        Sensibility="Company-Confidential",
        From="PSEUDO <test@free.fr>",
        To="receiver1@domain.com,receiver2@domain.com",
        Content_Type="text/plain; charset=us-ascii",
        Content_Transfer_Encoding="quoted-printable",
    )
    client.send_mail()

    print(repr(client))
    print(client)
    print(client.responses.decode())


def main():
    from sys import argv
    from getopt import getopt

    help_ = False
    arguments = {
        "host": None,
        "from": None,
        "to": None,
        "message": None,
        "port": 25,
        "ehlo": "SimpleTelnetMail",
        "pseudo": " ",
        "debug": 0,
        "ssl": False,
    }
    headers = {}

    optlist, args = getopt(
        argv[1:],
        "H:p:f:t:e:m:P:d:s",
        [
            "host=",
            "port=",
            "from=",
            "to=",
            "ehlo=",
            "message=",
            "pseudo=",
            "debug=",
            "ssl",
        ],
    )

    print(optlist)
    print(args)

    for argument in optlist:
        if argument[0] == "--host" or argument[0] == "-H":
            client = TelnetMail(argument[1])
            arguments["host"] = argument[1]
        elif argument[0] == "--from" or argument[0] == "-f":
            arguments["from"] = argument[1]
        elif argument[0] == "--to" or argument[0] == "-t":
            arguments["to"] = argument[1]
        elif argument[0] == "--message" or argument[0] == "-m":
            arguments["message"] = argument[1]
        elif argument[0] == "--port" or argument[0] == "-p":
            try:
                arguments["port"] = int(argument[1])
            except ValueError:
                print(
                    "ArgumentError: --port value or -p value must be an integer. Port is set to 25."
                )
        elif argument[0] == "--ehlo" or argument[0] == "-e":
            arguments["ehlo"] = argument[1]
        elif argument[0] == "--pseudo" or argument[0] == "-p":
            arguments["pseudo"] = argument[1]
        elif argument[0] == "--ssl" or argument[0] == "-s":
            arguments["ssl"] = True
        elif argument[0] == "--debug" or argument[0] == "-d":
            try:
                arguments["debug"] = int(argument[1])
            except ValueError:
                print(
                    "ArgumentError: --debug value or -d value must be an integer. Debug is set to 0."
                )
        else:
            breakpoint()
            help_ = True
            break

    for argument in args:
        if "=" in argument:
            argument = argument.split("=", 1)
            headers[argument[0]] = argument[1]
        else:
            breakpoint()
            help_ = True
            break

    for presence in arguments.values():
        if presence is None:
            breakpoint()
            help_ = True
            break

    if help_:
        help()
        exit(1)

    client.port = arguments["port"]
    client.ehlo = arguments["ehlo"]
    client.from_ = arguments["from"]
    client.to = arguments["to"].split(",")
    client.message = arguments["message"]
    client.pseudo = arguments["pseudo"]
    client.debug = arguments["debug"]
    client.ssl = arguments["ssl"]
    client.headers = headers

    print("Sending the mail...")
    client.send_mail()
    print("Debugging : ")

    print(repr(client))
    print(client)
    print(client.responses.decode())


def help():
    print(
        """
SimpleTelnetMail (OPTIONS NOT NAMED) (OPTIONS) [ ARGUMENTS : <host> <from> <to> <message> ]

ARGUMENTS :
    --host=<smtp.server.com>            -H=<smtp.server.com>
    --from=<my.address@domain.com>      -f=<my.address@domain.com>
    --to=<receiver@domain.com>          -t=<receiver@domain.com>
    --message=<my email message>        -m=<my email message>

OPTIONS :
    --port=<port number : default=25>   -p=<port number : default=25>
    --pseudo=<pseudo : default=" ">     -P=<pseudo : default=" ">
    --debug=<debug level : default=0>   -d=<debug level : default=0>
    --ssl                               -s
    --ehlo=<my hostname : default=SimpleTelnetMail> -e=<my hostname : default=SimpleTelnetMail>

OPTIONS NOT NAMED :
    HeaderName=HeaderValue
    Examples :
        Subject="My Simple Subject !"
        Sender="PSEUDO <my.adress@domain.com>"
        Date="Sat, 25 Dec 2021 05:35:23 -0000"
"""
    )


if __name__ == "__main__":
    main()
