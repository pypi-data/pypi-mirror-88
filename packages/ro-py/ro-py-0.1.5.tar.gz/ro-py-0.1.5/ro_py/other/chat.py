from ro_py.client import Client
from ro_py.notifications import NotificationReceiver
from sys import exit, stdout, stdin
import blessed

terminal = blessed.terminal.Terminal()

client = Client("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_002FEBFAB9FDB09EECDFDC40D797224CC18A4C3A4257CCA0FC7D20461D8E7232313A98F79C23BAA8FE7DA2FF1D465481AB6E36567C508472E7C5C510EF51A6C7503E0F8D1176D6141B65B4AC70705C1CB320173EF85F3A093C98D5E3F837B577B19A9F783C1E28FB042894EE728AC7338A3AAB7FC2CA1F999DB37FE35D39349E6B1DEAC33C4595BB7D4FCF68C6B43F2F881298B95F13353DAF4C2381646CCB44D7B2A6B0F3E8E69F8707DBFB799651A2D2515E2D02871E068E3A8E6369F6F1A27AA1AA47ECD28FA2C8C7B9D39835AB9703FED67D89FD06624D3932631A5E6E42B9FD280DF309D9AD509D46830F1421D944F467A0BEC6EDA5CB483C562466439927DA7578A2F007BE0D6DE64B235E63C09AD3DB9075D23839789444928EA1175709065B7D")
# conversation = Conversation(client.requests, "8585172596")

conversations = client.chat.get_conversations(1, 9)
options_text = ""
conversation_i = 1
for conversation in conversations:
    options_text = options_text + f"({conversation_i}) {conversation.title}\n"
    conversation_i += 1

stdout.write("Please choose from the following options:\n")
stdout.write(options_text)
option = stdin.readline()

try:
    option = int(option)
except ValueError:
    stdout.write("Invalid option.\n")
    exit()

try:
    conversation = conversations[option - 1]
except IndexError:
    stdout.write("Out of range.")
    exit()

stdout.write("Connecting...\n")


def message_event(evt_message):
    if evt_message.type == "NewMessage":
        if str(evt_message.data["conversation_id"]) == str(conversation.id):
            new_message_req = client.requests.get(
                url="https://chat.roblox.com/v2/multi-get-latest-messages",
                params={
                    "conversationIds": evt_message.data["conversation_id"],
                    "pageSize": "1"
                }
            )
            content = new_message_req.json()[0]["chatMessages"][0]["content"]
            message_sender = client.get_user(2067807455)
            stdout.write(message_sender.name + ": " + content + "\n")


receiver = NotificationReceiver(
    client.requests,
    lambda: print("Started"),
    lambda: print("Stopped"),
    lambda: print("Error"),
    message_event
)

stdout.write("Ready.\n")

while True:
    message = stdin.readline()
    message = message.replace("\n", "")
    conversation.send_message(message)
