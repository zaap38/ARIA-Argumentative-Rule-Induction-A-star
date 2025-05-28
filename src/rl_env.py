import random as rd
from statistics import mean
from tqdm import tqdm


HIT = 0
STAND = 1
SPLIT = 2
DOUBLE = 3

ACTIONS = [HIT, STAND, SPLIT, DOUBLE]


class Environment:

    def __init__(self):
        self.cards = []  # card stack
        self.dealer = []  # dealer cards
        self.player = []  # player cards

    def reset_deck(self):
        self.cards = []
        for value in (list(range(2, 10)) + ['J', 'Q', 'K', 'A']) * 4:
            self.cards.append(value)
        rd.shuffle(self.cards)

    def get_hand_value(self, hand):
        value = 0
        ace = 0
        has_ace = False
        for card in hand:
            if card in ['J', 'Q', 'K']:
                value += 10
            elif card == 'A':
                ace += 1
            else:
                value += card
        for i in range(ace):
            if value + 11 <= 21:
                value += 11
                has_ace = True
            else:
                value += 1
        return value, has_ace

    def init(self):
        self.reset_deck()
        """self.player = self.cards[:2]
        self.dealer = self.cards[2:4]
        self.cards = self.cards[4:]"""
        self.player = [self.cards.pop(), self.cards.pop()]
        self.dealer = [self.cards.pop()]

    def do_action(self, action):

        # return S, R, S', done

        prev_state = self.get_state()
        double = False
        if action == DOUBLE:
            double = True
            action = STAND
            self.player.append(self.cards.pop())
            if self.get_hand_value(self.player)[0] > 21:
                return prev_state, -2, self.get_state(), True
        
        if action == HIT:
            self.player.append(self.cards.pop())
            if self.get_hand_value(self.player)[0] > 21:
                return prev_state, -1, self.get_state(), True
            else:
                return prev_state, 0, self.get_state(), False

        elif action == SPLIT:
            pass

        elif action == STAND:
            dealer_value = self.get_hand_value(self.dealer)[0]
            while dealer_value < 17:
                self.dealer.append(self.cards.pop())
                dealer_value = self.get_hand_value(self.dealer)[0]
                #print(dealer_value)
            player_value, _ = self.get_hand_value(self.player)
            dealer_value, _ = self.get_hand_value(self.dealer)
            if dealer_value > 21 or player_value > dealer_value:
                rew = 1
                if double:
                    rew = 2
                if player_value == 21 and len(self.player) == 2:
                    rew *= 1.5
                return prev_state, rew, self.get_state(), True
            elif player_value == dealer_value:
                return prev_state, 0, self.get_state(), True
            else:
                rew = -1
                if double:
                    rew = -2
                return prev_state, rew, self.get_state(), True

    def get_state(self):
        player_value, player_has_ace = self.get_hand_value(self.player)
        dealer_value, dealer_has_ace = self.get_hand_value(self.dealer)
        player_str = str(player_value)
        if player_has_ace:
            player_str = str(player_value - 10) + '/' + player_str
        dealer_str = str(dealer_value)
        if dealer_has_ace:
            dealer_str = str(dealer_value - 10) + '/' + dealer_str
        return player_str + "|" + dealer_str

class Agent:

    def __init__(self, total):
        self.env = Environment()
        self.cards = []
        self.q = {}
        self.lr = 0.01
        self.gamma = 0.9
        self.epsilon = 1
        self.total = total
        self.decay = 1 / int(0.8 * total)

        self.step_count = 0
        self.history = []
        self.sum_reward = 0
        self.sum_reward_count = 0
        self.epsilon_history = []
        self.epsilon_power = 0.6

    def choose_action(self, state):
        possible = [HIT, STAND, DOUBLE]
        if pow(self.epsilon, self.epsilon_power) > rd.random():
            action = rd.choice(possible)
        else:
            action = max(possible, key=lambda a: self.q.get((state, a), 0))
        return action

    def update_q(self, prev_state, action, reward, state):
        self.q[(prev_state, action)] = self.q.get((prev_state, action), 0) + \
                                       self.lr * (reward + self.gamma * max([self.q.get((state, a), 0) for a in ACTIONS]) - \
                                       self.q.get((prev_state, action), 0))

    def step(self, verbose=False):
        action = None
        stop = False
        reward = 0
        state = self.env.get_state()
        if verbose:
            print("vvvvvv")
        while not stop:
            action = self.choose_action(state)
            prev_state, reward, state, stop = self.env.do_action(action)
            if verbose:
                print(prev_state, "HIT" if action == 0 else "STAND" if action == 1 else "DOUBLE", state)
            self.update_q(prev_state, action, reward, state)
            #self.epsilon *= self.decay
            self.epsilon -= self.decay
            self.epsilon = max(0, self.epsilon)
        if verbose:
            print("WIN" if reward > 0 else "LOSE" if reward < 0 else "DRAW")
        return reward

    def train(self, nb_episodes):
        reward_history = []
        reward_history_length = 5000
        for i in tqdm(range(nb_episodes)):
            self.step_count += 1
            self.env.init()
            verbose = i > 0.99 * nb_episodes and False
            reward = self.step(verbose)
            reward_history.append(reward)
            self.sum_reward += reward if self.epsilon <= 0 else 0
            self.sum_reward_count += 1 if self.epsilon <= 0 else 0
            if i >= reward_history_length:
                reward_history.pop(0)
            #print(mean(reward_history))
            if len(reward_history) >= reward_history_length and i % reward_history_length == 0:
                self.history.append(mean(reward_history))
                self.epsilon_history.append(pow(self.epsilon, self.epsilon_power))
            if i % reward_history_length == 0 and verbose:
                print(i, mean(reward_history))

    def reset(self):
        pass

    def export_data(self, filename, line_count):
        
        with open(filename, 'w') as f:
            for i in range(line_count):
                possible = [HIT, STAND, DOUBLE]
                player = rd.randint(4, 21)
                dealer = rd.randint(4, 16)
                max_value = -3
                max_key = None
                player_ace = ""
                ace_proba = 0.07
                if rd.random() < ace_proba and player > 10:
                    player_ace = str(player - 10) + '/'
                dealer_ace = ""
                if rd.random() < ace_proba and dealer > 10:
                    dealer_ace = str(dealer - 10) + '/'
                for p in possible:
                    value = self.q.get((player_ace + str(player) + '|' + dealer_ace + str(dealer), p), 0)
                    if value > max_value:
                        max_value = value
                        max_key = p
                label = self.q.get((str(player) + '|' + str(dealer), max_key), 0)
                label_string = "HIT" if max_key == 0 else "STAND" if max_key == 1 else "DOUBLE"


                args = dict()
                # basic
                args["player_sum"] = player
                args["dealer_sum"] = dealer
                args["player_less_dealer"] = player < dealer
                args["dealer_above_11"] = dealer > 11
                args["player_above_11"] = player > 11
                args["player_has_ace"] = len(player_ace) > 0
                args["dealer_has_ace"] = len(dealer_ace) > 0

                # advanced
                """args["player_above_15"] = player > 15
                args["dealer_below_11"] = dealer < 11
                args["dealer_above_6"] = dealer > 6
                args["player_less_dealer"] = player < dealer
                args["player_has_ace"] = len(player_ace) > 0
                args["dealer_has_ace"] = len(dealer_ace) > 0"""

                string = ""
                sep = ','
                for k in args.keys():
                    string += str(args[k]) + sep
                string += label_string
                f.write(string + '\n')
            f.close()

    def print_policy(self):
        data = self.q
        max_b_for_a = {}
        for key, value in data.items():
            a, b = key  # Unpack the tuple into variables 'a' and 'b'
            if a not in max_b_for_a or value > data[max_b_for_a[a]]:
                max_b_for_a[a] = key
        policy = {}
        for key, value in max_b_for_a.items():
            a, b = value
            policy[key] = 'HIT' if b == 0 else 'STAND' if b == 1 else 'DOUBLE'
        print(policy)


if __name__ == "__main__":

    total = 600000
    rd.seed(42)

    agent = Agent(total)
    agent.train(total)

    agent.export_data('data.txt', 600)
    # draw reward history
    print(round(agent.sum_reward / agent.sum_reward_count, 2))
    agent.print_policy()

    
    import matplotlib.pyplot as plt
    plt.plot(agent.history)
    plt.plot(agent.epsilon_history)
    plt.show()
    