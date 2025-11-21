Given the following environment made of a grid (55) parking lot: a passenger and a self-driving taxi. The goal is that
the agent (the taxi) picks up the passenger and drops them at the desired location.

There are four possible locations for the initial passenger and the destination. These locations are colored Red, Blue,
Yellow and Green in the figure below.

The possible actions are:

- Go West
- Go East
- Go North
- Go South
- Pickup
- Drop-off

Rewards:

- Correct dropoff: +20
- Wrong pickup/dropoff: -10
- Each time-step: -1

At each episode the agent and passenger/destination start at random valid locations.

![taxi snapshot](./screenshot.png)
