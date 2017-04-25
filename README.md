# Simple workout #

Built with guidance from 

https://alexatutorial.com/flask-ask/
https://alexatutorial.com/2

It works with a unique skill name, e.g., 'engage workout'.

To run:

1. In first Terminal window:

	$ python workout.py

2. In second Terminal window:

	$ /Users/pezzutidyer/libraries/ngrok http 5000

3. Log in at https://developer.amazon.com. Go to the Alexa section, Alexa Skills set, Engage Workout skill, Configuration tab. For Service Endpoint Type, choose HTTPS and North America, and paste in the Forwarding URL from ngrok.

4. Go to http://echosim.io/ and test with the phrase 'Engage Workout'.


# Deploy and Beta Test #

https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa

Add a tester of your skill with these instructions.

https://developer.amazon.com/blogs/post/Tx2EN8P2AHAHO6Y/How-to-Add-Beta-Testers-to-Your-Skills-Before-You-Publish