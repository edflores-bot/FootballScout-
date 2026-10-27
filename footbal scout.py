# ==========================================================================
# PROGRAM: AI Football Scout (Criterion D - Complete Development)
# PURPOSE: Helps a football coach register players, automatically evaluate
#          them with weighted statistics, search, filter, compare, and
#          keep the data between sessions.
# CLIENT:  Football coach (Success Criteria SC1-SC6)
# ==========================================================================

# --------------------------------------------------------------------------
# STEP 1: Load saved players from the previous session (SC6: persistence)
# A List [] holds the roster. Each player is a list:
# [name, position, goals, assists, rating]
# --------------------------------------------------------------------------
players = []
try:
    file = open("players.txt", "r")
    for line in file:
        parts = line.split(",")
        players.append([parts[0], parts[1], int(parts[2]), int(parts[3]), float(parts[4])])
    file.close()
    print(f"Welcome back, Coach! Loaded {len(players)} player(s) from file.")
except:
    print("Welcome, Coach! No previous data found. Starting fresh.")

# --------------------------------------------------------------------------
# STEP 2: Main menu with a WHILE loop (repeats until the coach exits)
# --------------------------------------------------------------------------
option = 0
while option != 8:
    print("\n========== AI FOOTBALL SCOUT ==========")
    print("1. Add player")
    print("2. Evaluate and rank players")
    print("3. Search player by name")
    print("4. Filter by position")
    print("5. Compare two players")
    print("6. Show all players")
    print("7. Save data to file")
    print("8. Save and exit")

    # input() pauses and waits for the user; int() converts text to number
    option = int(input("Choose an option: "))

    # ------------------ OPTION 1: Add player (SC1 + SC5) ------------------
    if option == 1:
        name = input("Player name: ")
        position = input("Position (GK/DF/MF/FW): ")
        goals = int(input("Goals this season: "))
        assists = int(input("Assists this season: "))

        # IF + AND + OR: validates the data before saving (SC5).
        # AND requires ALL conditions to be True; OR allows valid positions.
        valid_position = (position == "GK" or position == "DF" or position == "MF" or position == "FW")
        if name != "" and goals >= 0 and assists >= 0 and valid_position:
            # Check for duplicate player (erroneous data, test T6/T11)
            duplicate = False
            for p in players:
                if p[0] == name and p[1] == position:
                    duplicate = True
            if duplicate:
                print("Warning: this player already exists. Not saved.")
            else:
                players.append([name, position, goals, assists, 0.0])
                print(f"Player {name} saved successfully.")
        else:
            print("Warning: invalid data (empty name, negative number or bad position). Not saved.")

    # -------------- OPTION 2: Evaluate and rank (SC2 + SC4) --------------
    elif option == 2:
        if len(players) == 0:                      # len() counts items (boundary case)
            print("No players stored yet.")
        else:
            # FOR EACH loop: visits EVERY player and calculates rating (SC2).
            # Accumulation applies the coach's predefined weights.
            for p in players:
                p[4] = (p[2] * 0.4) + (p[3] * 0.3)

            # Sorting (rankPlayers): bubble sort, highest rating first (SC4)
            n = len(players)
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    if players[j][4] < players[j + 1][4]:
                        temp = players[j]
                        players[j] = players[j + 1]
                        players[j + 1] = temp

            print("\n--- RANKING ---")
            # IF / ELIF / ELSE classifies each player like the habit tracker feedback
            for k in range(n):
                if players[k][4] >= 8:
                    level = "Excellent"
                elif players[k][4] >= 5:
                    level = "Good player"
                else:
                    level = "Needs improvement"
                print(f"{k + 1}. {players[k][0]} ({players[k][1]}) - Rating: {players[k][4]:.2f} - {level}")

    # -------------- OPTION 3: Search by name (SC3) --------------
    elif option == 3:
        query = input("Name to search: ")
        found = False                              # Boolean flag tracks if we find a match
        for p in players:
            if p[0] == query:
                print(f"Found: {p[0]} | {p[1]} | Goals: {p[2]} | Assists: {p[3]} | Rating: {p[4]:.2f}")
                found = True
        if not found:
            print("No players found with that name.")

    # -------------- OPTION 4: Filter by position (SC3) --------------
    elif option == 4:
        pos = input("Position to filter (GK/DF/MF/FW): ")
        count = 0
        for p in players:
            if p[1] == pos:
                print(f"{p[0]} | Goals: {p[2]} | Assists: {p[3]} | Rating: {p[4]:.2f}")
                count = count + 1                  # Accumulator counts the matches
        if count == 0:
            print("No players found in that position.")

    # -------------- OPTION 5: Compare two players (SC4) --------------
    elif option == 5:
        name_a = input("First player: ")
        name_b = input("Second player: ")
        a = -1                                     # Variables store the found indexes
        b = -1
        for i in range(len(players)):
            if players[i][0] == name_a:
                a = i
            if players[i][0] == name_b:
                b = i
        if a == -1 or b == -1:
            print("Error: one or both players were not found.")
        else:
            print(f"\n{name_a}: {players[a][2]} goals, {players[a][3]} assists, rating {players[a][4]:.2f}")
            print(f"{name_b}: {players[b][2]} goals, {players[b][3]} assists, rating {players[b][4]:.2f}")
            # IF / ELIF / ELSE decides the winner (no manual calculation needed)
            if players[a][4] > players[b][4]:
                print(f"Result: {name_a} has a higher score. {name_a} wins!")
            elif players[b][4] > players[a][4]:
                print(f"Result: {name_b} has a higher score. {name_b} wins!")
            else:
                print("Result: both players are tied.")

    # -------------- OPTION 6: Show all players --------------
    elif option == 6:
        if len(players) == 0:
            print("No players stored yet.")
        else:
            for p in players:
                print(f"{p[0]} | {p[1]} | Goals: {p[2]} | Assists: {p[3]} | Rating: {p[4]:.2f}")

    # -------------- OPTION 7: Save to file (SC6) --------------
    elif option == 7:
        file = open("players.txt", "w")
        for p in players:
            file.write(p[0] + "," + p[1] + "," + str(p[2]) + "," + str(p[3]) + "," + str(round(p[4], 2)) + "\n")
        file.close()
        print(f"Data saved. {len(players)} player(s) stored in players.txt")

    # -------------- OPTION 8: Save and exit --------------
    elif option == 8:
        file = open("players.txt", "w")
        for p in players:
            file.write(p[0] + "," + p[1] + "," + str(p[2]) + "," + str(p[3]) + "," + str(round(p[4], 2)) + "\n")
        file.close()
        print("Data saved. Goodbye, Coach!")

    # -------------- ERRONEOUS option handling (validation, SC5) --------------
    else:
        print("Invalid option. Please choose 1-8.")