import os
import torch

def test_chatbot_response_with_mock_chain(mocker):
    os.environ["OPENAI_API_KEY"] = "fake-key"
    os.environ["PINECONE_API_KEY"] = "fake-key"
    os.environ["SYSTEM_QA_INDEX_NAME"] = "fake-index"
    os.environ["VECTOR_MODEL"] = "fake-model"
    os.environ["SENTENCE_TRANSFORMER_MODEL"] = "fake-model"
    mocker.patch("app.tools.chatbot_nlp.Pinecone", return_value=None)
    mocker.patch("app.tools.chatbot_nlp.SentenceTransformer", return_value=mocker.Mock(
        encode=lambda *args, **kwargs: torch.randn(1, 384)
    ))
    mocker.patch("app.tools.chatbot_nlp.HuggingFaceEmbeddings", return_value=mocker.Mock())
    
    mock_vectorstore = mocker.Mock()
    mock_vectorstore.as_retriever.return_value = "mock-retriever"
    mocker.patch("app.tools.chatbot_nlp.LangChainPinecone.from_existing_index", return_value=mock_vectorstore)

    mock_chain = mocker.Mock()
    mock_chain.run.return_value = "Mocked Answer"

    # Patch get_retrieval_chain to return the mocked chain
    mocker.patch("app.tools.chatbot_nlp.RetrievalQA.from_chain_type", return_value=mock_chain)

    from app.tools.chatbot_nlp import chatbot_response
    result = chatbot_response("Tell me about TB")
    assert result == "Mocked Answer"