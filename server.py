import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostbyname("")
port = 9003
server.bind((host, port))
server.listen(5)


clients = []
client_addrs = []

def accepting_connections():
    for client in clients:
        client.close()
    del clients[:]
    del client_addrs[:]
    while True:
        client, address = server.accept()
        clients.append(client)
        client_addrs.append(address)
        print("Client " + str(len(clients)) + " connected:" + address[0])

        if len(clients) == 3:
            quiz()
            break
        else:
            for c in clients:
                c.send(bytes("Waiting for other players to connect...\n", "utf-8"))


def sendtoall(msg):   # sends msg to all clients
    for client in clients:
        client.send(bytes(msg, "utf-8"))

def sendexcept(cli, msg):   # sends msg to all clients except specified client
    for c in clients:
        if c != cli:
            c.send(bytes(msg, "utf-8"))

def identify_client(c):    # identifies client number, given a client
    for i in range(len(clients)):
        if c == clients[i]:
            return i


questions = [
    " Which is the longest river on Earth?\n a.Amazon   b.Brahmaputra   c.Mississippi   d.Nile\n",
    " How many bones does an adult human have?\n a.207   b.206   c.208   d.205\n",
    " Which country is called the land of rising sun?\n a.Russia   b.India   c.Japan   d.China\n",
    " Which day is observed as World Environment Day?\n a.June 5   b.March 20   c.June 22   d.May 11\n",
    " How many days are there in a week?\n a.5   b.8   c.7   d.9\n",
    " Who is the author of the Harry Potter series of books?\n a.Agatha Christie   b.Harper Lee   c.Rick Riordan   d.J.K.Rowling\n",
    " Which is the longest bone in the human adult body?\n a.Femur   b.Stapes   c.Ulna   d.Sternum\n",
    " Which invented electricity?\n a.Benjamin Franklin   b.Thomas Edison   c.John Baird   d.James Watt\n",
    " Who is Thor?\n a.God of Nature   b.God of Thunder   c.God of Mischief   d.God of Death\n",
    " Who plays the role of Iron Man in the MCU?\n a.Robert Downey Jr.   b.Chris Evans   c.Tom Cruise   d.George Clooney\n",
    " What is a group of lions called?\n a.A school   b.A brood   c.A pride   d.A flock\n",
    " What is the name of Harry Potter's pet owl?\n a.Fluffy   b.Hedwig   c.Scabbers   d.Crookshanks\n",
    " How many consonants are there in the English alphabet?\n a.26   b.22   c.24   d.21\n",
    " Who painted the Mona Lisa?\n a.Rembrandt   b.Leonardo Da Vinci   c.Pablo Picasso   d.Raphael\n",
    " Which is the highest mountain on Earth?\n a.Kangchenjunga   b.Nanda Devi   c.Mt.Everest   d.K2\n",
    " Which city is the Statue of Liberty in?\n a.New York   b.Washington   c.Chicago   d.San Francisco\n",
    " Who wrote Hamlet and Macbeth?\n a.Mark Twain   b.Jane Austen   c.T.S.Eliot   d.William Shakespeare\n",
    " Which element does Fe represent?\n a.Sodium   b.Aluminium   c.Iron   d.Copper\n",
    " 5 + 6 = \n a.14   b.11   c.13   d.10\n",
    " Which infinity stone was in the Tesseract?\n a.Mind   b.Time   c.Space   d.Power\n",
    " 30 + 11 = \n a.41   b.69   c.59   d.51\n",
    " Which of the following is not a primary colour?\n a.Red   b.Blue   c.Yellow   d.Black\n",
    " Which is the longest grass?\n a.Palak   b.Pudhina   c.Bamboo   d.Dhaniya\n",
    " What is the full-form of SSD?\n a.Solid state drive   b.Solid storage drive   c.Super state drive   d.Super storage drive\n",
    " Who is the author of Marvel comics?\n a.Bruce Lee   b.Stan Lee   c.Harper Lee   d.Cooper Lee\n",
    " What is the Iron man's real name?\n a.Tony pork   b.Pony clark   c.Stony lark   d.Tony Stark\n",
    " 18/3 = \n a.2   b.3   c.9   d.6\n",
    " How many infinity stones were there?\n a.5   b.4   c.6   d.7\n",
    " 4 * 7 = \n a.24   b.21   c.28   d.35\n",
    " How many horcruxes did Lord Voldemort make?\n a.1   b.7   c.3   d.11\n",
    " What is Captain America's shield made of?\n a.Vibranium   b.Adamandium   c.Titanium   d.Ambuja Cement\n",
    " How many cameras does Galaxy S10 plus have in total?\n a.2   b.3   c.4   d.5\n",
    " How many states are there in India?\n a.29   b.28   c.30   d.31\n",
    " Which mythology features Thor?\n a.Greek   b.Indian   c.Eqyptian   d.Norse\n",
    " Who is Loki?\n a.God of Thunder   b.God of Dwarves   c.God of Mischief   d.God of Gods\n",
    " Who is the Prime Minister of India?\n a.Marendra Nodi   b.Gajendra Lodi   c.Ramprakash   d.Narendra Modi\n",
    " Who was one of the founders Apple Inc.?\n a.Steve Jobs   b.Adam and Eve   c.Stane Jobless   d.KRK\n",
    " Who is Holt's arch nemesis in Brooklyn Nine-Nine?\n a.Melissa Lunch   b.Madeline Wuntch   c.Jake Peralta   d.Norm Scully\n",
    " Who composed the Avengers theme song?\n a.Alan Silvestri   b.John Powell   c.A.R.Rehman   d.Prabhu Nidhish\n",
    " Who directed Avengers: Endgame?\n a.Russian brothers   b.Houdini brothers   c.Russo brothers   d.Stan Lee\n",
    " Who plays the role of Deadpool?\n a.Nicolas Cage   b.Hugh Jackman   c.Ryan Reynolds   d.Robert Downey\n",
    " What is Wolverine's claws composed of?\n a.Vibranium   b.Adamandium   c.Titanium   d.Ambuja Cement\n",
    " Who is Jake Peralta's criminal friend?\n a.Trudy Judy   b.Frank Judy   c.Doug Judy   d.Charles Boyle\n",
    " What cars does Doug Judy steal?\n a.Pontiacs   b.Maruti   c.Ford   d.Mahindra\n",
    " In which precint does Rosa Diaz work in?\n a.99   b.69   c.86   d.107\n",
    " Which pokemon does Ryan Reynolds voice in a particular Pokemon movie?\n a.Charmander   b.Squirtle   c.Pikachu   d.Bulbazor\n",
    " What is Lord Voldemort's real name?\n a.Tin-Tin   b.Tom Riddle   c.Tom Puzzle   d.Crossword Tom\n",
    " Which movie is Jake Peralta obsessed with?\n a.Pulp fiction   b.Die Hard   c.Inception   d.Ghost Rider\n",
    " Who is Harry Potter's godfather?\n a.Sirius Black   b.Sirius White   c.Silly Black   d.Silly White\n",
    " Who plays Batman in The Dark Knight?\n a.Hindu Whale   b.Muslim Gayle   c.Christian Bale   d.Jewish Pale\n"
]

answers = ['d', 'b', 'c', 'a', 'c', 'd', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'b', 'c', 'a', 'd', 'c', 'b', 'c', 'a', 'd', 'c', 'a', 'b',
           'd', 'd', 'c', 'c', 'b', 'a', 'd', 'b', 'd', 'c', 'd', 'a', 'b', 'a', 'c', 'c', 'b', 'c', 'a', 'a', 'c', 'b', 'b', 'a', 'c']

scores = [0, 0, 0]


def quiz():
    question_number = 0
    sendtoall("\nWelcome to QUIZ MASTERS.\n\n"
              "Rules:\n"
              "1. On receiving the question, each player is given 10 seconds to press the buzzer. \n"
              "2. The first one to press the buzzer gets a chance to provide the answer within 10 seconds.\n"
              "3. If the answer is correct, the player gets 1 point. Otherwise, the player gets -0.5. \n"
              "4. The first player to reach 5 points, wins the quiz.\n\n")

    while max(scores) < 5:
        print("\nRound " + str(question_number + 1) + ":")
        sendtoall("\nQuestion number: " + str(question_number + 1) + '\n')
        sendtoall(questions[question_number])

        sendtoall("\nPress enter key for buzzer.\n")
        readable, writable, exceptional = select.select(clients, [], [], 10)

        if readable:
            first_client = readable[0]
            client_number = identify_client(first_client)
            answering_client = [first_client]
            buzzer = first_client.recv(10)
            while buzzer == '\n':
                pass
            print("Player" + str(client_number + 1) + " pressed the buzzer first.")
            sendexcept(first_client, "   Player " + str(client_number + 1) + " pressed the buzzer first.\n")

            first_client.send(bytes("Enter correct option (in lower case and press enter key) :\n", "utf-8"))
            read, write, exception = select.select(answering_client, [], [], 10)
            if read:
                answer = first_client.recv(10)
                while answer == '\n':
                    pass

                answer = str(answer, 'utf-8')
                print("Player" + str(client_number + 1) + "'s answer: " + answer[0])
                if answer[0] == answers[question_number]:
                    scores[client_number] += 1
                    first_client.send(bytes("\n   Correct answer(+1). Your score:" + str(scores[client_number]) + "\n", "utf-8"))
                else:
                    scores[client_number] -= 0.5
                    first_client.send(bytes("\n   Wrong answer(-0.5). Your score:" + str(scores[client_number]) + "\n", "utf-8"))

            else:
                first_client.send(bytes("   Time up...\n", "utf-8"))

        else:
            sendtoall("\n   No player pressed the buzzer.\n\n")

        sendtoall("\n   Scores after round " + str(question_number + 1) +
                  ":\n   Player 1: " + str(scores[0]) +
                  "\n   Player 2: " + str(scores[1]) +
                  "\n   Player 3: " + str(scores[2]) + "\n\n")

        readable, writable, exceptional = select.select(clients, [], [], 0.25)
        while readable:
            c = readable[0]
            c.recv(10)
            readable, writable, exceptional = select.select(clients, [], [], 0.25)

        question_number += 1

        if question_number == 50:
            sendtoall("     GAME OVER!\n   There is no winner. " + "\n\n")
            print("\n     GAME OVER!\n   There is no winner. " + "\n\n")
            sendtoall("Exit")
            break

    if max(scores) >= 5:
        sendtoall("     GAME OVER!\n   The winner is Player " + str(scores.index(max(scores))+1) + "\n\n")
        print("\n     GAME OVER!\n   The winner is Player " + str(scores.index(max(scores))+1) + "\n\n")
        sendtoall("Exit")


accepting_connections()
