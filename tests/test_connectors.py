import asyncio

import aiohttp
import pytest

from pyrdf2vec.connectors import Connector, SPARQLConnector

URL = "http://pyRDF2Vec"
connector = SPARQLConnector("http://", cache=None)


class TestConnector:
    def test_fetch(self):
        with pytest.raises(NotImplementedError):
            entity = f"{URL}#Bob"
            query = f"SELECT ?p ?o WHERE {{ <{entity}> ?p ?o . }})"
            Connector.fetch(Connector, query)


class TestSPARQLConnector:
    def test_get_query(self):
        entity = f"{URL}#Bob"
        query = connector.get_query(entity)
        assert query == f"SELECT ?p ?o WHERE {{ <{entity}> ?p ?o . }}"

        preds = [f"{URL}#knows", f"{URL}#loves"]
        query = connector.get_query(entity, [preds[0]])
        assert query == (f"SELECT ?o WHERE {{ <{entity}> <{preds[0]}> ?o . }}")

        query = connector.get_query(f"{URL}#Bob", preds)
        assert query == (
            f"SELECT ?o WHERE {{ <{entity}> <{preds[0]}> ?o1 . "
            + f"?o1 <{preds[1]}> ?o . }}"
        )

    def test_close(self):
        connector._asession = aiohttp.ClientSession(raise_for_status=True)
        assert connector._asession.closed is False
        asyncio.run(connector.close())
        assert connector._asession.closed is True
