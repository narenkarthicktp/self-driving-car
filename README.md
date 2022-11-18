<div style="display: flex;">

 <div style="padding: 20px; width: 800px;">
  <img src=".\preview.png"></img>
 </div>

 <div style="padding: 20px;">

  ## Self-driving car

  A simple simulation of a self driving car in a highway traffic using feed forward neural networks. The neural network is refined using genetic algorithm. The network is mutated everytime the simulation is reloaded resulting in a slightly altered network that can either perform better or worse than the parent. This way, the best car from each simulation is saved and mutated in the next simulation to improve the neural network.

  <hr/>

  ## Steps to train the car :

   - Run the simulation until the car crashes [eventually]
   - Save the model and reload
   - Repeat the above steps until you get an optimal model that learns to reach a specific distance without crashing

  Tip : Inorder to train the network faster, try increasing the mutation rate and no. of car instances.

 </div>
</div>