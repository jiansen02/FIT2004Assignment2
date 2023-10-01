# FIT2004Assignment2
This assignment was graded a High Distinction by my lecturer (19.5/20 marks total)

There were 2 seperate projects in this assignment. Both of which are in the "assignment2.py" file.

Project 1: Utilizing Residual Flow Networks for the maximum flow of throughput. 

Summary of Project 1 details: This code models a system which is able to process backups of data for a company to different
data centres. The code helps to ensure that the data backups are done as fast as possible by making sure the maximum amount 
of data is able to be processed within a span of time. This is done so by coding out concepts like Residual Networks and the
Ford-Fulkerson method.


Project 2: Utilizing auto-complete technology to create a word prediction model (similar to SMS autocomplete functions on phones).

Summary of Project 2 details: This code is meant to be a word prediction model to complete unfinished words. This is done so
by coding out Tries.

Appendix (below) - what the question paper in the assignment is:

Project 1 (optional to read for more information):

You are the system administrator responsible for processing the backups of your company and
the data needs to be backed up in different data centres. During certain times of the day you
have total control over your company’s data centres and their network connections, but you
need to process the backup requests as fast as possible.
Your company has D data centres represented by 0, 1, . . . , |D| − 1. And you have a list
connections of the direct communication channels between the data centres. connections is
a list of tuples (a, b, t) where:
• a ∈ {0, 1, . . . , |D|−1} is the ID of the data centre from which the communication channel
departs.
• b ∈ {0, 1, . . . , |D| − 1} is the ID of the data centre to which the communication channel
arrives.
• t is a positive integer representing the maximum throughput of that channel.
Regarding connections:
• You cannot assume that the communication channels are bidirectional.
• You can assume that for each pair of data centers there will be at most one direct communication channel in each direction between them.
• You can assume that for every data centre {0, 1, . . . , |D| − 1} there is at least one communication channel departing or arriving at that data centre.
• You cannot assume that the list of tuples connections is given to you in any specific
order.
• The number of communication channels |C| might be significantly less than (D|2), therefore
you should not assume that |C| = Θ(|D|2).

Moreover, each data centre has overall limits on the amount of incoming data it can receive
per second, and also on the amount of outgoing data it can send per second. maxIn is a list of
integers in which maxIn[i] specifies the maximum amount of incoming data that data centre
i can process per second. The sum of the throughputs across all incoming communication
channels to data centre i should not exceed maxIn[i]. Similarly, maxOut is a list of integers
in which maxOut[i] specifies the maximum amount of outgoing data that data centre i can
process per second. The sum of the throughputs across all outgoing communication channels
from data centre i should not exceed maxOut[i].

The backup request that you receive has the following format: it specifies the integer ID origin
∈ {0, 1, . . . , |D| − 1} of the data centre where the data to be backed up is located and a list
targets of data centres that are deemed appropriate locations for the backup data to be stored.
targets is a list of integers such that each integer i in it is such that i ∈ {0, 1, . . . , |D| − 1}
and indicates that backing up data to server i is fine. Regarding those inputs:
• You can assume that origin is not contained in the list targets.
• You cannot assume that the list of integers targets is given to you in any specific order,
but you can assume that it contains no duplicated integers.
• The data to be backed up can be arbitrarily split among the data centres specified in
targets and each part of the data only needs to be stored in one of those data centres.


Your task is to determine the maximum possible data throughput from the data centre origin
to the data centres specified in targets.
You should implement a function maxThroughput(connections, maxIn, maxOut, origin,
targets) that returns the maximum possible data throughput from the data centre origin to
the data centres specified in targets.


Project 2 (optional to read for more information):

Everyone is now talking about chatGPT. As amazing as it is, it is simply a well trained next
word prediction model, similar to how the auto-complete on your phone but on a larger scale on
the vast knowledge of the internet. In other words, chatGPT helps you finish your sandwiches
sentences. You recall learning Tries from FIT2004 which can also be used for auto-complete.
Thus, you set out to implement something similar using Tries.
Unfortunately, you do not have the computing power needed to process human language. Your
friend, Kim Katdashian who is a cat expert suggest doing a variant for cats because it is simpler.
She call this catGPT. The concept is simple – the model would be able to complete what does
a cat say automatically:
1. Let say Tabby the cat goes “meow meoow meow meowth...”.
2. Then catGPT will be able to complete Tabby’s sentence with “... meow meuw nyan”.
Kim states that there are a total of 26 words in a cat’s vocabulary. You realized that it is
possible to map this to the 26 letters in the English language. For example:
• meow = a
• meoow = b
• meuw = c
• meuuw = d
• meuow = e
• ...
• nyan = y
• meowth = z
In the example above, Tabby’s initial sentence could be viewed as abaz and then it is autocompleted to be acy. It is auto-completed this way because many many cats would finish their
sentence in such a way 1
. Luckily, Kim has collected a large set of cat sentences to help your
Trie decide how a cat sentence would be completed. These sentences are stored in a long list
of sentences, formatted as follows:
• abc
• abazacy
• dbcef
• gdbc
• abazacy
• xyz
• ...
• abazacy
• dbcef

