
def states_mean_request(data, df):
    """
    Calculez media pentru fiecare stat pentru o intrebare data.
    
    Args:
        data (dict): Un dictionar care contine lista de intrebari.
        df (pd.DataFrame): DataFrame-ul care contine datele.
    """

    # extrag intrebarea
    question = data["question"]

    # filtrez datele in functie de intrebare si ani
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) &
                     (df["YearEnd"] <= 2022)]

    # grupez datele dupa stat si calculez media
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    # sortez rezultatul in functie de media calculata
    result = result.sort_values(by="Mean", ascending=True)

    # creez un dictionar cu rezultatul
    result_dict = dict(zip(result["State"], result["Mean"]))

    return result_dict

def state_mean_request(data, df):
    """
    Calculez media pentru o intrebare data pentru un stat dat.  
    """
    # extrag intrebarea si statul
    question = data["question"]
    state = data["state"]

    # filtrez datele in functie de intrebare, stat si ani
    filtered_df = df[(df["Question"] == question) &
                     (df["State"] == state) &
                     (df["Year"] >= 2011) &
                     (df["YearEnd"] <= 2022)]

    # grupez datele dupa stat si calculez media
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    # convertesc rezultatul intr-un dictionar
    result_dict = dict(zip(result["State"], result["Mean"]))

    return result_dict

def best5_request(data, df, questions_best_is_min):
    """
    Calculez media pentru fiecare stat pentru o intrebare data si returnez
    primele 5 state.
    """
    # extrag intrebarea
    question = data["question"]

    # filtrez datele in functie de intrebare si ani
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) &
                     (df["YearEnd"] <= 2022)]

    # grupez datele dupa stat si calculez media
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    # verific daca intrebarea este una care trebuie sa fie minima
    # si sortez rezultatul in functie de media calculata
    if question in questions_best_is_min:
        result = result.sort_values(by="Mean", ascending=True)
    else:
        result = result.sort_values(by="Mean", ascending=False)

    # iau primele 5 rezultate
    top5 = result.head(5)

    # creez un dictionar cu rezultatul
    result_dict = dict(zip(top5["State"], top5["Mean"]))

    return result_dict

def worst5_request(data, df, questions_best_is_min):
    """
    Calculez media pentru fiecare stat pentru o intrebare data si returnez
    ultimele 5 state.
    """
    # extrag intrebarea
    # filtrez datele in functie de intrebare si ani
    question = data["question"]
    filtered_df = df[(df["Question"] == question) &
                        (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    # grupez datele dupa stat si calculez media
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    # verific daca intrebarea este una care trebuie sa fie minima
    # si sortez rezultatul in functie de media calculata
    if question in questions_best_is_min:
        result = result.sort_values(by="Mean", ascending=False)
    else:
        result = result.sort_values(by="Mean", ascending=True)

    # iau ultimele 5 rezultate
    top5 = result.head(5)

    # creez un dictionar cu rezultatul
    result_dict = dict(zip(top5["State"], top5["Mean"]))

    return result_dict

def global_mean_request(data, df):
    """
    Calculez media globala pentru o intrebare data.
    """

    # extrag intrebarea
    # filtrez datele in functie de intrebare si ani
    question = data["question"]
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    # calculez media globala
    mean_value = filtered_df["Value"].mean()
    return {"global_mean": mean_value}

def diff_from_mean_request(data, df):
    """
    Calculez diferenta fata de media globala pentru o intrebare data. 
    Pentru fiecare stat.
    """

    # extrag intrebarea
    # filtrez datele in functie de intrebare
    question = data["question"]
    filtered_df = df[df["Question"] == question]

    # iau fiecare stat
    states = filtered_df["State"].unique()
    diffs = {}

    # parcurg fiecare stat si calculez diferenta fata de media globala
    for state in states:
        state_data = {'question': question, 'state': state}
        diff = state_diff_from_mean_request(state_data, df)
        diffs.update(diff)  # Adăugăm diferența în dicționar

    # rezultatul este un dictionar cu diferentele
    sorted_diffs = dict(sorted(diffs.items(), key=lambda item: item[1], reverse=True))

    return sorted_diffs



def state_diff_from_mean_request(data, df):
    """
    Calculez diferenta fata de media globala pentru o intrebare data
    pentru un stat dat.
    """
    # extrag intrebarea si statul
    # filtrez datele in functie de intrebare, stat si ani
    question = data["question"]
    state = data["state"]
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    # calculez media globala si media pentru statul dat
    global_mean = filtered_df["Value"].mean()
    state_mean = filtered_df[filtered_df["State"] == state]["Value"].mean()

    # calculez diferenta
    return {
        state: global_mean - state_mean
    }

def mean_by_category_request(data, df):
    """
    Calculate the mean of the given questions for each state and category.
    """
    # extrag intrebarea
    # filtrez datele in functie de intrebare si ani
    question = data["question"]
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    # grupez datele dupa stat si stratificare
    # calculez media
    grouped = filtered_df.groupby(["State", "StratificationCategory1",
                                   "Stratification1"])["Value"].mean().reset_index()
    # pastrez doar coloanele necesare
    grouped.columns = ["State", "Category", "Segment", "Mean"]

    # dictionarul rezultat va avea ca cheie un tuple (State, Category, Segment)
    # si ca valoare media
    result_dict = {}
    for _, row in grouped.iterrows():
        key = str((row['State'], row['Category'], row['Segment']))
        result_dict[key] = row["Mean"]

    return result_dict

def state_mean_by_category_request(data, df):
    """
    Calculate the mean of the given questions for a specific state and category.
    """
    # extrag intrebarea si statul
    # filtrez datele in functie de intrebare, stat si ani
    question = data["question"]
    state = data["state"]
    filtered_df = df[
        (df["Question"] == question) &
        (df["Year"] >= 2011) & (df["YearEnd"] <= 2022) &
        (df["State"] == state)
    ]

    # grupez datele dupa stratificare
    # calculez media
    grouped = filtered_df.groupby(["StratificationCategory1",
                                   "Stratification1"])["Value"].mean().reset_index()

    # pastrez doar coloanele necesare
    grouped.columns = ["Category", "Segment", "Mean"]

    # dictionarul rezultat va avea ca cheie un tuple (Category, Segment)
    # si ca valoare media
    result_dict = {}
    for _, row in grouped.iterrows():

        key = str((row["Category"], row["Segment"]))
        result_dict[key] = row["Mean"]

    return {state: result_dict}
