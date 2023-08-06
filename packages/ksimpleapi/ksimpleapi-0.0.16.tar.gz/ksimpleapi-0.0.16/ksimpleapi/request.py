# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union, Dict
from requests import Response
import random, copy, os, pickle

# Pip
from kcu.request import request, req_download, req_multi_download, RequestMethod
import tldextract

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Request ------------------------------------------------------------ #

class Request:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        default_headers: Optional[Dict[str, any]] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        keep_cookies: bool = True,
        cookies_file_path: Optional[str] = None,
        debug: bool = False
    ):
        self._cookies_path = cookies_file_path
        self.cookies = self._load_cookies()

        self.max_request_try_count = max_request_try_count
        self.sleep_s_between_failed_requests = sleep_s_between_failed_requests

        self.keep_cookies = keep_cookies
        self.debug = debug

        if type(user_agent) == list:
            user_agent = random.choice(user_agent) if len(user_agent) > 0 else None

        self.user_agent = user_agent
        self.last_used_user_agent = None

        if type(proxy) == list:
            proxy = random.choice(proxy) if len(proxy) > 0 else None

        self.proxy = proxy
        self.last_used_proxy = None

        self.default_headers = {}

        self.default_headers = self.__generate_headers(
            url=None,
            default_headers=default_headers,
            extra_headers=extra_headers
        )

    def get(
        self,
        url: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        extra_headers: Optional[Dict[str, any]] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        return self.__request(
            url,
            RequestMethod.GET,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            debug=debug
        )

    def put(
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
        return self.__request(
            url,
            RequestMethod.PUT,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            body=body,
            debug=debug
        )
    
    def post(
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
        return self.__request(
            url,
            RequestMethod.POST,
            user_agent=user_agent,
            proxy=proxy,
            use_cookies=use_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers=extra_headers,
            body=body,
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
        headers = self.__generate_headers(
            default_headers=self.default_headers,
            extra_headers=extra_headers,
            all_cookies=self.cookies,
            use_cookies=use_cookies
        )

        return req_multi_download(
            urls_paths,
            headers=headers,
            user_agent=self.__get_user_agent(user_agent, use_cookies),
            debug=debug if debug is not None else self.debug,
            max_request_try_count=max_request_try_count if max_request_try_count is not None else self.max_request_try_count,
            sleep_time=sleep_s_between_failed_requests if sleep_s_between_failed_requests is not None else self.sleep_s_between_failed_requests,
            proxy=self.__get_proxy(proxy, use_cookies)
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
    ) -> bool:
        headers = self.__generate_headers(
            url=url,
            default_headers=self.default_headers,
            extra_headers=extra_headers,
            all_cookies=self.cookies,
            use_cookies=use_cookies
        )

        return req_download(
            url,
            path,
            headers=headers,
            user_agent=self.__get_user_agent(user_agent, use_cookies),
            debug=debug if debug is not None else self.debug,
            max_request_try_count=max_request_try_count or self.max_request_try_count,
            sleep_time=sleep_s_between_failed_requests or self.sleep_s_between_failed_requests,
            proxy=self.__get_proxy(proxy, use_cookies)
        )


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def _clean_url(self, url: str) -> str:
        url_comps = tldextract.extract(self.driver.current_url)

        return url_comps.domain + '.' + url_comps.suffix

    def _get_cookies_for_url(self, url: str) -> Optional[Dict[str, str]]:
        url = self._clean_url(url)

        return self.cookies[url] if url in self.cookies else None

    def _save_cookies_for_url(self, url: str, cookies: Dict[str, str]):
        self._set_cookies_for_url(url, cookies=cookies, save=True)

    def _set_cookies_for_url(self, url: str, cookies: Dict[str, str], save: bool = False):
        self.cookies = self.cookies or {}
        self.cookies.update({self._clean_url(url):cookies})

        if save:
            self.__save_cookies()

    def __save_cookies(self):
        cookies_path = self.__cookies_path()

        try:
            os.remove(cookies_path)
        except:
            pass

        if not self.cookies:
            return

        pickle.dump(
            self.cookies,
            open(self.__cookies_path(), 'wb')
        )

    def _load_cookies(self) -> Optional[Dict[str, Dict[str, str]]]:
        if not self._cookies_path or not os.path.exists(self._cookies_path):
            return None

        return pickle.load(open(self._cookies_path, 'rb'))


    def __request(
        self,
        url: str,
        method: RequestMethod,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = True,
        max_request_try_count: Optional[int] = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        body: Optional[dict] = None,
        debug: Optional[bool] = None
    ) -> Optional[Response]:
        headers = self.__generate_headers(
            url=url,
            default_headers=self.default_headers,
            extra_headers=extra_headers,
            all_cookies=self.cookies,
            use_cookies=use_cookies
        )

        res = request(
            url,
            method,
            headers=headers,
            user_agent=self.__get_user_agent(user_agent, use_cookies),
            data=body,
            debug=debug if debug is not None else self.debug,
            max_request_try_count=max_request_try_count if max_request_try_count is not None else self.max_request_try_count,
            sleep_time=sleep_s_between_failed_requests if sleep_s_between_failed_requests is not None else self.sleep_s_between_failed_requests,
            proxy=self.__get_proxy(proxy, use_cookies)
        )

        if use_cookies and self.keep_cookies and res and res.cookies:
            self._set_cookies_for_url(url, res.cookies.get_dict(), save=self._cookies_path != None)

        return res

    def __get_proxy(
        self,
        proxy: Optional[Union[str, List[str]]],
        use_cookies: bool
    ) -> Optional[str]:
        proxy = proxy or self.proxy

        if type(proxy) == list:
            proxy = random.choice(proxy) if len(proxy) > 0 else None

        if use_cookies and self.last_used_proxy:
            proxy = self.last_used_proxy
        elif not self.last_used_proxy:
            self.last_used_proxy = proxy
        
        return proxy
    
    def __get_user_agent(
        self,
        user_agent: Optional[Union[str, List[str]]],
        use_cookies: bool
    ) -> Optional[str]:
        user_agent = user_agent or self.user_agent

        if type(user_agent) == list:
            user_agent = random.choice(user_agent) if len(user_agent) > 0 else None

        if use_cookies and self.last_used_user_agent:
            user_agent = self.last_used_user_agent
        elif not self.last_used_user_agent:
            self.last_used_user_agent = user_agent

        return user_agent

    def __generate_headers(
        self,
        url: Optional[str] = None,
        default_headers: Optional[Dict[str, any]] = None,
        extra_headers: Optional[Dict[str, any]] = None,
        all_cookies: Optional[Union[str, List[str]]] = None,
        use_cookies: bool = False
    ) -> Dict[str, str]:
        headers = {}

        if default_headers:
            for k, v in default_headers.items():
                if not v:
                    continue

                if type(v) != str:
                    v = str(v)

                headers[k] = v

        if extra_headers:
            for k, v in extra_headers.items():
                if not v:
                    continue

                if type(v) != str:
                    v = str(v)

                headers[k] = v

        if url and ('Host' not in headers or not headers['Host']):
            host = self.__get_host(url)

            if host:
                headers['Host'] = host

        if use_cookies and all_cookies:
            cookies_url = self.__clean_url(url)

            if cookies_url in all_cookies:
                cookie_strs = ['{}={}'.format(k, v) for k, v in all_cookies[cookies_url].items()]

                if len(cookie_strs) > 0:
                    headers['Cookie'] = '; '.join(cookie_strs)

        return headers

    def __get_host(self, url: str) -> Optional[str]:
        try:
            return url.split('://')[1].split('/')[0]
        except:
            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #