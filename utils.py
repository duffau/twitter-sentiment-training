import regex as re

FLAGS = re.MULTILINE | re.DOTALL


def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = "<hashtag> {} <allcaps>".format(hashtag_body)
    else:
        result = " ".join(["<hashtag>"] + re.split(r"(?=[A-Z])", hashtag_body, flags=FLAGS))
    return result


def allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps>"


def tokenize(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "<url>")
    text = re_sub(r"/"," / ")
    text = re_sub(r"@\w+", "<user>")
    text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), "<smile>")
    text = re_sub(r"{}{}p+".format(eyes, nose), "<lolface>")
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), "<sadface>")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "<neutralface>")
    text = re_sub(r"<3","<heart>")
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "<number>")
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 <elong>")

    ## -- I just don't understand why the Ruby script adds <allcaps> to everything so I limited the selection.
    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", allcaps)
    text = re_sub(r"([A-Z]){2,}", allcaps)

    return text.lower()


if __name__ == "__main__":

    tweets = [
    '''#bitcoin #BITCOIN #bit_coin #BitCoin #BTCcoin''',
    '''RT @Lium__: $XVG #XVG #privacy #security in #crypto is one of the key drivers. #SatoshiNakamoto wanted it this way with #bitcoin #btc @just…''',
    '''George Soros Purchases Blockchain Know-how For $100 Million #Bitcoin #Blockchain #Dollar #GeorgeSoros #Million… https://t.co/d9SiyEaE7H''',
    '''Just make some passive income with digital currency #blockchain #cryptocurrency #bitcoin #ethereum #ico https://t.co/2OH78kqk7c''',
     '''What it feels like to earn #bitcoin on a daily basis with https://t.co/8MWoMSvwlk (Available on Google Play) #money… https://t.co/5sU90FPnR9''',
     '''"RT @MyLaLaWorld: LaLa World ties up with Komtec, #fintech powerhouse in Azerbaijan to introduce LaLa Wallet.  #blockchain #bitcoin #ICO #To…"''',
     '''RT @bisuguha: A little  surprise #ecc Coin See the image why grab #ecc from https://t.co/VFyj6fVsTe     #bitcoin #verge #siacoin #crypto #g…''',
     '''RT @ProfessorRipple: Tell 'em!   #trx #tron #xrp #ripple #ada #cardano #xlm #stellar #bitcoin #btc #crypto #blockchain https://t.co/N7gLhZ6…''',
     '''RT @ORACLEofETH: WOW almost at 20K!  If I get 20k followers by the end of today.... I will pump #Bitcoin to 100k  -Warren B.''',
     '''LAUNCHED &amp; LIVE! #bitcoin #cryptocurrency #blockchain news &amp; updates @TradrsNtwkDtBiz https://t.co/1EkVfPCs1b New from @TheTopTier''',
     '''LAUNCHED &amp; LIVE! #bitcoin #cryptocurrency #blockchain news &amp; updates @TradrsNtwkDtBiz https://t.co/uFmmy17QOn New from @TheTopTier''',
     '''LAUNCHED &amp; LIVE! #bitcoin #cryptocurrency #blockchain news &amp; updates @TradrsNtwkDtBiz https://t.co/qRb7nZ1d27 New from @TheTopTier''',
     '''RT @SimoneBlum: The latest Twitter Daily! https://t.co/BDBOHuH8Sr Thanks to @winhere #bitcoin #crypto''',
     '''RT @OracleofBTC: I'm about to airdrop 1 #Bitcoin to a lucky FOLLOWER RETWEET if you want it!  (ONLY followers of  @OracleofBTC qualify)  -W…''',
     '''"RT @Fx_Junkies: Tried trading #Bitcoin on #metatrader? Fully regulated, leverage, guaranteed stops and fixed spreads plus free bitcoin trad…"'''
    ]

    for tweet in tweets:
        print(tweet)
        print(tokenize(tweet))