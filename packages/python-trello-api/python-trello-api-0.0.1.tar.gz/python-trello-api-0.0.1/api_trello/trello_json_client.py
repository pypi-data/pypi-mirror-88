import asyncio
from typing import List
from aiohttp import ClientSession, ClientResponse

from datetime import datetime
from loguru import logger as log
import re

class TrelloJson:
    def __init__(self, api_key: str = None, token: str = None, board_id: str = None):
        assert re.match(r'^[0-9a-fA-F]{32}$', api_key)
        assert re.match(r'^[0-9a-fA-F]{64}$', token)
        assert re.match(r'^[0-9a-fA-F]+$', board_id)
        self.api_key = api_key
        self.token = token
        self.board_id = board_id
        self.loop = asyncio.get_event_loop()
        self.base_json_params = {
            "key": self.api_key,
            "token": self.token,
        }

        # self.todo_list = self.board.get_list(Const_Trello_Lists.TODO)

        # self.MEMBER_SHRAINER = Member(client, "5d6eb04694e700834171741e")

    # # TODO: get_card_in_list
    # async def get_card(self, card_id, card_list_id):
    #     card_list = await self.loop.run_in_executor(None, self.board.get_list, card_list_id)
    #     json_obj = await self.loop.run_in_executor(None, self.client.fetch_json,
    #                                                '/boards/' + self.board_id + '/cards/' + str(card_id))
    #     return await self.loop.run_in_executor(None, Card.from_json, card_list, json_obj)

    async def get_webhooks(self) -> list:  #-> List[TrelloWebHook]:
        """
        Get Webhooks for Token
        """
        url = f"https://trello.com/1/tokens/{self.token}/webhooks"
        json = self.base_json_params.copy()
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.get(url, json=json)
            return await response.json()
        # return [TrelloWebHook.parse_obj(wh) for wh in response]

    async def del_webhook(self, wh_id: str) -> dict:  # wh: TrelloWebHook
        """
        :param wh_id: ID of the webhook to retrieve. Pattern: ^[0-9a-fA-F]{32}$
        """
        assert re.match(r'^[0-9a-fA-F]+$', wh_id)

        url = f"https://trello.com/1/tokens/{self.token}/webhooks/{wh_id}"
        json = self.base_json_params.copy()
        # return await self.delete(url=url, json=json)
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.delete(url, json=json)
            if response.content_type == "text/plain":
                return {"status": response.status, "message": await response.text(), "error": "ERROR"}
            return await response.json()

    async def set_webhook(self, callback_url: str, description: str = "", id_model: str = None) -> dict:
        """
        :param callback_url: A valid URL that is reachable with a HEAD and POST request.
        :param description: A string with a length from 0 to 16384.
        :param id_model: ID of the model to be monitored. Pattern: ^[0-9a-fA-F]{32}$
        """
        if not id_model:
            id_model = self.board_id
        assert re.match(r'^[0-9a-fA-F]+$', id_model)
        url = f"https://trello.com/1/tokens/{self.token}/webhooks"
        json = {
            **self.base_json_params.copy(),
            "description": description,
            "callbackURL": callback_url,
            "idModel": id_model
        }
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.post(url, json=json)
            if response.content_type == "text/plain":
                return {"status": response.status, "message": await response.text(), "error": "ERROR"}
            return await response.json()



    async def recreate_webhook(self, callback_url: str) -> dict:
        log.debug(f"Trello: Setting webhook {callback_url} ...")
        wh_list = await self.get_webhooks()
        # wh_list = await response.json()
        for wh in wh_list:
            # if "mpk" in wh.callBackURL:
            #     continue
            await self.del_webhook(wh["id"])
        return await self.set_webhook(callback_url)




    async def create_card(self, id_list, name: str = "", desc: str = "", due: str = None, pos = "top", **kwargs) -> dict:  # -> TrelloCard:
        """
        :param id_list: The ID of the list the card should be created in. Pattern: ^[0-9a-fA-F]{32}$
        :param name: The name for the card
        :param desc: The description for the card
        :param due: A due date for the card. Format: date
        :param pos: The position of the new card. top, bottom, or a positive float
        :param kwargs:
        """
        # assert re.match(r'^[0-9a-fA-F]+$', id_list)
        assert pos in ["top", "bottom"] or type(pos) == float
        if not due:
            due = str(datetime.today())

        today_str_hr = datetime.now().strftime("%d.%m.%Y %H:%M")
        url = f"https://trello.com/1/cards"
        json = {
            **self.base_json_params.copy(),
            "name": name,
            # "name": f"{user_name} {today_str_hr}",
            "desc": desc,
            "due": due,
            "idList": id_list,  # Const_Trello_Lists.TODO,
            "pos": pos,
            **kwargs
        }
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.post(url, json=json)
            if response.content_type == "text/plain":
                return {"status": response.status, "message": await response.text(), "error": "ERROR"}
            return await response.json()

    async def get_card(self, card_id: str) -> dict: #-> TrelloCard:
        """
        :param card_id: The ID of the Card. Pattern: ^[0-9a-fA-F]{32}$
        """
        # assert re.match(r'^[0-9a-fA-F]+$', card_id)
        url = f"https://trello.com/1/cards/{card_id}"
        json = {
            **self.base_json_params.copy(),
            "fields": "all",
            "checklists": "all",
            "customFieldItems": True,
        }
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.get(url, json=json)
            if response.content_type == "text/plain":
                return {"status": response.status, "message": await response.text(), "error": "ERROR"}
            return await response.json()
        #return TrelloCard.parse_obj(await self.get(url=url, json=json))

    async def update_card(self, card_id, **kwagrs) -> dict:  # -> TrelloCard:
        """
        :param card_id: The ID of the Card. Pattern: ^[0-9a-fA-F]{32}$
        """
        # assert re.match(r'^[0-9a-fA-F]+$', card_id)
        # , title: str = None, desc: str = None
        url = f"https://trello.com/1/cards/{card_id}"
        json = {
            **self.base_json_params.copy(),
            **kwagrs
        }

        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.put(url, json=json)
            if response.content_type == "text/plain":
                return {"status": response.status, "message": await response.text(), "error": "ERROR"}
            return await response.json()
        #return TrelloCard.parse_obj(await self.put(url=url, json=json))

        # new_title = "🔄 " + str(card_short_id) + " " + title
        # card = await self.get_card(card_id)
        #
        # if card:
        #     await self.loop.run_in_executor(None, card.set_name, new_title)
        #     await self.loop.run_in_executor(None, card.set_description, txt)
        #
        #     if card.labels and len(card.labels) > 0:
        #         for la in card.labels:
        #             await self.loop.run_in_executor(None, card.remove_label, la)
        #     if lab:
        #         await self.loop.run_in_executor(None, card.add_label, lab)
        #
        # return card, lab

    async def get_lists(self, **kwagrs):  #-> List[TrelloList]:
        url = f"https://trello.com/1/boards/{self.board_id}/lists"
        json = {
            **self.base_json_params.copy(),
            **kwagrs
        }
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.get(url, json=json)
            if response.content_type == "text/plain":
                return {"status": response.status, "message": await response.text(), "error": "ERROR"}
            return await response.json()
        # response = await self.get(url=url, json=json)
        # return [TrelloList.parse_obj(lst) for lst in response]

    async def add_member(self, card_id, value) -> dict:
        """
        :param card_id: The ID of the Card. Pattern: ^[0-9a-fA-F]{32}$
        :param value: The ID of the Member to add to the card. Pattern: ^[0-9a-fA-F]{32}$
        :return:
        """
        # assert re.match(r'^[0-9a-fA-F]+$', card_id)
        # assert re.match(r'^[0-9a-fA-F]+$', value)
        #
        url = f"https://trello.com/1/cards/{card_id}/idMembers"
        json = {
            **self.base_json_params.copy(),
            "value": value,
        }
        async with ClientSession(headers={"Accept": "application/json"}) as c:
            response = await c.post(url, json=json)
            if response.content_type == "text/plain":
                return {"status": response.status, "message": await response.text(), "error": "ERROR"}
            return await response.json()
        # return await self.post(url=url, json=json)



    # async def update_card_status(self, obj: Display):
    #     # TODO: лишний запрос в трелло
    #     card = await self.get_card(obj.entities.card.id)
    #
    #     if obj.entities.member_creator.id not in card.id_members:
    #         await self.add_member(card.id, obj.entities.member_creator.id)
    #
    #     if obj.entities.list_after.id == Const_Trello_Lists.DONE:
    #         new_title = "✅" + re.sub("[" + re.escape("🆘✅🔄" + "]"), "", card.name)
    #         await self.update_card(card.id, due_complete=True, title=new_title)
    #
    #     if obj.entities.list_before.id == Const_Trello_Lists.DONE:
    #         new_title = "🔄" + re.sub("[" + re.escape("🆘✅🔄" + "]"), "", card.name)
    #         await self.update_card(card.id, due_complete=False, title=new_title)

