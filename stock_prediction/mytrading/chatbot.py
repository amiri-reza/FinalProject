import requests
import spacy
from mytrading.moving_average import MovingAverageDayTrading
import pandas as pd
import datetime
from spacy.matcher import PhraseMatcher


class ChatBotSpacy:
    def __init__(self, ticker, df, statement):

        self.ticker = ticker
        self.df = df
        self.statement = statement

    def chatbot(self):
        nlp = spacy.load("en_core_web_md")
        matcher = PhraseMatcher(nlp.vocab)
        # print(self.df)
        # now = datetime.datetime.now()
        current_price = self.df.iloc[-1, self.df.columns.get_loc("Adj Close")]
        current_volume = self.df.iloc[-1, self.df.columns.get_loc("Volume")]
        
        # open = df.iloc[0, df.columns.get_loc("open")]
        # current_price2 = df.iloc[1, df.columns.get_loc('Adj Close')]
        # print(current_price)
        # print(current_volume)



        qa_dict = {
            "asset price": f"This is the current asset price for the ticker {self.ticker.upper()} : {current_price}",
            "volume": f"This is the current volume for the ticker {self.ticker.upper()} : {current_volume}",
            # "volume": f"This is the current volume for the ticker {self.ticker.upper()} : {current_volume}",
        }

        # print("Noun phrases statement:", [chunk.text for chunk in statement.noun_chunks])
        # print("Verbs statement:", [token.lemma_ for token in statement if token.pos_ == "VERB"])
        terms = [question for question, answer in qa_dict.items()]

        patterns = [nlp.make_doc(question) for question in terms]
        matcher.add("TerminologyList", patterns)

        statement = nlp(self.statement)

        matches = matcher(statement)
        for match_id, start, end in matches:
            span = statement[start:end]

            if span.text:
                return qa_dict[f"{span.text}"]
                
        # min_similarity = 0.60
        # for key, value in qa_dict.items():
        #     question = nlp(key)

        #     # print("Noun phrases question:", [chunk.text for chunk in question.noun_chunks])
        #     # print("Verbs question:", [token.lemma_ for token in question if token.pos_ == "VERB"])

        #     if question.similarity(statement) >= min_similarity:
        #         # flag = True
        #         return value
        #     else:
        #         return "Sorry I don't understand that. Please rephrase your statement."


if __name__ == "__main__":

    # list = [
    #     "give me the asset price ",
    #     "give me the current volume ",
    # ]

    print("Hi! I am Trado, a trading bot :)")

    ticker = input("Please enter the ticker:")

    print("Thank you ! ")
    print("Please hold let me collect the data for you. ")

    average = MovingAverageDayTrading(
        ticker, df_retrieve=True, stop_loss=0.03, take_profit=0.15
    )

    df = average.moving_average_timeframes()
    print(df)
    # statement = "What is the current price "
    # for statement in list:
    #     response = ChatBotSpacy(ticker, df ,statement)
    #     print(response.chatbot())

    continue_chat = True
    statement = input(
        f"What information would you like to know regarding the ticker: {ticker.upper()}? "
    )
    while continue_chat:
        response = ChatBotSpacy(ticker, df, statement)

        if response.chatbot() != None:
            print(response.chatbot())
        else:
            print("Sorry I don't understand that. Please rephrase your statement.")
        
        continue_response = input(
            "Is there something else I can help you with? ( no : to exit) "
        )
        if continue_response.lower() == "no":
            continue_chat = False
            print("Thank you for communicating with Trado. Have a great day!")
            break
        else:
            statement = continue_response