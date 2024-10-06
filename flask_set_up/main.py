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
        
        result = f'Your overall sustainability score is {score} out of {len(grocery_list) * 10} ({(score / (len(grocery_list) * 10) * 100):.2f}% sustainable). Here are some suggestions to improve your score:<br>'
        result += '<br>'.join([s for s in suggestions if s is not None])
        
        return render_template_string("""
            <h1>Groceries for Good</h1>
            <p>{{ result|safe }}</p>
            <a href="/">Try Again</a>
        """, result=result)
    return render_template_string("""
        <h1>Groceries for Good</h1>
        <form method="POST">
            <textarea name="grocery_list" rows="10" cols="30" placeholder="Enter items each on their own line, using the format 'brand: item $price'"></textarea><br>
            <input type="submit" value="Calculate">
        </form>
    """)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
