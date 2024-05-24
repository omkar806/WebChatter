### WebChatter

- **Description**: An intelligent web interaction tool that harnesses the power of RAG (Retriever, Aggregator, Generator) flow to facilitate seamless communication with websites.

- **Functionality**:
  - Upon receiving a webpage link, WebChatter swiftly scrapes the webpage, extracts its textual content, and divides it into manageable chunks.
  - These chunks are then embedded with metadata and stored in a Pinecone vector database.

- **User Interaction**:
  - Once the index is established, users can engage in conversational queries.
  - By inputting a query, WebChatter generates embeddings for the query and calculates cosine similarity scores between these embeddings and the embeddings of the webpage chunks.
  - The chunks exhibiting the highest similarity scores are selected and passed to the Language Model (LLM) along with the query, facilitating accurate and targeted responses.

- **UI Demo
- <img width="1209" alt="image" src="https://github.com/omkar806/WebChatter/assets/77787482/2b57a358-f9cf-4700-ad2e-5b338cb97112">  
  - Above is the image where User have to input the Webpage link.
- <img width="1217" alt="image" src="https://github.com/omkar806/WebChatter/assets/77787482/ff8b6a50-42f5-4d87-baeb-8d17536e0e99">
  - Above is the image where User will input his query and chat with the Webpage
- <img width="1204" alt="image" src="https://github.com/omkar806/WebChatter/assets/77787482/d6d59836-a847-4723-bf7b-e27f11aae7dd">
  - Above is the image where User receives his response from the bot.


