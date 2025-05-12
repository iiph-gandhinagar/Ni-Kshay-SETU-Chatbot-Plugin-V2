from unittest.mock import patch, Mock
import torch

def test_vectors_search_returns_node_ids():
    fake_node_id_1 = "node_123"
    fake_node_id_2 = "node_456"

    # Step 1: Patch environment variables
    with patch("app.tasks.vector_search.os.getenv") as mock_getenv:
        mock_getenv.side_effect = lambda key: {
            "APP_ENV": "test",
            "PINECONE_API_KEY": "fake-key",
            "PINECONE_ENV": "fake-env",
            "CHATBOT_INDEX_NAME": "fake-index",
            "VECTOR_MODEL": "fake-model",
            
        }.get(key)

        # Step 2: Mock Pinecone Index
        mock_index = Mock()
        mock_index.query.return_value = {
            "matches": [
                {"metadata": {"node_id": fake_node_id_1}, "score": 0.91},
                {"metadata": {"node_id": fake_node_id_2}, "score": 0.89}
            ]
        }

        # Step 3: Patch Pinecone() and .Index()
        mock_pinecone = Mock()
        mock_pinecone.Index.return_value = mock_index
        with patch("app.tasks.vector_search.Pinecone", return_value=mock_pinecone):

            # Step 4: Patch tokenizer
            mock_tokenizer = Mock()
            mock_tokenizer.return_value = {"input_ids": torch.tensor([[1, 2, 3]]), "attention_mask": torch.tensor([[1, 1, 1]])}
            with patch("app.tasks.vector_search.AutoTokenizer.from_pretrained", return_value=mock_tokenizer):

                # Step 5: Patch model
                mock_model = Mock()
                mock_model.return_value = Mock(last_hidden_state=torch.randn(1, 3, 384))  # random tensor
                mock_model.__call__ = lambda self, **kwargs: mock_model.return_value  # torch model call
                mock_model.__call__.return_value = mock_model.return_value

                with patch("app.tasks.vector_search.AutoModel.from_pretrained", return_value=mock_model):
                    from app.tasks.vector_search import vectors_search

                    # ✅ Call the actual function
                    result = vectors_search("tb prevention")

                    # ✅ Assert expected result
                    assert result == [fake_node_id_1, fake_node_id_2]
