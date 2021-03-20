from functools import singledispatch
import datetime
from os import close

import requests
import bs4
import collections
import pkg_resources
import sqlite3
import pickle
from tkinter import *
import os.path
import sys
import argparse
import logging
import yaml
import re

PATH_JOIN = os.path.join("tagcounter", "synonyms.yaml")

site = ""
tagDict = {}
today = datetime.date.today().strftime("%Y-%m-%d")
today_date_time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
tag_db_table = 'tag1.db'


def create_parser():
    get_parser = argparse.ArgumentParser(description="A list of args for tagcounter")
    get_parser.add_argument("--get", "--view", "--add", dest=site, help="Use get to get tag list")
    return get_parser


def init_logger():
    logging.basicConfig(level=logging.DEBUG, filename="tagcounter.log", format='%(asctime)s %(site)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger("tagcounter")
    logging.LoggerAdapter(logger, {"site": site})

    # file_handler = logging.FileHandler("tagcounter.log")
    # logger.addHendler(file_handler)
    # logger = logging.getLogger("tagcounter")


def main():
    """
    The main entry point of the tagcounter application
    """
    init_logger()
    parser = create_parser()
    if len(sys.argv) == 1:
        gui()
    elif sys.argv[1] == "--get":
        entered_site = str(sys.argv[2])
        tag_dict = get_tag_list(entered_site)
        print(tag_dict)
    elif sys.argv[1] == "--view":
        entered_site = str(sys.argv[2])
        tag_dict = retrieve_from_db(entered_site)
        print(tag_dict)
    elif sys.argv[1] == "--add":
        entered_site = str(sys.argv[2])
        write_to_db(entered_site)


if __name__ == '__main__':
    main()




def generate_log_file_name(site):
    return os.path.join(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), site)


log_file_name = generate_log_file_name(site)


def count_tag():
    input_site = str(entry.get())
    input_site = check_site_address(input_site)
    text.delete(1.0, END)
    if not input_site:
        text.insert(1.0, "Please, enter site!")
        label['background'] = "#ffaaaa"
        label['text'] = "Status: failed."
    else:
        tags = get_tag_list(input_site)
        text.insert(1.0, tags)
        label['background'] = "#aaffff"
        label['text'] = "Status: Success!"


def get_tag_list(site_address):
    global site
    site = site_address
    # init_logger()
    # logging.info("Start get_tag_list")
    html_list = requests.get(site)
    soap = bs4.BeautifulSoup(html_list.text, "html.parser")
    tag_default_dict = collections.defaultdict(int)
    for child in soap.recursiveChildGenerator():
        if child.name:
            tag_default_dict[child.name] += 1
    # logging.info("End get_tag_list")
    # logging.info("Go to write_to_db")
    write_to_db(site.split(":")[1].split(".")[0], site, tag_default_dict)

    return tag_default_dict


def load_from_db():
    text.delete(1.0, END)
    input_site = str(entry.get())
    input_site = check_site_address(input_site)
    if not input_site:
        text.insert(1.0, "Please, enter site address!")
        label['background'] = "#ffaaaa"
        label['text'] = "Status: failed."
    elif input_site == -1:
        manage_alias()
    else:
        tags_list = retrieve_from_db(input_site)
        if tags_list == 0:
            text.insert(1.0, "No such entry in the DB")
            label['background'] = "#ffaaaa"
            label['text'] = "Status: failed."
        else:
            text.insert(1.0, tags_list)
            label['background'] = "#aaffff"
            label['text'] = "Status: Success!"


def retrieve_from_db(site_address):
    global site
    site = site_address
    conn = sqlite3.connect(tag_db_table)
    c = conn.cursor()
    try:
        c.execute("SELECT tags FROM siteTags WHERE url LIKE ?", [(site)])
    except sqlite3.OperationalError as oe:
        print("sqlite3.OperationalError:", oe)
        return -1
    else:
        result = c.fetchall()
        if result:
            tags_tuple = result[0]
            tags_str = tags_tuple[0]
            unpickler_obj = pickle.loads(tags_str)
            return unpickler_obj
        else:
            print("No  such entry in DB")
            return 0


def write_to_db(site_name, site_address, tag_dictionary):
    global site
    site = site_name
    pickled_obj = pickle.dumps(tag_dictionary)
    sql_insert_command = "INSERT INTO siteTags VALUES('{0}','{1}','{2}',?)".format(site, site_address, today)
    conn = sqlite3.connect(tag_db_table)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS siteTags(site TEXT, url TEXT, date TEXT, tags blob)''')
    #     c.execute("SELECT tags FROM siteTags WHERE url LIKE ?", [(site)])
    except sqlite3.OperationalError as oe:
        print("sqlite3.OperationalError:", oe)
        return -1
    else:
    #     result = c.fetchall()
    # logging.info("Add new record to DB")
        c.execute(sql_insert_command, [sqlite3.Binary(pickled_obj)])
        conn.commit()
        conn.close()
    # logging.info(f"The new row was successfully added to DB for {site}")



# GUI
def gui():
    global entry, text, label
    window = Tk()
    entry = Entry(width=50)
    button = Button(text='Загрузить со страницы', command=count_tag, background="#87CEEB")
    button1 = Button(text='Показать из базы', command=load_from_db, background="#D8BFD8")
    text = Text(window, height=15)
    label = Label(window, text="Status", width=50, height=2, bg="grey", bd=10)
    entry.pack()
    button.pack()
    button1.pack()
    text.pack()
    label.pack()
    return window.mainloop()


def delete_vowel():
    pass


def check_site_address(input_site):
    # delete spaces
    input_site = input_site.lstrip().strip()
    # check if only spaces were input
    if not input_site:
        return None
    # check whether input_site is url or synonym
    elif input_site.find(".") != -1:
        # if url, check/add http and return site url
        input_site = check_http_in_address(input_site)
        return input_site
    else:
        with open(PATH_JOIN, 'r') as synonyms:
            yaml_data = yaml.safe_load(synonyms)
            if yaml_data[input_site]:
                yaml_site = yaml_data[input_site]
                yaml_site = check_http_in_address(yaml_site)
                return yaml_site
            else:
                return -1


def check_http_in_address(input_site):
    if not input_site.startswith("http://"):
        input_site = "http://" + input_site
    return input_site


def manage_alias():
    global entry1, entry2, txt
    window = Tk()
    window.title("Add synonym")

    frame1 = Frame(window)
    frame1.pack(fill=X)

    lbl1 = Label(frame1, text="Enter site alias", width=20)
    lbl1.pack(side=LEFT, padx=5, pady=5)

    entry1 = Entry(frame1)
    entry1.pack(fill=X, padx=5, expand=True)

    frame2 = Frame(window)
    frame2.pack(fill=X)

    lbl2 = Label(frame2, text="Enter site address", width=20)
    lbl2.pack(side=LEFT, padx=5, pady=5)

    entry2 = Entry(frame2)
    entry2.pack(fill=X, padx=5, expand=True)

    frame3 = Frame(window)
    frame3.pack(fill=Y)

    button1 = Button(frame3, text="Add alias", command=add_synonym, bg="#aaffff", width=15)
    button1.pack(side=LEFT, padx=20, pady=5)

    button2 = Button(frame3, text="Delete alias", command=delete_synonym, bg="#ffaaaa", width=15)
    button2.pack(side=LEFT, padx=20, pady=5)

    button3 = Button(frame3, text="Check synonym list", command=return_synonym_list, bg="#87CEFA", width=15)
    button3.pack(side=LEFT, padx=20, pady=5)

    frame4 = Frame(window)
    frame4.pack(expand=True)

    lbl4 = Label(frame4, text="List of available aliases", width=20)
    lbl4.pack(fill=Y, side=LEFT, anchor=N, padx=5, pady=5)

    txt = Text(frame4)
    txt.pack(fill=BOTH, pady=5, padx=5, expand=True)

    return window.mainloop()


def add_synonym():
    txt.delete(1.0, END)
    synonym_name = str(entry1.get())
    synonym_name = synonym_name.lstrip().strip()
    synonym_url = str(entry2.get())
    synonym_url = synonym_url.lstrip().strip()
    if len(synonym_name) == 0:
        txt.insert(1.0, "Please, enter site alias")
    elif len(synonym_url) == 0:
        txt.insert(1.0, "Please, enter site url")
    elif check_url(synonym_url) == -1:
        txt.insert(1.0, "You have entered a wrong url")
    else:
        with open(PATH_JOIN, "r+") as synonyms:
            yaml_dict = yaml.safe_load(synonyms)
            if not (synonym_name in yaml_dict):
                new_map = {synonym_name: synonym_url}
                yaml.safe_dump(new_map, synonyms)
                with open(PATH_JOIN, "r+") as up_synonyms:
                    yaml_dict1 = yaml.safe_load(up_synonyms)
                    dict_list = convert_map_to_str(yaml_dict1)
                    txt.insert(1.0, dict_list)
            else:
                txt.insert(1.0, "There is such alias in the synonym file: \n" + convert_map_to_str(yaml_dict))


def convert_map_to_str(dict_to_convert):
    dict_list = ""
    for key, value in dict_to_convert.items():
        dict_list += f"{key}: {value} \n"
    return dict_list


def return_synonym_list():
    global PATH_JOIN
    txt.delete(1.0, END)
    with open(PATH_JOIN, "r+") as synonyms:
        yaml_dict = yaml.safe_load(synonyms)
        dict_list = convert_map_to_str(yaml_dict)
        txt.insert(1.0, dict_list)


def delete_synonym():
    txt.delete(1.0, END)
    synonym_name = str(entry1.get())
    if len(synonym_name.strip().lstrip()) > 0:
        with open(PATH_JOIN, "r+") as synonyms:
            yaml_dict = yaml.safe_load(synonyms)
        if synonym_name in yaml_dict:
            yaml_dict.pop(synonym_name)
            with open(PATH_JOIN, "w") as up_synonyms:
                yaml.safe_dump(yaml_dict, up_synonyms)
        dict_list = convert_map_to_str(yaml_dict)
        txt.insert(1.0, dict_list)
    else:
        txt.insert(1.0, "Please, enter alias you want to delete")


def check_url(url):
    match = re.fullmatch(r'[-\w+\d+]+.+[-\w+\d+]', r'%s' % url)
    print('YES' if match else 'NO')


match12 = re.fullmatch(r'[\w+\d+]+.+[-\w+\d+]', r'123')
print('YES' if match12 else 'NO')



