import requests
import openai
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


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

openai.api_key = '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'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = "your_secret_key"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



music = [
    "Classical music, a genre that spans centuries, offers profound, emotional experiences. From Beethoven to Vivaldi, its masters have profoundly shaped music.",
    "Rock 'n Roll began as a fusion of blues, country and jazz, defined by its rebellious spirit. Icons like The Beatles and Elvis Presley made it a global phenomenon.",
    "Jazz, born in New Orleans and spread through the Harlem Renaissance, has shaped music worldwide. Its improvisational style showcases the individuality of each musician.",
    "Pop music, marked by its catchy melodies, is designed to appeal to a broad audience. Artists like Michael Jackson and Madonna have left indelible marks on the genre.",
    "Hip-hop, originating from African and Latin American communities in the Bronx, has become a global force. It's a genre known for its rhythmic style and powerful messages."
]

sports = [
    "Basketball is a fast-paced sport that requires agility, precision and teamwork. It's played globally and has given rise to some of the world's most well-known athletes.",
    "Football, also known as soccer in some countries, is a game of strategy and skill. It's the most popular sport in the world, uniting fans of all ages and backgrounds.",
    "Tennis is a game of endurance and finesse. Players need to have strong hand-eye coordination and the ability to anticipate their opponent's moves. The Grand Slam tournaments are highly anticipated every year.",
    "Soccer, known as football in many parts of the world, is a sport that brings people together. From the World Cup to local club games, it inspires passion and camaraderie.",
    "Baseball, often known as America's pastime, is a sport that requires patience and strategic thinking. From the MLB to little league, it's a beloved part of American culture."
]

topic = {"music": music, "sports": sports}

interests = None


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    interests = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        global interests
        interests = request.form.get('interests')

        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('signup'))

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), interests=interests)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user_interests = current_user.interests.split(",")
    user_tweets = []
    for interest in user_interests:
        for img_num in range(5):
            user_tweets.append(generate_tweet(interest, str(img_num)))

    return render_template('dashboard.html', tweets=user_tweets)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# # sen = input("Sentence: ")
# def next_step():
#     wyd = input("What do you want to do? (Search or POST or Cancel): ")
#     if wyd == 'search':
#         interests = input("Search: ")
#         algorithm(tweetsdb, interests)
#     elif wyd == 'post':
#         post()
#     elif wyd == 'cancel':
#         print("Goodbye")
#     else:
#         next_step()
#
# def algorithm(tweetsdb, interests):
#     for i in tweetsdb:
#         output = query({
#             "inputs": i,
#             "parameters": {"candidate_labels": interests}
#         })
#         for i in output['scores']:
#             if (i > .7):
#                 print(output['sequence'])
#     next_step()
#
# def query(payload):
#     API_TOKEN = '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'
#     API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
#     headers = {"Authorization": f"Bearer {API_TOKEN}"}
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()
#
# def post():
#     new_post = input("Do you want to post? Y/N?: ")
#     if new_post == 'y' or new_post == "Y":
#         new_twt = input("Enter Tweet: ")
#         tweetsdb.append(new_twt)
#         next_step()
#     elif new_post == 'n' or new_post == "N":
#         next_step()


def generate_tweet(interest, img_num):
    img_url = url_for('static', filename=f'img/{interest+img_num}.jpg')
    return {"text": topic[interest][int(img_num)].strip(), "img_url": img_url}


@app.route('/explore', methods=['POST'])
def explore():
    interest = request.form.get('search')
    user_tweets = []
    for img_num in range(5):
        user_tweets.append(generate_tweet(interest, str(img_num)))
    return render_template('dashboard.html', tweets=user_tweets)

@app.route('/post', methods=['POST'])
def post():
    txt = request.form.get('tweet-txt')
    url = request.form.get('tweet-img')
    user_tweets = [{"text": txt, "img_url": url}]
    for img_num in range(5):
        user_tweets.append(generate_tweet(interests, str(img_num)))
    return render_template('dashboard.html', tweets=user_tweets)

# function to generate a tweet using GPT-3
# def generate_tweet(interest, img_num):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Write a tweet about {interest}.",
#         temperature=0.7,
#         max_tokens=280
#     )
#
#     # assuming you have images for each interest category in the /static/img/ directory
#     img_url = url_for('static', filename=f'img/{interest+img_num}.jpg')
#
#     return {"text": response.choices[0].text.strip(), "img_url": img_url}

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
