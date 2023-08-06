import json

API_SEARCH="search"

class SearchResult():

    def __init__(self,
            client,
            docset_name: str,
            query_string: str, 
            max_results: int=None,
            fuzzy: bool=None,
            filters: dict=None,
            sorts: dict=None,
            page_size: int=None,
        ):
        """
        """
        api_data = {
            "q": query_string
        }
        if filters is not None:
            api_data["filters"] = filters
        if max_results is not None:
            api_data["max_res"] = max_results
        if fuzzy is not None:
            api_data["fuzzy"] = fuzzy
        #if sorts is not None:
        #    api_data["sorts"] = sorts
        if page_size is not None:
            api_data["page_size"] = page_size
        self._client=client
        self._api_data = api_data
        self._docset_name=docset_name
        self._base_url = f"{API_SEARCH}/{docset_name}"
        self._pages = dict()
        resp =  client._call_api_function(self._base_url, api_data)
        self._set_result(json.loads(resp.content))

    @property
    def terms(self):
        return self._terms

    def _go_to_page(self,
            page: int=None
            ):
        if not page:
            page = self._cur_page + 1
        self._cur_page = page
        if self._cur_page in self._pages:
            self._res_idx=0
            return
        api_data = {
            "search_key": self._key,
            "page": page
        }
        resp =  self._client._call_api_function(self._base_url, api_data)
        self._set_result(json.loads(resp.content))


            

    def _set_result(self,
            result: dict
            ):
        self._key = result['key']
        self._cur_page = int(result['page'])
        self._count = int(result['count'])
        self._num_pages = int(result['pages'])
        self._terms = result['terms']
        self._pages[self._cur_page] = result['results']
        # index of the result in the page
        self._res_idx = 0


    def __len__(self):
        return self._count

    def __iter__(self):
        self._cur_page = 0
        return self

    def __next__(self):
        page_data = self._pages[self._cur_page]
        if self._res_idx >= len(page_data):
            # laod next page
            self._go_to_page()
            page_data = self._pages[self._cur_page]
        if len(page_data) == 0:
            raise StopIteration
        res = page_data[self._res_idx]
        self._res_idx += 1
        return res

