from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

load_dotenv()


llm = OpenAI()
# chat_model = ChatOpenAI()
# memory = ConversationBufferWindowMemory( k=1)


conversation_with_summary = ConversationChain(
    llm=llm,
    # We set a low k=2, to only keep the last 2 interactions in memory
    memory=ConversationBufferWindowMemory(k=2),
    verbose=True
)

while True:
    user_input = input(">>> ")
    if user_input == "exit":
        break
    else:
        response = conversation_with_summary.predict(input=user_input)
        print(response)