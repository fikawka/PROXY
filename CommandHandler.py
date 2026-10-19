import threading

import PingRequest
from PortScanner import PortScanner
from bot import ConnectionStarter
from independent_modules.ProxyChecker import ProxyChecker
from player import Player
from independent_modules.PlayerList import PlayerList
from server_packets.ChangeGameStatePacket import ChangeGameStatePacket
from server_packets.ChatMessagePacket import ChatMessagePacket
from server_packets.PositionAndLookPacket import PositionAndLookPacket

playerlist = PlayerList()
#proxycheck = ProxyChecker()
def handleCommand(gracz: Player.Player, command: str):
    print("handle command")
    words = command.split(" ")

    if command.startswith(",help"):
        gracz.sendPacket(ChatMessagePacket("Tutaj zobaczysz wszystkie dostępne komendy:", None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(",help -- Wyświetla wszystkie komendy", None, bold="true", color="blue",))
        gracz.sendPacket(ChatMessagePacket(",join (ip) (port) (nick)", None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(",joinbot (ip) (port) (nick) (SOCKS5/none)", None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(",gamemode (0/1 -- Zmienia tryb gry", None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(",quit - Rozlacza z serwera z ktorym aktualnie jestes polaczony", None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(message=",crash (metoda) (liczba pakietow) -- Crashuje serwer", sender=None, bold="true", color="blue",))
        gracz.sendPacket(ChatMessagePacket(",crashlist - Wyswietla metody crashowania", sender=None, bold="true", color="blue",))
        gracz.sendPacket(ChatMessagePacket(",ping (ip) (port) - Podaje response z pingu od serwera", sender=None, bold="true", color="blue", ))
        gracz.sendPacket(ChatMessagePacket(message=",portscan (ip) (min_port) (max_port) - Przeszukuje ip pod katem serwerow minecraft", sender=None, bold="true", color="blue", ))
        gracz.sendPacket(ChatMessagePacket(message=",bungee (on/off) (ign to copy UUID from) - Bungeecord spoofer", sender=None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(message=",checkproxy - Sprawdza ponownie proxies z pliku (moze spowodowac chwilowy lag proxy)", sender=None, bold="true", color="blue"))
    elif command.startswith(",crashlist"):
        gracz.sendPacket(ChatMessagePacket(message="Dostepne metody crashowania serwera:", sender=None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(message="nbt_book: Klasyczny crasher MC|Bedit", sender=None, bold="true", color="blue"))
        gracz.sendPacket(ChatMessagePacket(message="nbt1: MC|Bedit przepisany pod bypass Custompayloadfixera", sender=None, bold="true", color="blue"))

    elif command.startswith(",crash "):
        words = command.split(" ")
        if len(words) == 3 and words[2].isnumeric():
            packet_count = int(words[2])
            if words[1] == "nbt_book":
                thread = threading.Thread(target=gracz.joiner.crasher.book_crash, args=(gracz.joiner.socket, packet_count))
                thread.daemon = True
                #thread.start()
                gracz.joiner.crasher.book_crash(socket=gracz.joiner.socket, packet_count=packet_count)
                gracz.sendPacket(ChatMessagePacket(message="Proboje crashowac serwer...", sender=None,bold="true", color="green"))
            elif words[1] == "nbt1":
                gracz.joiner.crasher.nbt1_crash(socket=gracz.joiner.socket, packet_count=packet_count)
                gracz.sendPacket(ChatMessagePacket(message="Proboje crashowac serwer...", sender=None, bold="true", color="green"))
            elif words[1].lower() == "window_nbt":
                gracz.joiner.crasher.better_nbt(socket=gracz.joiner.socket, packet_count=packet_count)
                gracz.sendPacket(ChatMessagePacket(message="Proboje crashowac serwer...", sender=None, bold="true", color="green"))
            elif words[1] == "netty1":
                gracz.joiner.crasher.netty_varint(socket=gracz.joiner.socket, packet_count=packet_count)
                gracz.sendPacket(ChatMessagePacket(message="Proboje crashowac serwer...", sender=None, bold="true", color="green"))
            else:
                gracz.sendPacket(ChatMessagePacket(message="Nie ma takiej metody", sender=None, bold="true", color="red"))


        else:
            gracz.sendPacket(ChatMessagePacket(message="Poprawne uzycie: ,crash (metoda) (liczba pakietow)", sender=None, bold="true", color="red"))
    elif command.startswith(",gamemode"):
        words = command.split(" ")
        if len(words) == 2 and words[1] == 0 or 1:
            wartosc = float(words[1])
            gracz.easySendPacket(ChangeGameStatePacket(reason=3, value= wartosc))
            gracz.easySendPacket(ChatMessagePacket(f"Zmieniam gamemode na {wartosc}", None, bold="true", color="green"))
        else:
            gracz.sendPacket(ChatMessagePacket(message="Poprawne uzycie: ,bungeecord (on/off)", sender=None, bold="true",color="red"))
    elif command.startswith(",portscan"):
        words = command.split(" ")
        if len(words) == 4 and words[2].isnumeric() and words[3].isnumeric():
            portscanner = PortScanner(host=words[1], port_min = int(words[2]), port_max = int(words[3]), player=gracz)
            portscanner.runScanner()
        else:
            gracz.sendPacket(ChatMessagePacket("Poprawne uzycie ,portscan (ip) (port_min) (port_max)", sender=None, bold="true", color="red"))

    elif command.startswith(",ping"):
        words = command.split(" ")
        if len(words) == 3:
            result = PingRequest.pingServer(ip=words[1], port=int(words[2]))
            if result == 0:
                gracz.sendPacket(ChatMessagePacket(message="Nie udalo sie polaczyc z serwerem", sender=None, bold=True, color="red"))
            else:
                gracz.sendPacket(ChatMessagePacket(message=result, sender=None, bold=True, color="purple"))
        else:
            gracz.sendPacket(ChatMessagePacket(message="Poprawne uzycie: ,ping (ip) (port)", sender=None, bold="true", color="red"))
    elif command.startswith(",bungee"):
        words = command.split(" ")
        if len(words) == 2:
            if words[1].lower() == "off":
                gracz.bungee = False
                gracz.sendPacket(ChatMessagePacket(message="bungecord off", sender=None, bold="true", color="green"))
            elif words[1].lower() == "on":
                gracz.bungee = True
                gracz.sendPacket(ChatMessagePacket(message="bungecord on", sender=None, bold="true", color="green"))
        else:
            gracz.easySendPacket(ChatMessagePacket(message="Poprawne użycie: ,bungeecord (on/off)", sender=None, bold="true", color="red"))

    elif command.startswith(",checkproxy"):
        gracz.sendPacket(ChatMessagePacket(message="Rozpoczeto sprawdzanie proxies! to moze chwile potrwac...", sender=None, bold="true", color="green"))
        proxy_count = proxycheck.checkProxies()
        gracz.sendPacket(ChatMessagePacket(message=f"Sprawdzono proxies! Liczba dostepnych: {proxy_count}", sender=None, bold="true", color="green"))
    elif command.startswith(",join"):
        words = command.split(" ")
        if len(words) == 4 and words[2].isnumeric():
            gracz.easySendPacket(ChatMessagePacket(f"Laczenie z serwerem {words[1]}:{words[2]} ", None, bold="true", color="blue"))
            try:
                gracz.join_server(ip=words[1], port=int(words[2]), ign_on_server=words[3])
            except Exception as e:
                gracz.easySendPacket(ChatMessagePacket(message=f"BŁAD PODCZAS LACZENIA Z SERWEREM: {str(e)}", sender=None, bold="true", color="red"))

        else:
            gracz.easySendPacket(
                ChatMessagePacket(message="Poprawne użycie: ,join (ip) (port) (nick)", sender=None, bold="true", color="red"))
    elif command.startswith(",quit"):
        if gracz.player_state == gracz.player_states.CONNECTED_TO_EXTERNAL_SERVER:
            gracz.joiner.quit()
            gracz.easySendPacket(ChatMessagePacket(message="Disconnecting from server..", bold="blue", color="red", sender=None))
            return
            #gracz.disconnect_from_external()

        else:
            gracz.easySendPacket(
                ChatMessagePacket(message="Nie jestes polaczony z zadnym serwerem!", bold="true", color="red", sender=None))
    elif command.startswith(",joinbot"): # ",joinbot (ip) (port) (nick) (SOCKS5/none) (liczba)
        if len(words) == 6 and words[2].isnumeric() and words[4].lower() is "none" or "socks5" and words[5].isnumeric():
            ip = words[1]
            port = int(words[2])
            nick = words[3]
            proxy_type = words[4].lower()
            liczba = int(words[5])
            boty = {
                "ip": ip,
                "port": port,
                "nick": nick,
                "proxy_type": proxy_type,
                "amount": liczba
            }
            ConnectionStarter.startConnection(boty)
        else:
            gracz.sendPacket(ChatMessagePacket("Poprawne uzycie: ,joinbot (ip) (port) (nick) (SOCKS5/none)",sender=None, bold="true", color="red"))


    else:
        gracz.sendPacket(ChatMessagePacket(message="Nieznana komenda! ,help pokazuje komendy", sender=None, bold="true", color="red"))

