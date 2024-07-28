import pickle


class Cookie:
    def __init__(self, engine):
        self.engine = engine


    def save(self):
        pickle.dump(self.engine.get_cookies(), open("../settings/cookies", "wb"))


    def use(self):
        for cookie in pickle.load(open("../settings/cookies", "rb")):
            self.engine.add_cookie(cookie)
