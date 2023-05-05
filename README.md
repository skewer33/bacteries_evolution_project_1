# bacteries_evolution_project_1
Bacteria evolution project using genetic algorithm. Implemented in python using pygame

This is an educational project that my students and I implemented as part of the "Mathematical Modeling of Evolution in Biological Systems" project for Sirius.Summer.

Purpose: to show the adaptation of a model organism in the conditions of competition for resources. A bacterium with a genome consisting of three genes was chosen as a model organism. Each gene influenced its own bacterium parameter: speed, size and sensitivity. At this stage, the gene is given by one real number.

Description of parameters:
Velocity affects how fast the bacterium moves across the simulation field.
Size affects the physical size of a bacterium. The larger size allows bacteria to eat smaller organisms.
Sensitivity allows the organism to determine the nearest objects within the radius of the value of this parameter. Depending on the type of object being determined, the organism makes a decision: to go to the object in order to eat it, or to run away from it.

The values of bacteria parameters affect the amount of energy they consume. The absorption of bacteria or food allows you to replenish energy reserves. When the energy value drops to 0, the organism dies. If a organism has an excess of energy, it gives offspring.

Adaptation is provided by the process of mutations. Every Mutation_Period of simulation steps, a random change occurs in one of the genes. Mutations are fixed in descendants.

At this stage, the size of the bacterium is a parameter that does not affect anything. Since it consumes energy, bacteria have become the most adapted, which manage to reduce the value of this parameter in a shorter time.
With simulation constants set (see file "constants") we were able to show two survival strategies. The first is to stand still and wait for a new portion of food to spawn on the map next to you, while spending almost no energy. At the same time, sensitivity and size also have values close to 0, since they are not needed.
The second strategy involves having great speed and instinct, which allows you to notice food at a great distance and quickly run towards it. At the same time, energy is consumed very quickly, which "forces" to increase speed in order to keep up with food before others.
My friend noticed that we got confirmation of the division of eukaryotes into plants and animals, lol.

You can try to modify the project or just run it and try changing the parameters in the "constant" file. You can share your results :)
