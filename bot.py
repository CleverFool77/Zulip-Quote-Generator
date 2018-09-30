import zulip
import pprint
from quote import quote_generator

pp = pprint.PrettyPrinter(indent=4)


class Bot():
    def __init__(self):
        self.client = zulip.Client(config_file="~/.zuliprc")
        self.subscribe()
        print("subscribed")

    def subscribe(self):
        stream_data = self.client.get_streams().get("streams")
        temp_dict = {}
        stream_list = []
        for data in stream_data:
            temp_dict["name"] = data.get("name")
            stream_list.append(temp_dict)

        result = self.client.add_subscriptions(stream_list)
        # pp.pprint(r)
        # pp.pprint(stream_data)

    def process(self, msg):
        words = msg.get('content').lower().split(" ")
        quote = "Invalid command"

        send_dict = {
            "type": "stream",
            "to": msg.get("display_recipient"),
            "subject": msg.get("subject"),
            "content": quote
        }
        if "quote" in words:
            try:
                num_quotes = int(words[3])
            except IndexError:
                num_quotes = 1
            for i in range(num_quotes):
                quote = quote_generator()
                send_dict["content"] = quote

                result = self.client.send_message(send_dict)
                pp.pprint(result)
        else:
            result = self.client.send_message(send_dict)     
        return


def main():
    bot = Bot()
    print("listening")
    bot.client.call_on_each_message(bot.process)


main()
