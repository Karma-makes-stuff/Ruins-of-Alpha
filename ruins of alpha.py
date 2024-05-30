print('''Welcome to the ruins of Alpha.
This is a short text-adventure dungeon crawler.
You are an adventurer who goes on a quest for glory (and loot) in the
*Ruins of Alpha*
As you enter into the dungeon, you are greated by an angry bat.
The bat charges at you in a blind rage!
''')
#initializes the game:
gameover=False
bozo=True #so the player doesn't skit their turn when they make an invalid input
incombat=True #determies item function
health=100
atk=10
enemyhp=0
enemyatk=0
inventory=['back','bread'] #other items see line 398-603
armor=0 
status=0 #0..healthy, 1..poison, 2..bleed, 3..idk
key=False
first_r1=True
first_r2=True
first_r4=True
first_r5=True
first_r6=True
room=0

def combatitem(): #selection of items in combat
    global inventory
    global enemyhp
    global health
    global bozo
    print('which item?')
    i=0
    for items in inventory:
        i=i+1
        print(i,items)
    LL=True
    while LL:
        try:
            item=int(input())-1
            match inventory[item]:
                case 'back':
                    bozo=True
                    break
                case 'bread':
                    bread()
                    break
                case 'shuriken':
                    shuriken()
                    break
                case 'red potion':
                    red_potion()
                    break
                case 'antidote':
                    antidote()
                    break
                case 'blue potion':
                    blue_potion()
                    break
                case 'bandages':
                    bandages()
                    break
        except IndexError:
            print('This Item does not exist.\nWhich item?')      
def combat(enemy): #the combat loop
    global health
    global atk
    global armor
    global bozo
    global incombat
    incombat=True
    global status
    global enemyhp
    global enemyatk
    turncount=1
    L=True
    while L:
        bozo=False
        guard=False
        dmg=0
        try:
            action=int(input('what do you do?\n 1 attack\n 2 item\n 3 guard \n 4 observe\n'))
            match action:
                case 1:
                    enemyhp=enemyhp-atk
                    print('You deal',atk,'damage to the',enemy,'.')
                    if enemyhp<=0:
                        break
                case 2:
                    combatitem()
                    if enemyhp<=0:
                        break
                case 3:
                    guard=True
                case 4:
                    healthcheck()
                    print('The',enemy,'seems to have',enemyhp,'health left.')
                case _:
                    print('please input a valid number!')
                    bozo=True
        except ValueError:
            print('Your input must be an integer(a whole number)')
            bozo=True
        if bozo==False:
            if enemyhp<=0:
                break
            match enemy:
                case 'bat':
                    print('The bat attacks!')
                    dmg=enemyatk-armor
                    if guard==True:
                        health=health-(dmg//3)
                        print('You took',(dmg//3),'damage.')
                    else:
                        health=health-dmg
                        print('You took',dmg,'damage.')
                case 'skeleton':
                    if turncount!=2:
                        print('The skeleton attacks!')
                        dmg=enemyatk-armor
                        if guard==True:
                            health=health-(dmg//3)                       
                            if turncount==3:
                                print("You took",(dmg//3),"damage, but you avoided the worst.")
                            else:
                                print('You took',(dmg//3),'damage.')
                        else:
                            health=health-dmg
                            print('You took',dmg,'damage.')
                            if turncount==3:
                                print('You took',dmg,'damage!')
                                print('The liquid sinks deep into your fresh wound.')
                                status=1
                    if turncount==2:
                        print('The skeleton pours suspicious liquid on its weapon.')
                case 'spider':
                    print('The spider attacks!')
                    dmg=enemyatk-armor
                    if guard==True:
                        health=health-(dmg//3)
                        print('You took',(dmg//3),'damage.')
                    else:
                        health=health-dmg
                        print('You took',dmg,'damage.')
                case 'ghoul':
                    if turncount%3==0:
                        enemyatk=40
                    else:
                        enemyatk=20
                    if (turncount+1)%3==0:
                        print('The ghoul looks at you with wide eyes.')
                    else:
                        print('The ghoul claws at you!')
                        dmg=enemyatk-armor
                        if guard==True:
                            health=health-(dmg//3)
                            print('You took',(dmg//3),'damage.')
                            if turncount%3==0:
                                print("The hit still hurts, but you avoided the worst.")
                        else:
                            health=health-dmg
                            print('You took',dmg,'damage.')
                            if turncount%3==0:
                                print("The ghoul's bite tore a chunk of flesh out.")
                                status=2        
                case'vampire':
                    if turncount==1:
                        print('The vampire slashes you!')
                        dmg=(enemyatk-armor)
                        if guard==True:
                            health=health-(dmg//3)
                            print('You took',(dmg//3),'damage.')
                        else:
                            health=health-dmg
                            print('You took',dmg,'damage.')
                        
                    elif turncount%3==0:
                        print('The vampire fixes you with its gaze!')
                    elif (turncount-1)%3==0:
                        if guard==True:
                            dmg=enemyatk+5-armor
                            health=health-(dmg//3)
                            print("The hit still hurts, but you avoided the worst.")
                        else:
                            dmg=enemyatk+5-armor
                            health=health-dmg
                            status=2
                            print('You took',dmg,'damage')
                            print("The vampire's bite left a bleeding wound!")
                    else:
                        print('The vampire slashes you!')
                        dmg=enemyatk-armor
                        if guard==True:
                            health=health-(dmg//3)
                            print('You took',(dmg//3),'damage.')
                        else:
                            health=health-dmg
                            print('You took',dmg,'damage.')
                case _:
                    print('The ',enemy,'? attacks!')
                    dmg=enemyatk-armor
                    if guard==True:
                        health=health-(dmg//2)
                        print('You took',(dmg//2),'damage.')
                    else:
                        health=health-dmg
                        print('You took',dmg,'damage.')
            if status==1:
                health=health-turncount
                print("You feel like you're rotting from the inside!")
            if status==2:
                health=health-(dmg//3)
                print("Blood is dripping from your wounds!")
            turncount+=1
        if enemyhp<=0:
            break
        if turncount==25:
            break
        if health<=0:
            break
    if enemyhp<=0:
        print(enemy,'was defeated.')
    elif turncount==25:
        print(enemy,'grew bored and let you go.')
    else:
        print('You were slain by',enemy)
    incombat=False
def gameovercheck(): #checks for gameover
    global health
    global gameover
    if health<=0:
        gameover=True
def win(): #ends the game
    global gameover
    gameover=True
    global room
    room=7
    print('''Congratulations, you made it out of the Ruins of Alpha alive (and without crashing the game).
With loot in your pockets (and blood on your hands) you can now retire and tell your grandchildren the story
of how you heroically conquered the Ruins of Alpha for honor, glory, and your financial gain.
          
Thanks for playing!
''')
def encounter(): #encounter text
    global health
    global atk
    global enemy
    global enemyhp
    global enemyatk
    print('You encountered a',enemy,'!')
    if (health*atk)>(enemyhp*enemyatk*4):
        print('You feel confident in your ability to take on the',enemy,'.')
    elif (health*atk*2)<(enemyhp*enemyatk):
        print('The',enemy,'looks a lot stronger than you.')
    elif (health*atk*3)<(enemyhp*enemyatk):
        print('You tremble in the presence of such a foe.')
    else:
        print('You appear to be evenly matched.')
def enemystats(): #stores stats of different enemies
    global enemyhp
    global enemyatk
    global enemy

    #this could probably be replaced by a dict (maybe a global one)
    match enemy:
        case 'bat':
            enemyhp=20
            enemyatk=5
        case 'skeleton':
            enemyhp=45
            enemyatk=6
        case 'spider':
            enemyhp=25
            enemyatk=10
        case 'ghoul':
            enemyhp=125
            enemyatk=20
        case 'vampire':
            enemyhp=240
            enemyatk=30
        case 'MissingNo.':        
            enemyhp=33
            enemyatk=136
        case _:
            enemyhp=45
            enemyatk=7
def restitem(): #selection of items outside of combat
    LLLL=True
    while LLLL:
        inventory[0]='done'
        print('which item?')
        i=0
        for items in inventory:
            i=i+1
            print(i,items)
        LLL=True
        while LLL:
            try:
                item=int(input())-1
                match inventory[item]:
                    case 'done':
                        print("You're done here.")
                        LLLL=False
                        inventory[0]='back'
                        break
                    case 'bread':
                        bread()
                        break
                    case 'shuriken':
                        shuriken()
                        break
                    case 'red potion':
                        red_potion()
                        break
                    case 'antidote':
                        antidote()
                        break
                    case 'blue potion':
                        blue_potion()
                        break 
                    case 'bandages':
                        bandages()
                        break
            except IndexError:
                print('This Item does not exist.\nWhich item?')
        break
def console(): #command console
    global atk
    global health
    global inventory
    global armor
    global key
    room_list = {
        "1": room1,
        "2": room2,
        "3": room3,
        "4": room4,
        "5": room5,
        "6": room6,
        "r": roomr
    }
    CL=True
    while CL:
        command=input('Opened console. Enter command or close.\n')
        match command:
            case 'help':
                print('''List of commands:
    -health, -fullhealth, -weapon, -godweapon, -armor, -godarmor, -items, -room x, -win''')
            case 'close': #(case closed)
                break
            case 'weapon':
                atk=30
                print('attack set to 30.')
            case 'godweapon':
                atk=999
                print('attack set to 999.')
            case 'armor':
                armor=8
                print('armor set to 8')
            case 'godarmor':
                armor=99
                print('armor set to 99.')
            case 'items':
                inventory.append('bread')
                inventory.append('red potion')
                inventory.append('shuriken')
                inventory.append('antidote')
                inventory.append('blue potion')
                inventory.append('bandages')
                print('items added to inventory')
            case s if s.startswith("room "):
                room_num = s.removeprefix("room ").strip()
                if len(room_num) > 0:
                    room_list.get(room_num)()
            case 'win':
                win()
                break
            case 'health':
                print(health)
            case 'fullhealth':
                health=100
                print('set health to 100.')
            case 'key':
                key=True
            case 'exit':
                exit()
            case _:
                print('invalid command')
        
def healthcheck():
    global health
    global status
    print('You have',health,'health left')
    if status==1:
        print("You're poisoned!")
    if status==2:
        print("You're bleeding!")

#the items:        
def bread():
    global inventory
    global health
    global incombat
    print('A loaf of bread. Restores some health.\n 1 eat\n 2 discard\n 3 back')
    L=True
    while L:
        try:
            action=int(input())
            match action:
                case 1:
                    health=health+10
                    if health>100:
                        health=100
                    print('You recovered some health.')
                    inventory.remove('bread')
                    if incombat==False:
                        restitem()
                    break
                case 2:
                    inventory.remove('bread')
                    print('You removed the bread from your inventory.')
                    if incombat==False:
                        restitem()
                    break
                case 3:
                    if incombat==True:
                        combatitem()
                    elif incombat==False:
                        restitem()
                    break
        except ValueError:
            print('Your input must be an integer(a whole number)')
def shuriken():
    global inventory
    global enemyhp
    global incombat
    global enemy
    print('A small metal star used for throwing.\n 1 throw\n 2 discard\n 3 back')
    L=True
    while L:
        try:
            action=int(input())
            match action:
                case 1:
                    if incombat==True:
                        enemyhp=enemyhp-(10+(3*atk//2))
                        print('You threw the shuriken at the',enemy,'. It dealt',(10+(3*atk//2)),'damage.')
                        inventory.remove('shuriken')
                        break
                    if incombat==False:
                        print('You throw the shuriken against the wall. It does nothing. You pick it up and feel stupid.')
                        restitem()
                        break
                case 2:
                    inventory.remove('shuriken')
                    print('You removed the shuriken from your inventory.')
                    if incombat==False:
                        restitem()
                    break
                case 3:
                    if incombat==True:
                        combatitem()
                    if incombat==False:
                        restitem()
                    break
        except ValueError:
            print('Your input must be an integer(a whole number)')
def red_potion():
    global inventory
    global health
    global incombat
    print('A red potion. It speeds up the healing process immensely.\n 1 drink\n 2 discard\n 3 back')
    L=True
    while L:
        try:
            action=int(input())
            match action:
                case 1:
                    health=health+50
                    if health>100:
                        health=100
                    print('You recovered a lot of health.')
                    inventory.remove('red potion')
                    if incombat==False:
                        restitem()
                    break
                case 2:
                    inventory.remove('red potion')
                    print('You removed the red potion from your inventory.')
                    if incombat==False:
                        restitem()
                    break
                case 3:
                    if incombat==True:
                        combatitem()
                    if incombat==False:
                        restitem()
                    break
        except ValueError:
            print('Your input must be an integer(a whole number)')
def antidote():
    global inventory
    global incombat
    global status
    print('An antidote to cure poisoning.\n 1 use\n 2 discard\n 3 back')
    L=True
    while L:
        try:
            action=int(input())
            match action:
                case 1:
                    if status==1:
                        status=0
                        print('Your poisoning was cured.')
                        inventory.remove('antidote')
                        if incombat==False:
                            restitem()
                        break
                    else:
                        print("You're not poisoned.")
                        if incombat==True:
                            combatitem()
                        if incombat==False:
                            restitem()
                            break
                case 2:
                    inventory.remove('antidote')
                    print('You removed the antidote from your inventory.')
                    break
                case 3:
                    if incombat==True:
                        combatitem()
                    if incombat==False:
                        restitem()
                    break
        except ValueError:
            print('Your input must be an integer(a whole number)')
def blue_potion():
    global inventory
    global enemyhp
    global incombat
    global enemy
    print('This liquid reacts violently when exposed to air.\n 1 throw\n 2 discard\n 3 back')
    L=True
    while L:
        try:
            action=int(input())
            match action:
                case 1:
                    if incombat==True:
                        enemyhp=enemyhp-(100)
                        print('You threw the vial at the',enemy,'. It burst into flames and dealt 100 damage.')
                        inventory.remove('blue potion')
                        break
                    if incombat==False:
                        print('''You can hear you Chemistry teacher calling out to you.
        "This is neither the right place, nor the right time to use this item."''')
                        restitem()
                        break
                case 2:
                    inventory.remove('blue potion')
                    print('You removed the blue potion from your inventory.')
                    if incombat==False:
                        restitem()
                    break
                case 3:
                    if incombat==True:
                        combatitem()
                    if incombat==False:
                        restitem()
                    break
        except ValueError:
            print('Your input must be an integer(a whole number)')
def bandages():
    global inventory
    global incombat
    global status
    print('These bandages can be used to treat bleeding.\n 1 use\n 2 discard\n 3 back')
    L=True
    while L:
        try:
            action=int(input())
            match action:
                case 1:
                    if status==2:
                        status=0
                        print('Your wound stopped bleeding.')
                        inventory.remove('bandages')
                        if incombat==False:
                            restitem()
                        break
                    else:
                        print("You're not bleeding.")
                        if incombat==True:
                            combatitem()
                        if incombat==False:
                            restitem()
                            break
                case 2:
                    inventory.remove('bandages')
                    print('You removed the bandages from your inventory.')
                    break
                case 3:
                    if incombat==True:
                        combatitem()
                    if incombat==False:
                        restitem()
                    break
        except:
            print('Your input must be an integer(a whole number)')

#the rooms
def room1():
    global first_r1
    global inventory
    global health
    global incombat
    incombat=False
    global room
    if first_r1==True:
        print('''
You finally arrive at the first room of the dungeon.
Torches light up the crudely hewn walls. In a small niche, you find a red potion and a shuriken.''')
        inventory.append('red potion')
        inventory.append('shuriken')
    if first_r1==False:
        print('''
You enter the first room of the dungeon again. You're starting to become familiar with this place.''')
    healthcheck()
    print('You could use an item or venture deeper into the dungeon.\n 1 item \n 2 move on\n')
    L1=True
    while L1:
        try:
            choice=int(input())
            match choice:
                case 1:
                    restitem()
                    break
                case 2:
                    break
                case _:
                    print('please input a valid number!')
        except:
            print('Your input must be an integer(a whole number)')
    LLL=True
    while LLL:
        message = "Before you lie three paths.\n"
        if first_r2:
            message += "1 On the left, you can hear rustling and clacking.\n2 In the middle, there seems to be a gate of some sorts. You need a key to pass here.\n"
        else:
            message += "1 You've already been to the left.\n2 In the middle, there seems to be a gate of some sorts. You need a key to pass here.\n"
        if first_r4:
            message += "3 On your right, you can hear heavy footsteps. Something big must be in there."
        else:
            message += "3 You've already been to the right."
        print(message)
        try:
            path=int(input())
            match path:
                case 1:
                    room=2
                    break
                case 2:
                    room=3
                    break
                case 3:
                    room=4
                    break
                case _:
                    print('please input a valid number!') 
        except ValueError:
            print('Your input must be an integer(a whole number)') 

    first_r1=False
def room2():
    global first_r2
    global inventory
    global health
    global incombat
    global enemy
    global atk
    global room
    incombat=False
    if first_r2==False:
        print("The skeleton still lies on the ground. This time, however, it stays dead.")
    if first_r2==True:
        print('''As you enter the next room, you see the skeleton of an adventurer who came here before you, but never made it out.
Its hand is still tightly gripping the sword which that unfortunate soul used to defend themselves.
As you come closer, the skeleton suddenly jolts up and turns towards you. It must be posessed by an evil spirit!
''')
        enemy='skeleton'
        enemystats()
        encounter()
        combat(enemy)
        gameovercheck()
        if gameover==False:
            print("Whatever brought this skeleton to life, it's gone.\nYou help yourself to the skeleton's sword.")
            if atk<25:
                atk=25
            print('Searching through the room, you find a loaf of bread, an antidote and another shuriken stashed away in a chest.')
            inventory.append('bread')
            inventory.append('antidote')
            inventory.append('shuriken')
    if gameover==False:
        healthcheck()
        print('You could use an item or venture deeper into the dungeon.\n 1 item \n 2 move on\n')
        L1=True
        while L1:
            try:
                choice=int(input())
                match choice:
                    case 1:
                        restitem()
                        break
                    case 2:
                        break
                    case _:
                        print('please input a valid number!')
            except ValueError:
                print('Your input must be an integer(a whole number)')
        LLL=True
        while LLL:
            print('''
There is a door leading deeper into the dungeon. You can also return to the first room and chose another path.
1 go deeper into the dungeon
2 go back to the first room
''')
            try:
                path=int(input())
                match path:
                    case 1:
                        room=5
                        break
                    case 2:
                        room=1
                        break
                    case _:
                        print('please input a valid number!')
            except ValueError:
                print('Your input must be an integer(a whole number)')

    first_r2=False
def room3(): #boss room
    global inventory
    global health
    global incombat
    incombat=False
    global room
    global key
    global enemy
    if key==False:
        print('This room is locked.')
        room=1
    else:
        print('''You insert the key into the gate and turn it. The gate swings wide open.
Unafraid of what's to come, you venture forth into the dark halls until you arrive in a well lit room.
Golden cups, jewelry and other trinkets scattered around the room have definitely made this adventure wirth your while.
However, the owner doesn't seem to be willing to part with it, as you soon find out. 
A vampire glides from the ceiling, with a hunger for blood in its eyes.
''')
        enemy='vampire'
        enemystats()
        encounter()
        combat(enemy)
        gameovercheck()
        if gameover==True:
            print('So close and yet so far')
        else:
            win()
def room4():
    global first_r4
    global inventory
    global health
    global incombat
    global enemy
    global atk
    global status
    global room
    incombat=False
    if first_r4==True:
        print('''You decide that it's time to take on whatever awaits you here.
A terrible stench of rotting flesh fills the air. On the other side of the room you just entered stands a large man.
However, he doesn't look like he's really alive anymore. His clothes are torn and reveal necrosis spreading across his skin.
His mouth is wide open and drooling what seems to be saliva mixed with blood. 
You are struck by the realization that this is a ghoul.
At the same moment, the ghoul is struck by the realization that fresh meat has just arrived at the door.
''')
        enemy='ghoul'
        enemystats()
        encounter()
        combat(enemy)
        gameovercheck()
        if gameover==False:
            print('After a tough battle, the ghoul is defeated. You decide to tend to your wounds and rest for a while.')
            status=0
            if health<80:
                health=80
            healthcheck()
    if first_r4==False:
        print('''You can still smell the ghoul. You decide it's better to move on quickly.''')
    if gameover==False:
        print('You could use an item or venture deeper into the dungeon.\n 1 item \n 2 move on\n')
        L1=True
        while L1:
            try:
                choice=int(input())
                match choice:
                    case 1:
                        restitem()
                        break
                    case 2:
                        break
                    case _:
                        print('please input a valid number!')
            except ValueError:
                print('Your input must be an integer(a whole number)')
        LLL=True
        while LLL:
            print('''
There is a door leading deeper into the dungeon. You can also return to the first room and chose another path.
1 go deeper into the dungeon
2 go back to the first room
''')
            try:
                path=int(input())
                match path:
                    case 1:
                        room=6
                        break
                    case 2:
                        room=1
                        break
                    case _:
                        print('please input a valid number!')
            except ValueError:
                print('Your input must be an integer(a whole number)')
    first_r4=False
def room5():
    global first_r5
    global inventory
    global health
    global incombat
    global enemy
    global atk
    global armor
    global room
    incombat=False
    if first_r5==True:
        print('''This room is full of cobwebs. Looks like nobody has bothered to look in here for quite some time.
The large spider rapidly crawling towards you gives you an Idea why.
              ''')
        enemy='spider'
        enemystats()
        encounter()
        combat(enemy)
        gameovercheck()
        if gameover==False:
            healthcheck()
            print('''In one swift strike, the spider is dispatched. Searching through the room, you find some worn armor.
It has sustained some damage and obviously failed to adequately protect its previous wearer.
''')
            if armor==0:
                armor=5
                print("It's better than nothing tho, so you put it on anyways.")
            else:
                print("You decide it's not better than what you're waering so you leave it there.")
            print('You also find a vial with a light blue liquid inside.')
            inventory.append('blue potion')
    if first_r5==False:
        print('There is nothing in this room except cobwebs and a dead spider.')
    if gameover==False:
        LLL=True
        while LLL:
            print('''This room appears to be a dead end.
1 go back to the start
2 go back one room
                    ''')
            try:
                path=int(input())
                match path:
                    case 1:
                        room=1
                        break
                    case 2:
                        room=2
                        break
                    case _:
                        print('please input a valid number!')
            except ValueError:
                print('Your input must be an integer(a whole number)')
        first_r5=False    
def room6():
    global first_r6
    global inventory
    global health
    global incombat
    global key
    global atk
    global armor
    global enemy
    incombat=False
    global room
    if first_r6==True:
        print('''As you enter the next room, you see the skeleton of an adventurer who came here before you, but never made it out.
Its hand is still tightly gripping the sword which that unfortunate soul used to defend themselves.
As you come closer, the skeleton suddenly jolts up and turns towards you. It must be posessed by an evil spirit!
''')
        enemy='skeleton'
        enemystats()
        encounter()
        combat(enemy)
        gameovercheck()
        if gameover==False:
            healthcheck()
            print('''Whatever brought this skeleton to life, it's gone. 
In its dead hands, you see a golden key. Remembering the gate from earlier, you decide to take it.''')
            key=True
            print('''Looking around inside the room, it appears to have been used as a storage room. 
Since the original owner desn't seem to be alive anymore, you take whatever seems useful to you.
That includes a shiny new sword, plated armor, a red potion and some bandages.
''')
            if atk<30:
                atk=30
            if armor<8:
                armor=8
            inventory.append('red potion')
            inventory.append('bandages')
    if first_r6==False:
        print('The skeleton lies dead on the floor.') 
    if gameover==False:
        LLLLL=True
        while LLLLL:
            print('''This room appears to be a dead end.
1 go back to the start
2 go back one room
''')
            try:
                path=int(input())
                match path:
                    case 1:
                        room=1
                        break
                    case 2:
                        room=4
                        break
                    case _:
                        print('please input a valid number!')
            except ValueError:
                print('Your input must be an integer(a whole number)')
    first_r6=False
def roomr(): #yeah idk, maybe send the player here, if they've been naughty
    print('I am error!')
    combat('MissingNo.')
    healthcheck()
    console()

while gameover==False: #the game has to run in this loop so I can end it
    match room:
        case 0:
            enemy='bat'
            enemystats()
            encounter()
            combat(enemy)
            gameovercheck()
            #console() #dev option
            room=1 #turn this off if you want early console
        case 1:
            room1()
        case 2:
            room2()
        case 3:
            room3()
        case 4:
            room4()
        case 5:
            room5()
        case 6:
            room6()
        case _:
            roomr()

if health<=0:
    print('GAME OVER!')
elif room!=7:
    print("Well... This shouldn't happen")
    console()
input('Input anything to exit the game.')