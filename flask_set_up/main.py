from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

import sys
from collections import namedtuple

brands_scores = {
    "Lay's": 6,
    "Doritos": 6,
    "Pringles": 5,
    "Cheetos": 5,
    "Ritz": 6,
    "Kellogg's": 7,
    "General Mills": 8,
    "Post": 6,
    "Quaker": 7,
    "Cheerios": 8,
    "Land O'Lakes": 5,
    "DairyPure": 4,
    "Chobani": 8,
    "Yoplait": 7,
    "Horizon Organic": 9,
    "Coca-Cola": 5,
    "Pepsi": 6,
    "Gatorade": 5,
    "Tropicana": 6,
    "Lipton": 7,
    "Stouffer's": 5,
    "Birds Eye": 7,
    "Marie Callender's": 5,
    "Hot Pockets": 4,
    "Totino's": 4,
    "Heinz": 6,
    "Hellmann's": 6,
    "French's": 6,
    "Tabasco": 7,
    "Frank's RedHot": 6,
    "Pillsbury": 5,
    "Betty Crocker": 6,
    "Duncan Hines": 5,
    "McCormick": 8,
    "Jell-O": 5,
    "Wonder Bread": 4,
    "Pepperidge Farm": 6,
    "Arnold": 6,
    "Nature's Own": 7,
    "King's Hawaiian": 5,
    "Barilla": 8,
    "De Cecco": 7,
    "Ronzoni": 6,
    "Mueller's": 5,
    "Buitoni": 7,
    "Campbell's": 6,
    "Del Monte": 7,
    "Progresso": 6,
    "Bush's": 6,
    "Goya": 5,
    "Clorox": 6,
    "Tide": 5,
    "Lysol": 5,
    "Dawn": 6,
    "Mr. Clean": 5,
    "Seventh Generation": 9,
    "Ecover": 9,
    "Method": 9,
    "Patagonia Provisions": 9,
    "Nature's Path": 9,
    "Alter Eco": 9,
    "Dr. Bronner's": 9,
    "Beyond Meat": 9,
    "Amy's Kitchen": 9,
    "Ben & Jerry's": 8,
    "Tom's of Maine": 8,
    "Burt's Bees": 8,
    "Annie's Homegrown": 8,
    "Newman's Own": 8,
    "Nestlé": 3,
    "Unilever": 4,
    "Tyson Foods": 3,
    "Mondelez International": 4,
    "Mars": 4,
    "Keurig Dr Pepper": 3,
    "Reckitt Benckiser": 4,
    "Johnson & Johnson": 4,
    "Kraft Heinz": 4,
    "Cargill": 3,
    "Dole": 4,
    "Palmolive": 3,
    "Colgate": 4,
    "Red Bull": 3
}

Brand = namedtuple('Brand', ['name', 'score', 'suggestion'])

def get_suggestion(brand):
  suggestion = ""
  if brand == "Nestlé":
    suggestion = ("Nestlé: consider Oatly for a more sustainable approach to dairy alternatives" )
  elif brand == "Unilever":
    suggestion = ("Unilever: try Ethique, which offers zero-waste personal care products ")
  elif brand == "Tyson Foods":
    suggestion = ("Tyson Foods: Switch to Beyond Meat for plant-based protein options" )
  elif brand == "Modelez International":
    suggestion = ("Modelez International: Look into GreenTree for sustainable construction solutions." )
  elif brand == "Mars":
    suggestion = ("Mars: Explore Alter Eco for ethically sourced chocolate." )
  elif brand == "Keurig Dr Pepper":
    suggestion = ("Keurig Dr Pepper: Opt for Soma for eco-friendly coffee brewing solutions" )
  elif brand == "Reckitt Benckiser":
    suggestion = ("Recknitt Benckiser: Choose Ecover for biodegradable cleaning products." )
  elif brand == "Johnson & Johnson":
    suggestion = ("Johnson & Johnson: Consider Native for aluminum-free, sustainable personal care" )
  elif brand == "Kraft Heinz":
    suggestion = ("Kraft Heinz: Try Annie's for organic and sustainable packaged foods" )
  elif brand == "Cargill":
    suggestion = ("Cargill: Switch to Nutrien for more sustainable agricultural solutions" )
  elif brand == "Dole":
    suggestion = ("Dole: Consider Fruits & Roots for organic and locally sourced produce" )
  elif brand == "Palmolive":
    suggestion = ("Palmolive: Opt for Seventh Generation for eco-friendly dish and laundry soaps" )
  elif brand == "Colgate":
    suggestion = ("Colgate: Look into Bamboo Brush for a sustainable alternative to toothpaste and toothbrushes." )
  elif brand == "Red Bull":
    suggestion = ("Red Bull: Try RUNA for a natural energy drink made from guayusa leaves." )
  else:
    return None
  return suggestion

def import_brands_and_scores(brands_scores):
  brands = []
  for brand, score in brands_scores.items():
        suggestion = get_suggestion(brand)
        brand = Brand(name=brand, score=int(score), suggestion=suggestion)
        brands.append(brand)
  return brands

def import_brands_from_file(file_path):
  grocery_brand_names = []
  try:
    with open(file_path, 'r') as file:
      for line in file:
        brand_name, score = line.strip().split(':')
        grocery_brand_names.append(brand_name)
  except OSError:
    print('Invalid file name')
  return grocery_brand_names

def import_brands_from_list(grocery_list):
  grocery_brand_names = []
  for string in grocery_list:
      brand_name, score = string.strip().split(':')
      grocery_brand_names.append(brand_name)
  return grocery_brand_names

def calculate_score_and_get_suggestions(groceries, brands):
  score = 0
  suggestions = []
  for item in groceries:
    check = False
    for brand in brands:
      if item == brand.name:
        check = True
        score += brand.score
        suggestions.append(brand.suggestion)
        break
    if not check:
      print(f"{item} not included in database. Make sure the brand name is capitalized and contains punctuation (ex. Lays vs Lay's) \n")
  return score, suggestions

def main():
  brands_master_list = import_brands_and_scores(brands_scores)
  bad_input = True
  while bad_input:
    input_choice = input('How would you like to provide your list ("c" for copy and paste, "f" for file import)')
    if input_choice == "f":
      bad_input = False
      grocery_file = input('Enter the file name of your grocery list (.txt file, brands separated from items with a colon): ')
      grocery_list_brands = import_brands_from_file(grocery_file)
    elif input_choice == "c":
      bad_input = False
      print("Enter items each on their own line, using the format 'brand: item $price'. Type ctrl-d to stop")
      grocery_list = []
      try:
        while True:
          line = input()
          grocery_list.append(line.strip())
      except EOFError:
          print("Finished reading input.")
      grocery_list_brands = import_brands_from_list(grocery_list)
    else:
      print("invalid input")
  score, suggestions = calculate_score_and_get_suggestions(grocery_list_brands, brands_master_list)
  print(f'Your overall sustainability score is {score} out of {len(grocery_list_brands)*10} ({((score/(len(grocery_list_brands)*10))*100):.2f}% sustainable). Here are some suggestions to improve your score: \n')
  for suggestion in suggestions:
    if suggestion != None:
      print(suggestion)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        grocery_list = request.form["grocery_list"].splitlines()
        brands_master_list = import_brands_and_scores(brands_scores)
        grocery_list_brands = import_brands_from_list(grocery_list)
        score, suggestions = calculate_score_and_get_suggestions(grocery_list_brands, brands_master_list)
        percentage_score = (score / (len(grocery_list_brands) * 10)) * 100
        if percentage_score >= 80:
            message = "Great job! You're making sustainable choices."
        elif percentage_score >= 50:
            message = "You're on the right track, but there's room for improvement."
        else:
            message = "Let's work on making more sustainable choices."
        
        result = f'Your overall sustainability score is {score} out of {len(grocery_list) * 10} ({(score / (len(grocery_list) * 10) * 100):.2f}% sustainable). {message}<br>'
        result += 'Here are some suggestions to improve your score:<br>'
        result += '<br>'.join([s for s in suggestions if s is not None])
        
        return render_template_string("""
            <style>
                body {
                    background-color: #b2ffb2; /* Light green background */
                    color: #004d00; /* Dark green text */
                    font-family: 'Arial', sans-serif; /* Change font */
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-image: url('https://www.transparenttextures.com/patterns/white-paper.png'); /* Subtle texture */
                }
                .container {
                    text-align: center;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.9); /* White background with transparency */
                    position: relative; /* For positioning decorations */
                }
                h1 {
                    margin-bottom: 20px;
                    font-size: 2.5em;
                    color: #ff66b2; /* Pink accent for title */
                }
                p {
                    font-size: 1.2em;
                    margin-bottom: 20px;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 15px;
                    background-color: #ff66b2; /* Pink background */
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                }
                a:hover {
                    background-color: #e55a9b; /* Darker pink on hover */
                }
                textarea {
                    width: 100%;
                    max-width: 300px; /* Responsive textarea */
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    resize: none;
                    margin-top: 10px;
                }
                input[type="submit"] {
                    padding: 10px 15px;
                    border: none;
                    background-color: #004d00;
                    color: white;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                input[type="submit"]:hover {
                    background-color: #003300; /* Darker green on hover */
                }
                .decor {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                    z-index: -1;
                    background-image: url('https://www.transparenttextures.com/patterns/polkas.png'); /* Polka dots */
                    opacity: 0.2; /* Light polka dots */
                }
                .squiggly-line {
                    position: absolute;
                    top: 20px;
                    left: 0;
                    right: 0;
                    height: 20px;
                    background-image: url('https://upload.wikimedia.org/wikipedia/commons/3/3f/Squiggly_Line.svg'); /* Squiggly line */
                    background-repeat: repeat-x;
                }
                .circle {
                    position: absolute;
                    border-radius: 50%;
                    opacity: 0.6; /* Slight transparency */
                }
                .circle.dark-green {
                    background-color: #004d00; /* Dark green */
                }
                .circle.teal {
                    background-color: #008080; /* Teal */
                }
                /* Positioning circles */
                .circle1 {
                    width: 100px;
                    height: 100px;
                    top: -30px;
                    left: -50px;
                }
                .circle2 {
                    width: 80px;
                    height: 80px;
                    bottom: -40px;
                    right: -40px;
                }
                .circle3 {
                    width: 60px;
                    height: 60px;
                    top: 60px;
                    right: -30px;
                }
            </style>
            <div class="container">
                <div class="decor"></div>
                <div class="squiggly-line"></div>
                <div class="circle dark-green circle1"></div>
                <div class="circle teal circle2"></div>
                <div class="circle dark-green circle3"></div>
                <h1>Groceries for Good</h1>
                <p>{{ result|safe }}</p>
                <a href="/">Try Again</a>
            </div>
        """, result=result)
    
    return render_template_string("""
        <style>
            body {
                background-color: #b2ffb2; /* Light green background */
                color: #004d00; /* Dark green text */
                font-family: 'Arial', sans-serif; /* Change font */
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-image: url('https://www.transparenttextures.com/patterns/white-paper.png'); /* Subtle texture */
            }
            .container {
                text-align: center;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.9); /* White background with transparency */
                position: relative; /* For positioning decorations */
            }
            h1 {
                margin-bottom: 20px;
                font-size: 2.5em;
                color: #ff66b2; /* Pink accent for title */
            }
            form {
                margin-top: 20px;
            }
            textarea {
                width: 100%;
                max-width: 300px; /* Responsive textarea */
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                resize: none;
                margin-top: 10px;
            }
            input[type="submit"] {
                padding: 10px 15px;
                border: none;
                background-color: #004d00;
                color: white;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            input[type="submit"]:hover {
                background-color: #003300; /* Darker green on hover */
            }
            .decor {
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                z-index: -1;
                background-image: url('https://www.transparenttextures.com/patterns/polkas.png'); /* Polka dots */
                opacity: 0.2; /* Light polka dots */
            }
            .squiggly-line {
                position: absolute;
                top: 20px;
                left: 0;
                right: 0;
                height: 20px;
                background-image: url('https://upload.wikimedia.org/wikipedia/commons/3/3f/Squiggly_Line.svg'); /* Squiggly line */
                background-repeat: repeat-x;
            }
            .circle {
                position: absolute;
                border-radius: 50%;
                opacity: 0.6; /* Slight transparency */
            }
            .circle.dark-green {
                background-color: #004d00; /* Dark green */
            }
            .circle.teal {
                background-color: #008080; /* Teal */
            }
            /* Positioning circles */
            .circle1 {
                width: 100px;
                height: 100px;
                top: -30px;
                left: -50px;
            }
            .circle2 {
                width: 80px;
                height: 80px;
                bottom: -40px;
                right: -40px;
            }
            .circle3 {
                width: 60px;
                height: 60px;
                top: 60px;
                right: -30px;
            }
        </style>
        <div class="container">
            <div class="decor"></div>
            <div class="squiggly-line"></div>
            <div class="circle dark-green circle1"></div>
            <div class="circle teal circle2"></div>
            <div class="circle dark-green circle3"></div>
            <h1>Groceries for Good</h1>
            <form method="POST">
                <textarea name="grocery_list" rows="10" placeholder="Enter items each on their own line, using the format 'brand: item $price'"></textarea><br>
                <input type="submit" value="Calculate">
            </form>
        </div>
    """)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
