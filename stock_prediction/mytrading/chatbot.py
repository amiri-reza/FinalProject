import spacy
from spacy.matcher import PhraseMatcher


class ChatBotSpacy:
    def __init__(self, ticker, df, statement):
        self.ticker = ticker
        self.df = df
        self.statement = statement

    def chatbot(self):
        nlp = spacy.load("en_core_web_md")
        matcher = PhraseMatcher(nlp.vocab)
        current_price = self.df.iloc[-1, self.df.columns.get_loc("Adj Close")]
        current_volume = self.df.iloc[-1, self.df.columns.get_loc("Volume")]
        qa_dict = {
            "asset price": f"This is the current asset price for the ticker {self.ticker.upper()} : {current_price}",
            "volume": f"This is the current volume for the ticker {self.ticker.upper()} : {current_volume}",
        }

        terms = [question for question, answer in qa_dict.items()]
        patterns = [nlp.make_doc(question) for question in terms]
        matcher.add("TerminologyList", patterns)
        statement = nlp(self.statement)
        matches = matcher(statement)
        for match_id, start, end in matches:
            span = statement[start:end]

            if span.text:
                return qa_dict[f"{span.text}"]
