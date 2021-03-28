from WebApp import app

if __name__ == "__main__":
    #nltk.download("stopwords")
    #nltk.download("punkt")
    app.run(debug=True, port=8080)