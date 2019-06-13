# Genetic Imaging
### A genetic algorithm that reproduces an image from scratch!
But why?
- It's a simple project of mine that was elaborated in about a day (but I will continue it cause it's really fun). These already exist, and there are tons on the internet that you can check out that are probably better than mine.
- Yea it's fun.
### Some examples
Since there are a few parameters that can be tweaked on, results may differ, and the bigger your population size and number of epochs, the longer it will take to generate the output image.
##### I believe this one took less than a minute.![cute cats](https://i.imgur.com/qizjBqO.png)
##### These roughly took, respectively: 0.5s, 2s, 5s, 9 min, 7 years (had to google it lol).![enter image description here](https://i.imgur.com/kvOxSII.png)
##### These one was just for curiosity sake: it took like 8 hours or so.![enter image description here](https://i.imgur.com/tMNEjqE.png)
You can experiment it yourself by changing the parameters and using your own images.
### How to run? It's quite simple :).
1. You can clone this repository by doing:

`https://github.com/thiagop-usp/Genetic-Imaging.git`

2. After that, you will need some python3 libraries, so you can run:

`pip3 install -r requirements.txt`

3. Then make sure you're running it with Python 3.7 (f-strings are the best):

`python3 genetic.py`

### Improvements yet to be done:
- Code is kind bad. It can be much better modularized.
- It's quite slow, some things can be changed when calculating the fitness.
- There are much better ways to reproduce the individuals (and some better ways to maintain good ones
- The idea of mutation is very important here, but I didn't use it.
- Make the progress and estimated time better to understand haha.
- Make it work to RGB as well. As of right now it's only grayscale, and if you tweak the code around it won't work.
