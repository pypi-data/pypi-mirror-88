# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from abc import ABC, abstractmethod
from typing import Optional, List, Union, Dict
from requests import Response

# Local
from .request import Request

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------------- class: Api -------------------------------------------------------------- #

class Api:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        keep_cookies: bool = False,
        cookies_file_path: Optional[str] = None,
        store_pickled_cookies: bool = False,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        default_headers: Optional[Dict[str, any]] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: bool = False
    ):
        """init function

        Args:
            user_agent (Optional[Union[str, List[str]]], optional): User agent(s) to use for requests. If list is provided, one will be chosen randomly. Defaults to None.
            proxy (Optional[Union[str, List[str]]], optional): Proxy/Proxies to use for requests. If list is provided, one will be chosen randomly. Defaults to None.
            keep_cookies (bool, optional): Keep cookies for requests and reuse them at next one. Defaults to True.
            cookies_file_path (str, optional): If provided, cookies will be saved to/loaded from it. Defaults to None.
            max_request_try_count (int, optional): How many times does a request can be tried (if fails). Defaults to 1.
            sleep_s_between_failed_requests (Optional[float], optional): How much to wait between requests when retrying. Defaults to 0.5.
            debug (bool, optional): Show debug logs. Defaults to False.
        """
        self._request = Request(
            user_agent=user_agent,
            proxy=proxy,
            keep_cookies=keep_cookies,
            cookies_file_path=cookies_file_path,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            default_headers=default_headers or self.default_headers(),
            extra_headers=extra_headers or self.extra_headers(),
            debug=debug
        )


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @classmethod
    def default_headers(cls) -> Optional[Dict[str, any]]:
        """ Default headers to use for every request.
            Overwrite this value as needed.
        """

        return {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
        }

    @classmethod
    def extra_headers(cls) -> Optional[Dict[str, any]]:
        """ Every entry from this adds/overwrites an entry from 'default_headers'
            Overwrite this value as needed.
        """

        return None


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def _get(
        self,
        url: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return self._request.get(
            url,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )

    @classmethod
    def _get_cls(
        cls,
        url: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return Api(default_headers=cls.default_headers(), extra_headers=cls.extra_headers())._get(
            url,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=False,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )

    def _post(
        self,
        url: str,
        body: dict,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return self._request.post(
            url,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            body=body,
            debug=debug
        )

    @classmethod
    def _post_cls(
        cls,
        url: str,
        body: dict,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return Api(default_headers=cls.default_headers(), extra_headers=cls.extra_headers())._post(
            url,
            body,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=False,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )
    
    def _put(
        self,
        url: str,
        body: dict,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return self._request.put(
            url,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            body=body,
            debug=debug
        )

    @classmethod
    def _put_cls(
        cls,
        url: str,
        body: dict,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return Api(default_headers=cls.default_headers(), extra_headers=cls.extra_headers())._put(
            url,
            body,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=False,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )
    
    def download(
        self,
        url: str,
        path: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> List[bool]:
        return self._request.download(
            url,
            path,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )

    @classmethod
    def download_cls(
        cls,
        url: str,
        path: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> List[bool]:
        return Api(default_headers=cls.default_headers(), extra_headers=cls.extra_headers()).download(
            url,
            path,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=False,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )

    def download_async(
        self,
        urls_paths: Optional[Dict[str, str]] = None,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> List[bool]:
        return self._request.download_async(
            urls_paths,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )

    @classmethod
    def download_async_cls(
        cls,
        urls_paths: Optional[Dict[str, str]] = None,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> List[bool]:
        return Api(default_headers=cls.default_headers(), extra_headers=cls.extra_headers()).download_async(
            urls_paths,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=False,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #