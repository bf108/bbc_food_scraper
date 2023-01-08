from bbc_food_scraper.bbc_scrape import (convert_url_to_soup,
                                         get_recipe_title,
                                         get_list_ingredient_tags,
                                         replace_frac_with_float,
                                         get_qty_unit,
                                         get_single_ingredient,
                                         get_ingredient_prep,
                                         get_cooking_time,
                                         get_prep_time,
                                         get_serving_portions,
                                         get_photo_url,
                                         get_method
                                         )

test_url = "https://www.utm.edu/staff/jlofaro/Joe%20Lofaro's%20Dive%20Shop%20Project/basic.html"

# url = "https://www.bbc.co.uk/food/recipes/easy_roast_chicken_and_73976"
url = "https://www.bbc.co.uk/food/recipes/donals_irish_beef_stew_85494"
soup = convert_url_to_soup(url)

def test_covert_url_to_soup():
    assert convert_url_to_soup(test_url).title.text == " The Most Basic Web Page in the World"

def test_get_recipe_title():
    assert get_recipe_title(soup) == 'Irish beef stew'

def test_get_list_ingredient_tags():
    #Only checking first and last ingredient in recipe
    ing_tags = get_list_ingredient_tags(soup)
    assert ing_tags[0].text.strip() == "2 tbsp vegetable oil"
    assert ing_tags[-1].text.strip() == "sea salt and freshly ground black pepper"

def test_replace_frac_with_float():
    ing_tags = get_list_ingredient_tags(soup)
    assert replace_frac_with_float(ing_tags[5]) == "1 litre/1.75pint beef stock (from stock cubes)"
    # assert replace_frac_with_float(ing_tags[-1]) == ".5 tsp soy sauce (preferably dark)"

def test_get_qty_unit():
    tag_text_list = [replace_frac_with_float(tag) for tag in get_list_ingredient_tags(soup)]
    expected = [("2",'tbsp'),
                ("1","kg"),
                ("2",""),
                ("3",""),
                ("4",""),
                ("1","litre"),
                ("900","g"),
                ("25","g"),
                ("","")]
    for text, exp in zip(tag_text_list, expected):
        assert get_qty_unit(text) == exp

def test_get_single_ingredient():
    tag_text_list = get_list_ingredient_tags(soup)
    expected = [
            "vegetable oil",
            "braising steak",
            "onions",
            "celery",
            "carrots",
            "beef stock",
            "potatoes",
            "butter",
            "black pepper",
            ]
    for text, exp in zip(tag_text_list, expected):
        assert get_single_ingredient(text) == exp

def test_get_ingredient_prep():
    tag_text_list = get_list_ingredient_tags(soup)
    expected = [
            "",
            "cut into 2.5cm/1in chunks",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ]
    for text, exp in zip(tag_text_list, expected):
        assert get_ingredient_prep(text) == exp

def test_get_cooking_time():
    assert get_cooking_time(soup) == '1 to 2 hours'

def test_get_prep_time():
    assert get_prep_time(soup) == 'less than 30 mins'

def test_get_serving_portions():
    assert get_serving_portions(soup) == 'Serves 6'

def test_get_photo_url():
    assert get_photo_url(soup) == 'https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/donals_irish_beef_stew_85494_16x9.jpg'

def test_get_method():
    
    expected = {1: "Preheat the oven to 200C/180C Fan/Gas 6. Place a large saucepan over a high heat, add 1 tablespoon of the oil and brown the beef in batches so the pan isn't too full. Remove the beef from the pan and set aside on a plate. Don't clean the pan, as you'll need it to fry the vegetables.",
    2: "While the beef is frying, peel and chop the onions and carrots and slice the celery.",
    3: "Heat the remaining oil in the same saucepan and fry the onion, celery and carrot for 4–5 minutes, or until the onions have softened. Scrape any cooked on bits from the bottom of the pan; this will add flavour to the stew. Season with salt and pepper.",
    4: "Mix the beef with the vegetables, then take the pan off the heat. Tip the meat and vegetables into a large ovenproof dish and pour the stock over the top.",
    5: "Peel and slice the potatoes into ½cm/¼in-thick slices and arrange over the top of the beef. Dot the butter over the top, then cover tightly with foil. Bake for 1 hour, then remove the foil and bake for a further 15 minutes, until the potatoes are crisp and golden-brown. Serve in deep bowls.",
    }
    assert get_method(soup) == expected