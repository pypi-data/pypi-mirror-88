import itertools
import pandas as pd
from newsapi import NewsApiClient
from newsapi.const import categories
from sourceRank.helper.settings import (logger, default_field,
                                        resources_domains_filename,
                                        resources_directory)
from sourceRank.helper.utils import (get_best_matching_candidate_from_list,
                                     get_nationality_from_country_code,
                                     get_fuzzy_matching_sort_ratio, parse_url,
                                     get_main_language_code_from_country_code,
                                     load_resources_from_csv)
from sourceRank.models.source_credibility_models import NewsAPISourceDoc


class NewsAPIConnector(object):
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.news_api: NewsApiClient = NewsApiClient(
            api_key=self.api_key)
        self.resources_dir: str = resources_directory
        self.dataset_filename: str = resources_domains_filename
        self.df_resources: pd.DataFrame = self.get_media_dataset_from_resources(
            resources_dir=self.resources_dir,
            filename=self.dataset_filename)

    def get_categories_from_resource_dataset(self):
        return list(set(list(itertools.chain.from_iterable(
            self.df_resources[['media_focus']].values.tolist()))))

    def get_source_categories(self) -> list:
        return categories + self.get_categories_from_resource_dataset()

    def get_sources_from_news_api(self, category: str = None, country_code: str = None,
                                  language: str = None) -> list:
        sources: list = []
        try:
            response_api: dict = self.news_api.get_sources(
                category=category, country=country_code, language=language)
            sources: list = response_api.get("sources", [])
        except Exception as e:
            logger.error(e)
        return sources

    def get_everything_from_news_api(self, q: str,sources: str,
                                     domains: str,from_param: str,
                                     to: str, language: str,
                                     sort_by: str = 'relevancy',
                                     page: int = 2) -> dict:
        all_articles: dict = {}
        try:
            all_articles: dict = self.news_api.get_everything(
                q=q,
                sources=sources,
                domains=domains,
                from_param=from_param,
                to=to,
                language=language,
                sort_by=sort_by,
                page=page)
        except Exception as e:
            logger.error(e)
        return all_articles

    def get_source_matching_from_url(self, candidate_source: str, category: str = None,
                                     country_code: str = None, language: str = None,
                                     matching_threshold: int = 95) -> NewsAPISourceDoc:
        source_matching: NewsAPISourceDoc = object.__new__(NewsAPISourceDoc)
        try:
            sources: list = self.get_sources_from_news_api(
                category=category, country_code=country_code, language=language)

            # Get matching index
            res_source_matching: tuple = get_best_matching_candidate_from_list(
                candidate=candidate_source, matching_options=sources)

            # Verify matching
            source_matching_obj: dict = res_source_matching[0]
            matching_item: str = parse_url(source_matching_obj.get("url")).fqdn
            res_matching_verification: float = get_fuzzy_matching_sort_ratio(
                input_query=candidate_source,
                matching_item=matching_item)

            # 2. Retrieve index
            if res_matching_verification > matching_threshold:
                source_matching_obj: dict = res_source_matching[0]

                source_matching: NewsAPISourceDoc = NewsAPISourceDoc(
                    id=source_matching_obj.get("id"),
                    name=source_matching_obj.get("name"),
                    description=source_matching_obj.get("description"),
                    url=source_matching_obj.get("url"),
                    category=source_matching_obj.get("category"),
                    language=source_matching_obj.get("language"),
                    country=source_matching_obj.get("country"),
                    nationality=get_nationality_from_country_code(
                        source_matching_obj.get("country")),
                    analysed=True)
            else:
                # Try to retrieve the data from resources
                source_matching: NewsAPISourceDoc = self.get_media_information_from_resources(
                    candidate_source=candidate_source, matching_threshold=matching_threshold)
        except Exception as e:
            logger.error(e)
        return source_matching

    def get_media_information_from_resources(self, candidate_source: str, matching_threshold: int = 95):
        source_matching: NewsAPISourceDoc = object.__new__(NewsAPISourceDoc)
        try:
            matching_elements_fqdn: list = list(itertools.chain.from_iterable(
                self.df_resources[['fqdn']].values.tolist()))
            res_source_matching: tuple = get_best_matching_candidate_from_list(
                candidate=candidate_source, matching_options=matching_elements_fqdn)

            if res_source_matching[1] > matching_threshold:
                res_df: dict = self.df_resources[self.df_resources["fqdn"] == res_source_matching[0]]

                # URL
                url = res_df["domain"].values.tolist()[0]

                # Name
                name: str = list(itertools.chain.from_iterable(
                    res_df[['name']].values.tolist()))[0]

                # Category
                category: str = list(itertools.chain.from_iterable(
                    res_df[['media_focus']].values.tolist()))[0]

                # country
                country_code: str = res_df["country_code"].values.tolist()[0]

                # language
                language: str = get_main_language_code_from_country_code(
                    country_code=country_code)

                source_matching: NewsAPISourceDoc = NewsAPISourceDoc(
                    id=name.replace(" ", "-").lower(),
                    name=name,
                    description="",
                    url=url,
                    category=category,
                    language=language,
                    country=country_code,
                    nationality=get_nationality_from_country_code(
                        country_code),
                    analysed=True)
            else:
                source_matching: NewsAPISourceDoc = NewsAPISourceDoc(
                    id=default_field,
                    name=default_field,
                    description=default_field,
                    url=candidate_source,
                    category=default_field,
                    language=default_field,
                    country=default_field,
                    nationality=default_field,
                    analysed=False)

        except Exception as e:
            logger.error(e)
        return source_matching

    @staticmethod
    def get_media_dataset_from_resources(resources_dir: str, filename: str) -> pd.DataFrame:
        return load_resources_from_csv(resources_dir=resources_dir, filename=filename)

