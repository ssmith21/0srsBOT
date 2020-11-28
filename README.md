# OpenCV Old School Runescape Bot!

### Quick Disclaimer: 
Use of bots is against the rules in OSRS. This bot is purely a coding exercise and I have therefor removed and obscurified important parts of the code to prevent people from quickly downloading and using the bot to gain an in-game advantage. 

### About the game
This game is an online MMORPG played on mouse and keyboard. Part of playing the game is training various skills in order to level up. There are many way to train each skill and levelling up each skill leads to the player's account gaining access to more content of the game. To find out more or to play the game, visit https://oldschool.runescape.com/ .

# About the bot
This bot uses an open source computer vision software "OpenCV" to detect objects on the screen and train specific skills. A python class is used to continuously capture screenshots, where the screenshots are passed to the OpenCV API to detect certain objects on screen. We can call this process the "Vision" process.
## Here's an example of detecting rocks used to train the mining skill!
![Object detection without filtering](gifs/4.gif)
In order to reduce visual noise and increase the performance of the "Vision", a colour filter can be applied to each screenshot using the HSVFilter class. This improves "Vision" performance by allowing the OpenCV API to more easily detect the on-screen objects since there is less visual noise. Although each screenshot must be processed, if filtered correctly, the framerate can actually increase in addition having more accurate object detection.
 ## In less than 60, we can filter out all objects except my character!
 ![Drowning out noise using HSV filter](gifs/2.gif)
Once we've filtered out what we need on screen, we need the bot to actually interact with the game. We can call this process the "Movement" process. The "Movement" must also mimic human movement, otherwise the game's bot-detection system could mark the account as a bot. Since it is unkown to players how the bot-detection system works, it is up to the programmer to make assumptions as to what will trigger the anit-botting system. So how does the bot play the game? The "Vision" process returns a list of points to click on displayed as crosshairs. These points on the pixel coordinates on your monitor which display the in game objects to detect. The "Vision" and "Movement" process run in parallel using multiprocessing, therefor this bot requires the atleast 2 cores. A custom object is used to implement Points which are passed to a shared Array which both processes interact with. This bot is also scalable to different skills. As long as there's a pattern in training the skill, this bot should work!
## Here are some action shots of the bot training 3 different skills!
On the left is what the bot sees, on the right is what the user sees; the use is not interacting with the computer at all.
![Aerial fishing](gifs/1.gif)
![Mining](gifs/3.gif)
![Woodcutting](gifs/5.gif)

## Future plans.
GUI to start the bot
A wizard to help setup the movement speed
Machine learning image detection
