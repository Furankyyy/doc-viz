# DocViz: An Interactive Document Visualization Tool with Sentence-BERT

This is the local version of DocViz. Since Sentence-BERT is fairly computationally intensive, I recommend people clone the repo and run it on there local machines. To view the webapp, please visit https://furankyyy.github.io/docviz/ or this [github repo](https://github.com/Furankyyy/docviz-web) (**Web app currently unavailable**). 

### What is it?

DocViz is a web app for you to visualize and inspect your documents. You can input up to 4 different documents. The model will compute the vector representation of each sentence in your document, and plot them in a 3D space.

### How to Use?

```git clone https://github.com/Furankyyy/doc-viz.git```

```pip install -r requirements.txt```

Then run:

```python app.py```

### How does it work?

If you want to know the full technical details, check the [How it works](https://furankyyy.github.io/docviz/how_it_works) page for the details, including what models I am using and **how to interpret the visualization**

### Why do you make it?

Traditional text mining tools mainly provides word-level, frequency based analyses, such as summary statistics of the document, word clouds, term frequency graphs, etc. I want to create a tool that utilizes state-of-the-art NLP models for text analysis. This visualization app is a step forward that focuses on sentence-level semantic information in input documents. It is designed for literature, humanities, and social science researchers and people who are interested in NLP to play around.

### Sample visualization

To demonstrate the advantage of DocViz over other traditional text visualizaton tool, let's look at a sample visualization generated by DocViz. The input data is the State of the Union Address (SOTU) by the United States President Cleveland in 1896 and Roosevelt in 1934. Cleveland and Roosevelt are both presidents that experienced a major economic crisis during their presidency. These are the SOTU when the recessions were almost over (1896 and 1934).

![](./sample.html)

If you rotate the graph and observe the result, you will see a cluster of you will see an enormous cluster of sentences on the right side. Those are a group of sentences mentioning NUMBERS and DATA in the speech. This information is otherwise unavailable in traditional word-level frequency-based word clouds, because each number is most likely to occur only one time (e.g. imported merchandise was “$369,757,470”). However, with the Sentence-BERT based DocViz, researchers can identify such semantic features of the data easily.
