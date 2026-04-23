from config import *
from vector_store import *
from ai_chat  import *
from qdrant_client import AsyncQdrantClient, models
import os 
import asyncio
async def check_points(client: AsyncQdrantClient , collection_name: str , file_path: str = "expected_points.txt"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found ")
    with open(file_path , "r") as f :
        expected_points = int(f.read().strip())
    count_result = await client.count(collection_name=collection_name , exact=True)
    actual_points = count_result.count
    # print(f"expected : {expected_points} , Actual {actual_points}")
    if actual_points == expected_points : 
        return True 
    else : 
        with open(file_path , "w") as f : 
            f.write(str(actual_points))
        print("the value of expected points has beed updated ")
        return False 



async def main():
# we need to check if the database exists 
    if not(check_database()):
        create_qdrant_collection()
    client = AsyncQdrantClient(host="localhost" , port=6333)
    check = await check_points(client , COLLECTION_NAME)
    if not(check) : 
        embed_database()
    start_chat_bot()  




asyncio.run(main())
