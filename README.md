# GAARI
Genetic Algorithm for Argumentative Rule Induction.

<h2>Authors:</h2><br>
B. Alcaraz<br>
C. Leturc<br>
T. Kampik<br>

<h2>Options:</h2><br>
<ul>
  <li>'-e [export_file]'  # The location of the export files. By default 'output/'.</li>
  <li>'-d [dataset]'  # The index of the dataset used (please refer to the section Dataset).</li>
  <li>'-r [max_size]'  # The maximum count of attack relations in the generated graphs. By default 'None'.</li>
  <li>'-m [mutation_intensity]'  # The count of mutations at each steps. By default '4'.</li>
  <li>'-h [heavy_mutation_intensity]'  # The count of additional mutations for agents affected by heavy mutations. By default '10'.</li>
  <li>'-x [extension]'  # The chosen extension (please refer to the section Extension). By default 'g'.</li>
  <li>'-t [train_test_ratio]'  # The ratio of data used for training. Remaining data are used for testing. By default '0.7'.</li>
  <li>'-n [noise_percent]'  # The percent of training data affected by artificial noise. By default '0'.</li>
  <li>'-i [numerical_interpolation]'  # The count of interval created for numerical attributes. By default '10'.</li>
  <li>'-p [population_size]'  # The count of agent in the population of the genetic algorithm. By default '10'.</li>
  <li>'-s [steps]'  # The count of learning steps.</li>
  <li>'--reduce'  # Toggle the forced reducing. By default already toggled.</li>
  <li>'--negation'  # Toggle the generation of negated arguments. By default 'False'.</li>
</ul>

<h2>Extensions:</h2><br>
<ul>
  <li>'g': Grounded
  <li>'p': Preferred</li>
</ul>

<h2>Dataset:</h2><br>
<p>Only in-use dataset are listed below. For more information, please refer to "src/datasets/[name]/*.names.txt" files.</p>
<ul>
  <li>#: [name]
  <li>0: Mushroom</li>
  <li>1: Voting</li>
  <li>2: Breast-cancer</li>
  <li>3: Heart-disease</li>
  <li>4: Car</li>
  <li>5: Brest-cancer-wisconsin</li>
</ul>
