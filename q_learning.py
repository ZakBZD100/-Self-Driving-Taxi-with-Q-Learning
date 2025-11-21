import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import random


def update_q_table(Q, s, a, r, sprime, alpha, gamma):
    """
    This function should update the Q function for a given pair of action-state
    following the q-learning algorithm, it takes as input the Q function, the pair action-state,
    the reward, the next state sprime, alpha the learning rate and gamma the discount factor.
    Return the same input Q but updated for the pair s and a.
    """
    #Q-learning update rule:
    #Q(s,a) <- Q(s,a) + alpha * (r + gamma * max_a' Q(s',a') - Q(s,a))
    best_next = np.max(Q[sprime])
    td_target = r + gamma * best_next
    td_error = td_target - Q[s, a]
    Q[s, a] = Q[s, a] + alpha * td_error
    return Q

def epsilon_greedy(Q, s, epsilone):

    """
    This function implements the epsilon greedy algorithm.
    Takes as unput the Q function for all states, a state s, and epsilon.
    It should return the action to take following the epsilon greedy algorithm.
    """
    # exploration with probability epsilone
    if random.random() < epsilone:
        return random.randint(0, Q.shape[1] - 1)
    # otherwise exploitation: choose best action with random tie-breaking
    best_actions = np.flatnonzero(Q[s] == Q[s].max())
    return int(np.random.choice(best_actions))

if __name__ == "__main__":
    env = gym.make("Taxi-v3", render_mode="human")

    Q = np.zeros([env.observation_space.n, env.action_space.n])

    alpha = 0.15
    gamma = 0.99
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.998

    n_epochs = 2000
    max_itr_per_epoch = 200
    rewards = []

    print("Training started - watch the taxi learn!\n")

    for e in range(n_epochs):
        total_r = 0
        S, _ = env.reset()

        for t in range(max_itr_per_epoch):
            A = epsilon_greedy(Q=Q, s=S, epsilone=epsilon)

            # gymnasium returns: obs, reward, terminated, truncated, info
            Sprime, R, terminated, truncated, info = env.step(A)
            done = terminated or truncated

            total_r += R

            Q = update_q_table(Q=Q, s=S, a=A, r=R, sprime=Sprime, alpha=alpha, gamma=gamma)

            S = Sprime

            if done:
                break

        #decay epsilon
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

        rewards.append(total_r)

        if (e + 1) % 100 == 0:
            print(f"Episode {e+1}/{n_epochs}  avg_reward(last100)={np.mean(rewards[-100:]):.2f}  eps={epsilon:.3f}")

    print(f"\nTraining finished! Average reward = {np.mean(rewards):.2f}")
    print("\nNow watch the trained taxi perform!\n")

    import time
    n_eval = 5
    for i in range(n_eval):
        S, _ = env.reset()
        done = False
        total_r = 0
        steps = 0
        print(f"\n=== Evaluation Run #{i+1} ===")
        while not done and steps < 200:
            A = int(np.argmax(Q[S]))
            Sprime, R, terminated, truncated, info = env.step(A)
            done = terminated or truncated
            total_r += R
            S = Sprime
            steps += 1
            time.sleep(0.05)
        print(f"Completed: reward={total_r}, steps={steps}")
        if total_r == 20:
            print("SUCCESS! Passenger picked up and dropped at correct destination!")
        time.sleep(0.5)

    env.close()
