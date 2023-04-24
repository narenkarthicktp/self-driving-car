## Self-driving car :car:

A simple simulation of a self driving car in a highway traffic using feed forward neural networks. The neural network is refined using genetic algorithm. The network is mutated everytime the simulation is reloaded resulting in many slightly altered networks, in which some of them might perform better than the parent. This way, the best car from each simulation is saved and mutated in the next simulation to improve the neural network.

---

## Preview :

<img src=".\preview.gif" margin="20px" width="400px"></img>

---

## Steps to train the car :

 - Run the simulation until the car crashes [eventually]
 - Save the model and reload
 - Repeat the above steps until you get an optimal model that learns to reach a specific distance without crashing

Tip : Inorder to train the network faster, try increasing the <a href="https://github.com/NKTP-718/self-driving-car/blob/master/main.py#L53">mutation rate</a> and <a href="https://github.com/NKTP-718/self-driving-car/blob/master/main.py#L54">no. of car instances</a>

---
