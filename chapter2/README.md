## Introduction to Dask

Dask is an open-source framework that enables parallelization of Python code. This can be applied to all kinds of Python use cases, not just machine learning. Dask is designed to work well on single-machine setups and on multi-machine clusters. You can use Dask with pandas, NumPy, scikit-learn, and other Python libraries. 

* Delayed or Lazy Evaluation

Delaying a task with Dask can queue up a set of transformations or calculations so that it's ready to run later, in parallel. This is what's known as "lazy" evaluation - it won't evaluate the requested computations until explicitly told to. This differs from other kinds of functions, which compute instantly upon being called. Many very common and handy functions are ported to be native in Dask, which means they will be lazy (delayed computation) without you ever having to even ask.

However, sometimes you will have complicated custom code that is written in pandas, scikit-learn, or even base python, that isn't natively available in Dask. Other times, you may just not have the time or energy to refactor your code into Dask, if edits are needed to take advantage of native Dask elements. If this is the case, you can decorate your functions with @dask.delayed, which will manually establish that the function should be lazy, and not evaluate until you tell it. You'd tell it with the processes .compute() or .persist(), described in the next section. We'll use @dask.delayed several times in this workshop to make PyTorch tasks easily parallelized.


* Native Dask libraries and functions

https://dask.org/

* Initializing computation

Lots of new users of Dask find the .persist() and .compute() processes confusing. This is understandable! But the answer is not as hard as you might think.

First, remember we have several machines working for us right now. We have our Jupyter instance right here running on one, and then our cluster of worker machines also.

If we use .compute(), we are asking Dask to take all the computations and adjustments to the data that we have queued up, and run them, and bring it all to the surface here, in Jupyter. That means if it was distributed we want to convert it into a local object here and now. If it's a Dask Dataframe, when we call .compute(), we're saying "Run the transformations we've queued, and convert this into a pandas dataframe immediately." If our data is too big to be held in local pandas memory, this can be a disaster! But if it is small, then we might be fine.

If we use .persist(), we are asking Dask to take all the computations and adjustments to the data that we have queued up, and run them, but then the object is going to remain distributed and will live on the cluster, not on the Jupyter instance. So when we do this with a Dask Dataframe, we are telling our cluster "Run the transformations we've queued, and leave this as a distributed Dask Dataframe."

So, if you want to process all the delayed tasks you've applied to a Dask object, either of these methods will do it. The difference is where your object will live at the end.



* Communicating with a machine cluster in Dask

Another important element to discuss before we start hands on work is the interaction between our Jupyter instance and our Dask cluster. When we use the @dask.delayed decorator, we queue up some work and put it in a list, ready to be run. So how do we send it to the workers and explain what we want them to do?

For this, we need the distributed module from Dask. We make our connection to the Client (you saw this in Notebook 1), and then our Jupyter instance is prepared to communicate with the cluster.

We will use a few processes to do this communication: .submit() and .map().

.submit() lets us send one task to the cluster, to be run once on whatever worker is free
.map() lets us send lots of tasks, which will be disseminated to workers in the most efficient way.
There's also .run() which you can use to send one task to EVERY worker on the cluster simultaneously. This is only used for small utility tasks, however - like installing a library or collecting diagnostics.
For the work we are doing in the rest of this workshop, we'll use .map() in this way:

futures = client.map(function, image_batches)

This takes our function, maps it over all the batches of images we're going to create, and then these tasks are distributed to the cluster workers. Note: they still won't actually compute yet! Our function is delayed, so it's just out there on the workers ready to go when we say. futures is a list of pointers to these tasks that we can use to send that command.

We have one more step before we use .compute(), which is .gather(). This creates one more instruction to be included in this big delayed job we're establishing: retrieving the results from all of our jobs. It's going to sit tight as well until we finally say .compute().

futures_gathered = client.gather(futures)

It may help to think of all the work as instructions in a list. We have so far told our cluster: "map our delayed function over this list of inputs, and pass the resulting tasks to the workers", "Gather up the results of those tasks, and bring them back". But the one thing we haven't said is "Ok, now begin to process all these instructions"! That's what .compute() will do. For us this looks like:

futures_computed = client.compute(futures_gathered, sync=False)