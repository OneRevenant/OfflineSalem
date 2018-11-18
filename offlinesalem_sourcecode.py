import random
roleNames=["Investigator","Doctor","Mafioso"]
roleIsEvil=[False,False,True]
playerAbilityUses=[]
playerRoles=[]
playerNames=[]
playerEvents=[]
playerSuspicions=[]
playerVotes=[]
votesAgainstPlayer=[]
playerActionLogs=[]
playerAlive=[]
night=0
dayActions=1
playerCount=0
humanPlayerAlive=True
def Day():
	global night
	global playerEvents
	global playerNames
	global playerCount
	global dayActions
	global playerVotes
	global votesAgainstPlayer
	print("DAY "+str(night))
	i=0
	while i<playerCount:
		playerVotes[i]=-1
		votesAgainstPlayer[i]=0
		if playerAlive[i]:
			dying=0
			j=0
			while j<len(playerEvents[i]):
				if playerEvents[i][j]==0: #attacked
					dying+=1
				elif playerEvents[i][j]==1: #healed
					dying-=100
				else: #unknown event (error)
					print("Unknown forces affected "+playerNames[i])
				j+=1
			if dying>0:
				Death(i,playerNames[i]+" died last night!")
			else:
				playerEvents[i]=[]
				i+=1
		else:
			i+=1
	ListPlayers()
	while dayActions>0:
		#player input
		if humanPlayerAlive==True:
			target=int(input("(Day actions left "+str(dayActions)+"/3)\n1. Vote\n2. Claim role\n3. Wait\n"))-1
			if target==0:
				Vote(0,int(input("Who to vote? "))-1)
			elif target==1:
				i=0
				while i<len(roleNames):
					print(str(i+1)+". "+roleNames[i])
					i+=1
				Claim(0,int(input("Which role to claim? "))-1)
			else:
				print("")
		dayActions-=1
		#AI voting
		i=int(humanPlayerAlive)
		alives=0
		while i<playerCount:
			if playerAlive[i]==True:
				alives+=1
				mostSusps=0
				suspestPlrs=[]
				j=0
				while j<playerCount:
					if playerAlive[j]==True:
						if playerSuspicions[i][j]>mostSusps:
							mostSusps=playerSuspicions[i][j]
							del suspestPlrs[:]
						if playerSuspicions[i][j]>=mostSusps:
							suspestPlrs.append(j)
						playerSuspicions[i][j]+=random.randint(0,1) #adding suspicion every day to simulate paranoia
					j+=1
				if len(suspestPlrs)>0 and playerSuspicions[i][suspestPlrs[0]]>1:
					if playerVotes[i]==suspestPlrs[random.randint(0,len(suspestPlrs)-1)]:
						if roleIsEvil[playerRoles[i]]:
							Claim(i,random.randint(0,1))
						else:
							Claim(i,playerRoles[i])
					else:
						Vote(i,suspestPlrs[random.randint(0,len(suspestPlrs)-1)])
			i+=1
		#check votes
		i=0
		while i<playerCount:
			if votesAgainstPlayer[i]>alives/2: #voted up
				print(playerNames[i]+" was voted up!\n")
				if i==0 and humanPlayerAlive==True:
					j=0
					while j<len(roleNames):
						print(str(j+1)+". "+roleNames[j])
						j+=1
					Claim(0,int(input("Which role to claim? "))-1)
				else:
					if roleIsEvil[playerRoles[i]]==True:
						Claim(i,random.randint(0,1))
					else:
						Claim(i,playerRoles[i])
					if humanPlayerAlive==True:
						playerVotes[0]=int(input("\n1. Vote guilty\n2. Vote innocent\n3. Abstain\n"))-1
				j=int(humanPlayerAlive)
				while j<playerCount:
					if playerAlive[j]==True and j!=i:
						if playerSuspicions[j][i]>0:
							playerVotes[j]=0
						elif playerSuspicions[j][i]<0:
							playerVotes[j]=1
						else:
							playerVotes[j]=2
					j+=1
				j=0
				guilties=0
				innos=0
				while j<playerCount:
					if playerAlive[j]==True:
						if j!=i:
							if playerVotes[j]==0:
								print(playerNames[j]+" voted guilty.")
								guilties+=1
							elif playerVotes[j]==1:
								print(playerNames[j]+" voted innocent.")
								innos+=1
							else:
								print(playerNames[j]+" abstained.")
					playerVotes[j]=-1
					votesAgainstPlayer[j]=0
					j+=1
				if guilties>innos:
					Death(i,playerNames[i]+" gets lynched!")
					dayActions=0
			i+=1
def Vote(voter, voted):
	if voter!=voted:
		global playerVotes
		if playerVotes[voter]>=0:
			votesAgainstPlayer[playerVotes[voter]]-=1
			print(playerNames[voter]+" changed their vote to "+playerNames[voted]+".")
		else:
			print(playerNames[voter]+" voted against "+playerNames[voted]+".")
		playerVotes[voter]=voted
		votesAgainstPlayer[voted]+=1
		index=0
		while index<playerCount:
			if playerSuspicions[index][voter]<0:
				playerSuspicions[index][voted]-=playerSuspicions[index][voter]
			index+=1
def Claim(claimer, role, showMessage=True):
	if roleIsEvil[role]==True:
		j=0
		while j<playerCount:
			playerSuspicions[j][claimer]+=1000
			j+=1
	else:
		j=0
		while j<playerCount:
			playerSuspicions[j][claimer]-=10
			j+=1
	if showMessage==True:
		print(playerNames[claimer]+" claimed "+roleNames[role]+".")
def Death(plr, message):
	print(message+" Their role was "+roleNames[playerRoles[plr]]+".")
	print("\nLast will: \n")
	global playerCount
	index=0
	if roleIsEvil[playerRoles[plr]]==True:
		print("(*_*)")
	while index<len(playerActionLogs[plr])-1:
		print("N"+str(index+1)+": "+playerNames[playerActionLogs[plr][index][0]], end="")
		if playerRoles[plr]==0:
			print(" - "+roleNames[playerActionLogs[plr][index][1]], end="")
			if roleIsEvil[playerActionLogs[plr][index][1]]:
				i=0
				while i<playerCount:
					playerSuspicions[i][playerActionLogs[plr][index][0]]+=1000
					i+=1
			else:
				i=0
				while i<playerCount:
					playerSuspicions[i][playerActionLogs[plr][index][0]]-=1000
					i+=1
		print("")
		index+=1
	print("\n")
	playerAlive[plr]=False
	global humanPlayerAlive
	evilsFound=0
	towniesFound=0
	index=0
	global gameEnded
	while index<playerCount:
		if playerAlive[index]==True:
			if roleIsEvil[playerRoles[index]]==True:
				evilsFound+=1
			else:
				towniesFound+=1
		index+=1
	if towniesFound==0:
		gameEnded=True
		input("THE GAME HAS ENDED! MAFIA HAS WON!")
	if evilsFound==0:
		gameEnded=True
		input("THE GAME ENDED! TOWN HAS WON!")
	global humanPlayerAlive
	if plr==0 and humanPlayerAlive==True and gameEnded==False:
		humanPlayerAlive=False
		input("You have died. Press enter to see how rest of the game plays out.") 	
def Night():
	global night
	night+=1
	print("NIGHT "+str(night))
	i=0
	ListPlayers()
	while i<playerCount:
		if playerAlive[i]==True:
			if playerRoles[i]==0:
				InvestigatorNightAbility(i)
			elif playerRoles[i]==1:
				DoctorNightAbility(i)
			elif playerRoles[i]==2:
				MafiosoNightAbility(i)
			else:
				print("")
		i+=1
def InvestigatorNightAbility(activator):
	if activator==0 and humanPlayerAlive==True:
		target=int(input("Which player to interrogate? (insert a number): "))-1
		print(playerNames[target]+" is a "+roleNames[playerRoles[target]]+"!")
	else:
		lowestInfo=1000000000000
		i=0
		target=-1
		targetChoices=[]
		while i<playerCount:
			if playerAlive[i]==True and i!=activator:
				if abs(playerSuspicions[activator][i])==lowestInfo:
					targetChoices.append(i)
				if abs(playerSuspicions[activator][i])<lowestInfo:
					lowestInfo=abs(playerSuspicions[activator][i])
					del targetChoices[:]
					targetChoices.append(i)
			i+=1
		if len(targetChoices)>0:
			target=targetChoices[random.randint(0,len(targetChoices)-1)]
		if target>=0 and roleIsEvil[playerRoles[target]]==True:
			playerSuspicions[activator][target]+=1000
		else:
			playerSuspicions[activator][target]-=1000
	playerActionLogs[activator].append([target,playerRoles[target]])
	if humanPlayerAlive==False:
		print(playerNames[activator]+" ("+roleNames[playerRoles[activator]]+") visited "+playerNames[target]+" ("+roleNames[playerRoles[target]]+")")
def DoctorNightAbility(activator):
	if activator==0 and humanPlayerAlive==True:
		print("You have "+str(playerAbilityUses[activator])+" self heals left.")
		target=int(input("Which player to heal? (insert a number): "))-1
	else:
		lowestSusp=100000000000000
		i=0
		targetChoices=[]
		while i<playerCount:
			if playerAlive[i]==True and (i!=activator or playerAbilityUses[activator]>0):
				if playerSuspicions[activator][i]==lowestSusp:
					targetChoices.append(i)
				if playerSuspicions[activator][i]<lowestSusp:
					lowestSusp=playerSuspicions[activator][i]
					del targetChoices[:]
					targetChoices.append(i)
			i+=1
		if len(targetChoices)>0:
			target=targetChoices[random.randint(0,len(targetChoices)-1)]
	if target!=activator or playerAbilityUses[activator]>0:
		if target==activator:
			playerAbilityUses[activator]-=1
		playerEvents[target].append(1)
	playerActionLogs[activator].append([target])
	if humanPlayerAlive==False:
		print(playerNames[activator]+" ("+roleNames[playerRoles[activator]]+") visited "+playerNames[target]+" ("+roleNames[playerRoles[target]]+")")
def MafiosoNightAbility(activator):
	if activator==0 and humanPlayerAlive==True:
		target=int(input("Which player to kill? (insert a number): "))-1
	else:
		target=random.randint(0,playerCount-1)
		while roleIsEvil[playerRoles[target]] or playerAlive[target]==False:
			target=random.randint(0,playerCount-1)
	playerEvents[target].append(0)
	if humanPlayerAlive==False:
		print(playerNames[activator]+" ("+roleNames[playerRoles[activator]]+") visited "+playerNames[target]+" ("+roleNames[playerRoles[target]]+")")
def ListPlayers():
	index=0
	while index<playerCount:
		print(str(index+1)+". "+playerNames[index], end="")
		if playerAlive[index]==False:
			print(" (dead) ("+roleNames[playerRoles[index]]+")",end="")
		else:
			if gameEnded==True:
				print(" ("+roleNames[playerRoles[index]]+")",end="")
		print("")
		index+=1
print("Welcome to OfflineSalem v0.1 by OneRevenant!")
quitGame=False
gameEnded=False
while quitGame==False:
	i=input("\n1. Start a game\n2. Exit\n")
	if i=="1":
		defaultNames=["John Willard","Deodat Lawson","Jonathan Corwin","Giles Corey","Cotton Mather","Edward Bishop","James Bayley","James Russel",
				"John Hathorne","John Proctor","Samuel Parris","Samuel Sewall","Thomas Danforth","William Phips","William Hobbs",
				"Mary Warren","Abigail Hobbs","Alice Young","Sarah Good","Ann Hibbins","Ann Putman","Ann Sears","Betty Parris","Dorothy Good","Lydia Dustin",
				"Martha Corey","Mary Eastey","Mary Johnson","Sarah Bishop","Sarah Wildes"]
		gameEnded=False
		roleList=[0,0,0,0,1,1,1,2,2]
		i=0
		print("\nRolelist:")
		while i<len(roleList):
			print(roleNames[roleList[i]])
			i+=1
		print("")
		playerCount=len(roleList)
		dayActions=1
		night=0
		del playerEvents[:]
		del playerRoles[:]
		del playerVotes[:]
		del playerNames[:]
		del votesAgainstPlayer[:]
		del playerAbilityUses[:]
		del playerSuspicions[:]
		del playerActionLogs[:]
		del playerAlive[:]
		humanPlayerAlive=True
		roleListClone=roleList
		while len(roleListClone)>0:
			j=random.randint(0,len(roleList)-1)
			playerRoles.append(roleList[j])
			roleList.pop(j)
			j=random.randint(0,len(defaultNames)-1)
			playerNames.append(defaultNames[j])
			defaultNames.pop(j)
			playerEvents.append([])
			playerVotes.append(-1)
			votesAgainstPlayer.append(0)
			playerSuspicions.append([])
			playerAbilityUses.append(1)
			playerActionLogs.append([])
			playerAlive.append(True)
			j=0
			while j<playerCount:
				playerSuspicions[len(playerSuspicions)-1].append(0)
				j+=1
		playerNames[0]=input("Choose a name: ")
		print("Your role is "+roleNames[playerRoles[0]])
		if roleIsEvil[playerRoles[0]]:
			print("Your team is:")
			k=0
			while k<playerCount:
				if roleIsEvil[playerRoles[k]]:
					print(playerNames[k])
				k+=1
			print("")
		j=0
		while gameEnded==False:
			Day()
			if gameEnded==False:
				Night()
				dayActions=3
		input()
	elif i=="2":
		quitGame=True
