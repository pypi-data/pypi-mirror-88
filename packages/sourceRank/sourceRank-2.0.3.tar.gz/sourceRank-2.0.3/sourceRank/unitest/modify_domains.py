import pandas as pd
import itertools

data_path: str = "sourceRank/resources/resources_domains.csv"

df = pd.read_csv(data_path, index_col=0)

categories: list = list(itertools.chain.from_iterable(
    df[['media_focus']].values.tolist()))


def preprocess_category(category: str) -> str:
    res_category: str = category.lower()
    if category == "General Interest":
        res_category = "general"
    elif category == "Sport":
        res_category = "sports"
    elif category == "Science Tech" or category == "Agriculture":
        res_category = "science"
    elif category == "Shopper":
        res_category = "entertainment"
    return res_category


def get_category_mapping() -> dict:
    category_mapping: dict = {'science': 5,
                              'technology': 4,
                              'entertainment': 3,
                              'sports': 3,
                              'health': 4,
                              'general': 4,
                              'business': 4,
                              'religion': 2,
                              'ethnic': 3,
                              'military': 4,
                              'satire': 1,
                              'government': 5,
                              'alternative': 3}
    return category_mapping


def get_alternative_category_mapping() -> dict:
    category_mapping: dict = {'Agriculture': 4,
                              'Business': 4,
                              'Entertainment': 3,
                              'Ethnic': 3,
                              'Sport': 3,
                              'General Interest': 4,
                              'Government': 5,
                              'Religion': 2,
                              'Satire': 1,
                              'Alternative': 3,
                              'Science Tech': 5,
                              'Shopper': 2,
                              'Military': 4}
    return category_mapping


new_categories = [preprocess_category(i) for i in categories]
print(set(new_categories))

df.drop(["media_focus"], axis=1, inplace=True)
df["media_focus"] = new_categories

df.to_csv("resources_domain_v2.csv")


df_2 = pd.read_csv("resources_domain_v2.csv", index_col=0)