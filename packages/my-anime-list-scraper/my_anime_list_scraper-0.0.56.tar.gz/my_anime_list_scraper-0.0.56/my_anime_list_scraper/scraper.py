import time
import requests
from bs4 import BeautifulSoup
from my_anime_list_scraper import cleaner
from my_anime_list_scraper import extractor
from my_anime_list_scraper import saver
from my_anime_list_scraper import sql_queries
from my_anime_list_scraper.scraper_types import PageTypes


class MalScraper:
    """
    Scraper for www.myanimelist.com
    """

    def __init__(self, output_type="tsv", output_location=None, db_host=None,
                 db_user=None, db_password=None, db_database=None, request_period=10):
        """
        Parameters
        ----------
        output_type: str
            The format to save the data. Either "tsv" or "mysql".
        output_location: str
            The location to save the data if output_type="tsv".
        db_host: str
            The database host. Required if output_type="mysql".
        db_user: str
            The database user. Required if output_type="mysql".
        db_password: str
            The database password. Required if output_type="mysql".
        db_database: str
            The database name. Required if output_type="mysql".
        request_period: int
            Time (secs) to wait in between requests to avoid being blocked.
        """

        if output_location != None and (output_location[-1] != '/' and output_location[-1] != '\\'):
            raise Exception("The output location must be folder. This means the output location must end with a slash (either forward or backwards).")

        self.output_type = output_type
        self.output_location = output_location
        self.base_url = "https://myanimelist.net/"
        self.request_period = request_period
        self.sql_manager = None

        if (output_type == "mysql") and (db_host is not None) and (db_user is not None) and (db_password is not None) and (db_database is not None):
            from my_anime_list_scraper.mysql_manager import DatabaseManager

            self.sql_manager = DatabaseManager(db_host, db_user, db_password, db_database)


    def scrape_details(self, content_type="anime", start_page=0, failure_threshold=100, print_intermediate=False, num_retries=5):
        """
        Scrapes MyAnimeList detail pages.

        Parameters
        ----------
        content_type: str
            The type of page being scraped. Either "anime" or "manga".
        start_page: int
            The location to start at (e.g. type="anime" and start_page=5 => https://myanimelist.net/anime/5 )
        failure_threshold: int
            The number of consecutive fails allowed before stopping the scraper. A fail is when a 404 page is returned,
            signifying no content is at that page.
        print_intermediate: bool
            Determines if intermediate output would be appreciated by the user (current page being scraped, number of 
            consectuve fails, etc.).
        num_retries: int
            Number of retries the scraper will attempt for an individual page. This is used as a backup for IP blocking scenarios.
            The time between retries are always (5 minutes * retry attempt #).
        """

        continue_scraping = True
        mal_id = start_page
        failure_count = 0
        retry_count = 0
        sql_details_table = self.sql_manager.check_table_exists("MAL_Anime_Details") if self.sql_manager != None else None

        if sql_details_table == False:
            self.sql_manager.execute(sql_queries.create_mal_anime_details_table(), None)
            self.sql_manager.execute(sql_queries.create_mal_anime_detail_stats_table(), None)

        if print_intermediate:
            print("\n\n======================= STARTING MYANIMELIST SCRAPER =======================\n")
            print(str(self.request_period) + " seconds between page requests\n\n")

        try: 
            while continue_scraping:
                url = self.base_url + content_type + "/" + str(mal_id)

                if print_intermediate:
                    print("Scraping: " + url)

                page = None

                # Attempt page request, if the IP address is blocked, keep retrying with increasing time in between requests until
                # num_retries is hit.
                try:
                    # Request page
                    page = requests.get(url)
                    retry_count = 0
                except requests.exceptions.ConnectionError as e:
                    retry_count = retry_count + 1

                    if retry_count <= num_retries:
                        if print_intermediate:
                            print("\nIP has been blocked. Retrying in " + str(retry_count * 5)  + " minutes...")
                            print("Currently at " + str(retry_count) + "/" + str(num_retries) + " possible attempts for " + url + "\n")

                        time.sleep((retry_count * 5) * 60)
                        continue
                    else:
                        raise(e)

                # This should never occur.
                if page == None:
                    raise(url + " cannot be requested.")

                # Parse content
                soup = BeautifulSoup(page.content, "html.parser")

                # Check if content_type with this id was found
                page_not_found = soup.find("div", class_="error404") is not None

                # If we get the 404 page, increase the failure_count
                if page_not_found:
                    failure_count = failure_count + 1

                    if print_intermediate:
                        print("Page not found in " + str(failure_count) + " continuous attempts.")

                    # If we have reached our limit off continuous 404 pages, stop scraping
                    # (this assumes there's nothing left to scrape)
                    if failure_count == failure_threshold:
                        continue_scraping = False
                else:
                    # Set failure count to 0 because we succeeded
                    failure_count = 0
                    data = self.__extract(soup, mal_id, PageTypes.anime_details) if content_type == "anime" else None

                    if self.output_type == "tsv":
                        saver.save_as_tsv(self.output_location, "mal_" + content_type + "_details", data)
                    elif self.output_type == "mysql":
                        if content_type == "anime":
                            q1, v1 = sql_queries.insert_mal_anime_detail(data)
                            self.sql_manager.execute(q1, v1)

                            q2, v2 = sql_queries.insert_mal_anime_detail_stats(data)
                            self.sql_manager.execute(q2, v2)

                mal_id = mal_id + 1
                time.sleep(self.request_period)

            if print_intermediate:
                print("\n\n======================= FINISHED SCRAPING MYANIMELIST =======================\n")
        except Exception as e:
            print("\n\nError occured while scraping "  + self.base_url + content_type + "/" + str(mal_id) + "\n\n")
            raise(e)

    def __extract(self, soup, mal_id, page_type):
        """
        Extracts an anime page's details and statistics.

        Parameters
        ----------
        soup: BeautifulSoup object
            The BeautifulSoup object containing the page's content
        mal_id: int
            Id of the anime being scraped
        page_type: PageType
            Type of page to scrape
        """

        if page_type == PageTypes.anime_details:
            details_dict = extractor.extract_anime_details(soup, mal_id)
            cleaned_dict = self.__clean(details_dict, page_type)
            return cleaned_dict

        return {}

    def __clean(self, information_dict, page_type):
        """
        Cleans raw extracted data

        Parameters
        ----------
        information_dict : dict
            The dictionary holding extracted data
        page_type: PageType
            Type of page to scrape
        """

        if page_type == PageTypes.anime_details:
            return cleaner.clean_anime_details(information_dict)
        
        return {}