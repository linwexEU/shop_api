import logging
import sys
from typing import Literal

import aiohttp
import asyncio 
from bs4 import BeautifulSoup

from src.scripts.generator import GenerateExcel
from src.broker.producer import Producer
from src.organizations.schema import SOrganizationsFilters, SOrganizationsModel
from src.utils.dependency import organizations_service, users_service
from src.models.enums import CategoriesEnum, UsersRoleEnum
from src.logger import config_logger 
from src.config import settings
from src.users.schema import SUsersFilters, SUsersModel


logger = logging.getLogger(__name__)

# Configure logger
config_logger() 


class RozetkaParser: 
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-UA,en;q=0.9,ru-UA;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'service-worker-navigation-preload': 'true',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    }

    def __init__(self, url: str, category_type: CategoriesEnum, store: Literal["db", "excel"]) -> None: 
        self.url = url
        self.category_type = category_type
        self.store = store

    async def get_pagination(self) -> int: 
        async with aiohttp.ClientSession() as session: 
            async with session.get(self.url, headers=self.headers) as response: 
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                return int(soup.find_all("a", class_="page text-2xl")[-1].text.strip())

    @staticmethod   
    async def create_test_organization() -> int: 
        organizations_service_db = organizations_service()
        user_services_db = users_service()

        # Create Test User and Test Ogranization if needed 
        has_created = await user_services_db.get_by_filters(SUsersFilters(email="test@dot.com"))

        user_id = None 
        organization_id = None

        if not has_created:
            user_id = await user_services_db.add(
                SUsersModel(username="test_user", email="test@dot.com", hashed_password="bassha256$$$sd", role=UsersRoleEnum.Owner)
            )
            organization_id = await organizations_service_db.add(
                SOrganizationsModel(business_name="TestOrganization", user_id=user_id)
            )
        else: 
            user = await user_services_db.get_by_filters(SUsersFilters(email="test@dot.com"))
            user_id = user.id 

            organization = await organizations_service_db.get_by_filters(SOrganizationsFilters(user_id=user_id))
            organization_id = organization.id

        return organization_id

    async def parse_pages(self) -> None:
        pagination = await self.get_pagination()
        await asyncio.sleep(1)

        # Create Test Ogranization 
        organization_id = await self.create_test_organization()

        if self.store == "excel":
            excel_data = []

        for page in range(1, pagination + 1):
            async with aiohttp.ClientSession() as session: 
                async with session.get(self.url.replace("page=1", f"page={page}"), headers=self.headers) as response: 
                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")

                    products = soup.find_all("div", class_="item")
                    for product in products: 
                        try:
                            title = product.find("a", class_="tile-title black-link text-base").text.strip()

                            price = product.find("div", class_="price").text.replace("\xa0", "").strip(" ₴")
                            if price is None: 
                                price = product.find("div", class_="price color-red").text.replace("\xa0", "").strip(" ₴")
                            price = float(price)

                            image = product.find("img", class_="tile-image").get("src")

                            if self.store == "excel":
                                data = {
                                    "title": title, 
                                    "category": self.category_type.value, 
                                    "price": price, 
                                    "image": image, 
                                    "organization_id": organization_id 
                                }
                                excel_data.append(data)
                            else:
                                # Add product to db
                                async with Producer() as producer: 
                                    await producer.send_message({
                                        "category": self.category_type, 
                                        "title": title, 
                                        "image": image,
                                        "price": price, 
                                        "organization_id": organization_id
                                    })
                            logger.info("Product %s was parsed!" % title)
                        except Exception as ex: 
                            logger.warning("Parser error: %s" % ex) 

            await asyncio.sleep(1)
        
        if self.store == "excel":
            try:
                excel_generator = GenerateExcel()
                excel_generator.generate_file("monitors", ["title", "category", "price", "image", "organization_id"], excel_data)
            except Exception as ex: 
                logger.error("Excel error: %s" % ex)


async def run_script(category, store="db") -> None: 
    url, type = get_url(category)
    rozetka = RozetkaParser(url, type, store)  
    await rozetka.parse_pages() 


def get_url(category: str) -> tuple[str, CategoriesEnum]: 
    match category: 
        case "Computers": return settings.COMPUTERS_URL, CategoriesEnum.Computers # parsed
        case "Phones": return settings.PHONES_URL, CategoriesEnum.Phones # parsed
        case "Monitors": return settings.MONITORS_URL, CategoriesEnum.Monitors # parsed
        case "Lego": return settings.LEGOS_URL, CategoriesEnum.Legos # parsed
        case "Books": return settings.BOOKS_URL, CategoriesEnum.Books # parsed
        case "Keyboards": return settings.KEYBOARDS_URL, CategoriesEnum.Keyboards # parsed
        case "Mouses": return settings.MOUSES_URL, CategoriesEnum.Mouses # parsed
        case "Electronics": return settings.ELECTRONICS_URL, CategoriesEnum.Electronics # parsed


if __name__ == "__main__": 
    category = sys.argv[1:][0]
    store = sys.argv[1:][1] if len(sys.argv[1:]) > 1 else "db"
    asyncio.run(run_script(category, store))
