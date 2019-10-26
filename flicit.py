import json
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


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
        elif input_str == "s":
            display_stats()
        elif input_str == "o":
            change_options()
        else:
            break
    print("Thank for playing!")


def print_help():
    print("""OPTIONS:
        (m)atch -> runs a match between two competitors
        (r)atings -> prints all of the elo ratings top to bottom
        (u)psets -> prints all of the matches where the predicted loser won
        (s)tatistics -> displays interesting statistics about the program / game
        (o)ptions -> alows you to change settings in the config file
        
        INFO:
        There is a config.json file in the project directory. It has settings like upset threshold.
        The upset threshold determines how low the winners predicted score had to be to be considered an upset.
        For example, if the upset threshold is 45 and a user was predicted to lose 46-64, that is not an upset.""")


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

        print("{} has a {}% chance of winning, giving {} {}%".format(player1, player1_expect * 100, player2,
                                                                     player2_expect * 100))

        player1_points = int(input("How many points did {} score? ".format(player1)))
        player2_points = int(input("How many points did {} score? ".format(player2)))
        total_points = player1_points + player2_points
        player1_score = player1_points / total_points
        player2_score = player2_points / total_points

        update_upsets(player1_points, player2_points, player1_expect, player2_expect, player1, player2)

        if player1_points > player2_points and player1_expect > player2_expect:
            config_dict["correct"] += 1
        elif player2_points > player1_points and player2_expect > player1_expect:
            config_dict["correct"] += 1

        config_dict["total"] += 1

        player1_rating += 64 * (player1_score - player1_expect)
        player2_rating += 64 * (player2_score - player2_expect)

        ratings_dict[player1] = player1_rating
        ratings_dict[player2] = player2_rating

        with open("ratings.json", "w") as ratings_file:
            json.dump(ratings_dict, ratings_file)
        with open("upsets.json", "w") as upsets_file:
            json.dump(upsets_dict, upsets_file)
        with open("config.json", "w") as configs_file:
            json.dump(config_dict, configs_file)


def update_upsets(player1_points, player2_points, player1_expect, player2_expect, player1, player2):
    threshold = config_dict["threshold"] / 100
    if player1_points > player2_points and player1_expect < threshold:
        print("UPSETTT for player1")
        rivalry_title = player1 + " vs " + player2
        if rivalry_title in upsets_dict.keys():
            upsets_dict[rivalry_title].append((player1_points, player2_points))
        else:
            upsets_dict[rivalry_title] = [(player1_points, player2_points)]
    elif player2_points > player1_points and player2_expect < threshold:
        print("UPSETTT for player2")
        rivalry_title = player2 + " vs " + player1
        if rivalry_title in upsets_dict.keys():
            upsets_dict[rivalry_title].append((player2_points, player1_points))
        else:
            upsets_dict[rivalry_title] = [(player2_points, player1_points)]


def display_ratings():
    x = np.array([])
    elo = np.array([])

    plt.clf()

    name_rating_pair_list = sorted(ratings_dict.items(), key=lambda key_val: key_val[1], reverse=True)

    for name_rating_pair in name_rating_pair_list:
        elo_rating = name_rating_pair[1]
        print("{}\t{}".format(name_rating_pair[0], elo_rating))
        plt.text(get_x_from_elo(elo_rating), elo_rating, name_rating_pair[0])
        x = np.append(x, get_x_from_elo(elo_rating))
        elo = np.append(elo, elo_rating)

    plt.title("Elo rating visualizer")
    if config_dict["display_graph"] == "logistic":
        plt.scatter(x, elo)
        domain = np.linspace(np.amin(x), np.amax(x), 100)
        yrange = 800 / (1 + np.exp(domain * -6.68336)) + 600
        plt.plot(domain, yrange, 'b')
        plt.xlabel("suck/don't suck factor")
        plt.ylabel('elo rating')
        plt.show()
    elif config_dict["display_graph"] == "histogram":
        fit = stats.norm.pdf(elo, np.mean(elo), np.std(elo))
        plt.plot(elo, fit, '-x')
        plt.hist(elo, facecolor='b', density=True)
        plt.xlabel("Elo rating")
        plt.ylabel("Frequency")
        plt.show()


# Based on finding inverse of this graph: https://www.desmos.com/calculator/ud1ui0nvy7
def get_x_from_elo(rating):
    x = -1 * math.log(800 / (rating - 600) - 1) / 6.68336
    return x


def display_upsets():
    for rivalry, scores in upsets_dict.items():
        print(rivalry.ljust(19, " "), end='\t')
        for score in scores:
            print(score)
            print("\t" * 5, end='')
        print("")


def display_stats():
    correct = config_dict["correct"]
    total_matches = config_dict["total"]
    print("{}%\tCorrect prediction percent ({} / {})".format((correct / total_matches) * 100, correct, total_matches))


def change_options():
    print("Current options:")
    print(config_dict)
    while True:
        input_opt = input("What option do you want to change? (q to exit) ")
        if input_opt == "threshold":
            thresh_input = int(input("What should the threshold be (please give an integer in the range [0, 51]) "))
            config_dict["threshold"] = thresh_input
        elif input_opt == "display_graph":
            graph_input = input("What should the display type be? (logistic, histogram) ")
            config_dict["display_graph"] = graph_input
        else:
            break
    with open("config.json", 'w') as configs_file:
        json.dump(config_dict, configs_file)


with open("config.json", 'r') as config_file:
    config_dict = json.load(config_file)
with open("ratings.json", 'r') as rating_file:
    ratings_dict = json.load(rating_file)
with open("upsets.json", 'r') as upset_file:
    upsets_dict = json.load(upset_file)

main()
