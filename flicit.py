import json


def main():
    while True:
        input_str = input("What do you want to do? (h for help): ").lower()
        print(input_str)
        if input_str == "h":
            print_help()
        elif input_str == "m":
            run_match()
        elif input_str == "r":
            display_ratings()
        elif input_str == "u":
            display_upsets()
        else:
            break
    print("Thank for playing!")


def print_help():
    print("""OPTIONS:
        (m)atch -> runs a match between two competitors
        (r)atings -> prints all of the elo ratings top to bottom
        (u)psets -> prints all of the matches where the predicted loser won
        
        INFO:
        There is a config.json file in the project directory. It has settings like upset threshold.
        The upset threshold determines how low the winners predicted score had to be to be considered an upset.
        For example, if the upset threshold is .45 and a user was predicted to lose 46-64, that is not an upset.""")


def run_match():
    while True:
        player1 = input("Enter the name of player 1: ").lower()
        player2 = input("Enter the name of player 2: ").lower()
        if player1 == "##" or player2 == "##":
            break

        if player1 not in ratings_dict:
            ratings_dict[player1] = 1000
        if player2 not in ratings_dict:
            ratings_dict[player2] = 1000
        player1_rating = ratings_dict[player1]
        player2_rating = ratings_dict[player2]

        player1_expect = 1.0 / (1 + 10.0 ** ((player2_rating - player1_rating) / 400.0))
        player2_expect = 1 - player1_expect

        player1_points = int(input("How many points did {} score? ".format(player1)))
        player2_points = int(input("How many points did {} score? ".format(player2)))
        total_points = player1_points + player2_points
        player1_score = player1_points / total_points
        player2_score = player2_points / total_points

        # TODO: Make upsets actually useful but I'm tired and just want the basics working now
        if player1_points > player2_points and player1_expect < threshold:
            print("UPSETTT for player1")
        elif player2_points > player1_points and player2_expect < threshold:
            print("UPSETTT for player2")

        player1_rating += 64 * (player1_score - player1_expect)
        player2_rating += 64 * (player2_score - player2_expect)

        ratings_dict[player1] = player1_rating
        ratings_dict[player2] = player2_rating

        with open("ratings.json", "w") as ratings_file:
            json.dump(ratings_dict, ratings_file)


# TODO Make these next two functions not just a meme
def display_ratings():
    print("Hello there")


def display_upsets():
    print("General Kenobi")


def read_config_file():
    with open("config.json", 'r') as config_file:
        config_settings = json.load(config_file)
        thresh = config_settings["threshold"] / 100
        return thresh


with open("config.json", 'r') as config_file:
    threshold = read_config_file()
with open("ratings.json", 'r') as rating_file:
    ratings_dict = json.load(rating_file)
with open("upsets.json", 'r') as upset_file:
    upsets_dict = json.load(upset_file)

main()
