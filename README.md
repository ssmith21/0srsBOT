# OpenCV 0ld School Runescape Bot!

### Quick Disclaimer: 
Use of bots is against the rules in OSRS. I do not endorse cheating; this bot is purely a personal project and I accept that my account may be banned if caught. I have therefor removed and obscurified important parts of the code to prevent people from quickly downloading and using the bot to gain an in-game advantage. 

### About the game
This game is an online MMORPG played on mouse and keyboard. Part of playing the game is training various skills in order to level up. There are many way to train each skill and levelling up each skill leads to the player's account gaining access to more content of the game. To find out more or to play the game, visit https://oldschool.runescape.com/ .

# About the bot
This but uses an open source computer vision software "OpenCV" to detect objects on the screen. A python class is used to continuously capture screenshots, where the screenshots are passed to the OpenCV API to detect certain objects on screen. We can call this process the "Vision" process.
## Here's an example of detecting rocks used to train the mining skill!
![Object detection without filtering](gifs/4.gif)
In order to reduce visual noise and increase the performance of the Vision, an colour filter can be applied to each screenshot. This improves bot performance by allowing the OpenCV API to detect the on-screen objects with more ease since there is less visual noise. Although each screenshot must be processed, if filtered correctly, the framerate can actually increase in addition having more accurate object detection.
## My character can appear to be the only object on screen with less than a minute of manual filtering!
 ![Drowning out noise using HSV filter](gifs/2.gif)

![Alt text](gifs/1.gif)

![Alt text](gifs/3.gif)


![Alt text](gifs/5.gif)
