from flask import Flask
import requests


app = Flask(__name__)


tweetsdb = [
    "Just got the latest smartphone, and it's mind-blowing! 📱 The camera quality is out of this world! #TechGeek #GadgetLover",
    "AI is revolutionizing the way we interact with technology. Excited to see how it continues to shape our future. #ArtificialIntelligence #TechTrends",
    "Exploring the beautiful streets of Kyoto, Japan today! 🏯 The blend of ancient temples and modern culture is captivating. #TravelJapan #Wanderlust",
    "Beach vibes and sunny skies in Bali! 🌞🏖️ Can't get enough of the breathtaking landscapes and warm hospitality. #TravelGoals #BaliLife",
    "Another day, another gym session! 💪 Crushing my fitness goals one workout at a time. #FitnessMotivation #GymLife",
    "Remember, progress takes time. Stay consistent and trust the process. You'll get there! #FitnessJourney #HealthyLifestyle",
    "Just had the most incredible sushi dinner! 🍣 The flavors were exquisite, and I can't wait to go back for more. #Foodie #SushiLover",
    "Tried a new recipe today, and it turned out to be a huge success! 😋 Nothing beats the joy of cooking and sharing delicious meals. #HomeCooking #FoodPorn",
    "Just finished reading 'The Great Gatsby,' and wow, what a classic! 📚 The symbolism and themes are so thought-provoking. #Bookworm #LiteraryMasterpiece",
    "Can't get enough of fantasy novels. Currently lost in a magical world full of dragons and wizards! 🐉🧙‍♂️ #FantasyFiction #ReadingAdventure"
]

interests = ['technology', 'food', 'movies']
# sen = input("Sentence: ")
def algorithm(tweetsdb):
    for i in tweetsdb:
        output = query({
            "inputs": i,
            "parameters": {"candidate_labels": interests}
        })
        for i in output['scores']:
            if (i > .7):
                print(output['sequence'])

def query(payload):
    API_TOKEN = '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'
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    algorithm(tweetsdb)
    # app.run()