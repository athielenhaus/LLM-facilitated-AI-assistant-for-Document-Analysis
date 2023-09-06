from acc_checkerUI import get_conversation_chain
from text_prep.text_prep import FileProcessor

def test_get_conversation_chain():
    # WRITE TEST
    # need to create a sample vector store
    fp = FileProcessor('text_prep/test.pdf')
    conversation = get_conversation_chain(fp.text_chunks)
    assert conversation is not None

test_get_conversation_chain()