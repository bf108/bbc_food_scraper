import requests
from bs4 import BeautifulSoup as bs4
from bs4.element import Tag
from typing import List, Union, Dict, Tuple
import re
from functools import reduce
import os
os.chdir('/Users/u1079317/Desktop/testdrivenio/bbc_food_scraper/')
# os.chdir(os.path.dirname(__file__))

from bbc_food_scraper.config import header, allowed_units

####################
#Handle Recipe Page
####################
def convert_url_to_soup(url: str) -> Union[bs4, ValueError]:
    resp = requests.get(url,headers=header)
    if resp.status_code == 200:
        return bs4(resp.content, 'html.parser')
    else:
        raise ValueError('Invalid URL')

def get_recipe_title(soup: bs4) -> str:
    return soup.find('h1',class_='gel-trafalgar content-title__text')\
        .text.strip().replace("'","").replace('’',"")

def get_list_ingredient_tags(soup: bs4) -> List[Tag]:
    return soup.find_all('li',class_="recipe-ingredients__list-item")

def replace_frac_with_float(tag: Tag) -> str:
    frac_map = {chr(188): ".25",
                chr(189): ".5",
                chr(190): ".75",
                '¼': ".25",
                '½': ".5",
                '¾': ".75"}
    tag_text = tag.text
    for k, v in frac_map.items():
        tag_text = tag_text.replace(k,v)
    return tag_text

def get_qty_unit(text: str) -> tuple[str,str]:
    #add leading zero to any substituted fractions
    if text[0] == ".":
        text = "0" + text
    text_list = re.split(' |/',text)
    if len(text_list) > 1 and text_list[1].lower() in allowed_units:
        qty, unit = text_list[0], text_list[1]
    else:
        try:
            qty, unit = re.search('(\d+\.?\d*)([a-z]*|[A-Z]*)',text).groups()
        except AttributeError:
            qty, unit = "", ""
    return qty, unit

def get_single_ingredient(tag: Tag) -> str:
    single_ing = ""
    try:
        return tag.find('a').text
    except AttributeError:
        return single_ing

def get_ingredient_prep(tag: Tag) -> str:
    full_text = tag.text
    return full_text.split(', ')[1].strip() if ', ' in full_text else ""

def get_cooking_time(soup: bs4) -> str:
    return soup.find('p',class_="recipe-metadata__cook-time").text

def get_prep_time(soup: bs4) -> str:
    return soup.find('p',class_="recipe-metadata__prep-time").text

def get_serving_portions(soup: bs4) -> str:
    return soup.find('p',class_="recipe-metadata__serving").text

def get_photo_url(soup: bs4) -> str:
    try:
        return soup.find('div',class_="recipe-media__image responsive-image-container__16/9").find('img')['src']
    except:
        try:
            return soup.find('div',class_="pre_play_layout_container").find('img')['src']
        except:
            return None

def get_method(soup: bs4) -> List[Tuple[int, str]]:
    m_lst = soup.find('ol',class_='recipe-method__list')
    return {i+1:step.text.strip() for i, step in
         enumerate(m_lst.find_all('li',class_='recipe-method__list-item'))}

def extract_qty_unit_ingredient(tag: Tag) -> Tuple[float, str, str]:
    ingredient = extract_single_ingredient(tag)
    full_text = tag.text
    text_minus_ing = text_without_ingredient(full_text, ingredient)
    print(text_minus_ing)
    qty, unit = extract_qty_unit(text_minus_ing)
    return qty, unit, ingredient

def collect_ingredients(soup: bs4) -> Dict:
    collected_ingredients = []
    tags = [ing_tag for ing_tag in get_list_ingredient_tags(soup)]
    tags_fmt = [replace_frac_with_float(ing_tag) for ing_tag in get_list_ingredient_tags(soup)]
    counter = 1
    for t, tf in zip(tags, tags_fmt):
        collected_ingredients.append({
            'item': get_single_ingredient(t),
            'quantity':get_qty_unit(tf)[0], 
            'unit':get_qty_unit(tf)[1], 
            'prep':get_ingredient_prep(t),
            'num': counter
            })
        counter += 1
    return collected_ingredients

def collect_entire_recipe_from_url(url: str) -> Dict:
    recipe_dict = {'title':None, 'cooking_time':None, 'prep_time':None, 'serving_portions':None, 'method':None, 'photo_url':None}
    functions_to_call = [get_recipe_title, get_cooking_time, get_prep_time, get_serving_portions, get_photo_url]
    soup = convert_url_to_soup(url)
    for k, f in zip(recipe_dict, functions_to_call):
        recipe_dict[k] = f(soup)
    recipe_dict['ingredients'] = collect_ingredients(soup)
    recipe_dict['method'] = get_method(soup)
    return recipe_dict

def get_recipe_cards_from_collection(url: str) -> list[Tag]:
    soup = convert_url_to_soup(url)
    return soup.find_all('div',class_='gel-layout__item gel-1/2 gel-1/3@m gel-1/4@xl')

def generate_recipe_url(url: str) -> str:
    return f"https://www.bbc.co.uk{url}"

def get_recipe_url_from_card(tag: Tag) -> str:
    return generate_recipe_url(tag.find_all('a')[0].get('href'))