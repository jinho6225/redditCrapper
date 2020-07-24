import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

app = Flask("reddit")

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/read")
def read():
  big_list = []
  target = request.args
  reading = ""
  for lang in list(target):
    reading += "r/" + lang + " "
    URL = f"https://www.reddit.com/r/{lang}/top/?t=month"
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find("div", {"class": "_1OVBBWLtHoSPfGCRaPzpTf"}).find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"})
    children = div.children
    for child in children:
      filtered_promoted = child.find("span", {"class": "_2oEYZXchPfHwcf9mTMGMg8"})
      if filtered_promoted is None:
        dic = {}
        vote = child.find("div", {"class":"_1E9mcoVn4MYnuBQSVDt1gC"})
        vote = vote.find("div", {"class":"_1rZYMD_4xY3gRcSS3p8ODO"}).string

        if "k" in vote:
          index = vote.index("k")
          vote = vote[0] + vote[index-1] + "00"

        title = child.find("h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).string
        link = child.find("a")["href"]
        dic["lang"] = lang
        dic["vote"] = int(vote)
        dic["title"] = title
        dic["link"] = link
        big_list.append(dic)

  sorted_by_vote = sorted(big_list, key = lambda i: i['vote'], reverse=True)

  return render_template("read.html",
  sorted_by_vote = sorted_by_vote,
  reading = reading
  )


app.run(host="0.0.0.0")
