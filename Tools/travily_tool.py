from tavily import TavilyClient 
import os
from dotenv import load_dotenv
load_dotenv()
client=TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")

)
def tavily_search(Query ):
    response=client.search(
        query=Query ,
        max_results=5
    )
    result  