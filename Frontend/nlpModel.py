from sgnlp.models.sentic_gcn import (
    SenticGCNBertConfig,
    SenticGCNBertModel,
    SenticGCNBertEmbeddingConfig,
    SenticGCNBertEmbeddingModel,
    SenticGCNBertTokenizer,
    SenticGCNBertPreprocessor,
    SenticGCNBertPostprocessor
)
import warnings
warnings.filterwarnings("ignore")


tokenizer = SenticGCNBertTokenizer.from_pretrained("bert-base-uncased")

config = SenticGCNBertConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_bert/config.json"
)

model = SenticGCNBertModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_bert/pytorch_model.bin",
    config=config
)

embed_config = SenticGCNBertEmbeddingConfig.from_pretrained(
    "bert-base-uncased")

embed_model = SenticGCNBertEmbeddingModel.from_pretrained("bert-base-uncased",
                                                          config=embed_config
                                                          )

preprocessor = SenticGCNBertPreprocessor(
    tokenizer=tokenizer, embedding_model=embed_model,
    senticnet="https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticnet.pickle",
    device="cpu")

postprocessor = SenticGCNBertPostprocessor()


def classify(text, aspect):

    inputText = text.split(" ")
    aspectExist = False
    for word in inputText:
        if word == aspect:
            aspectExist = True
    if (aspectExist == False):
        inputs = [{
            "aspects": [aspect],
            "sentence": aspect + " " + text,
        }]
    else:
        inputs = [{
            "aspects": [aspect],
            "sentence": text,
        }]

    processed_inputs, processed_indices = preprocessor(inputs)
    raw_outputs = model(processed_indices)
    post_outputs = postprocessor(
        processed_inputs=processed_inputs, model_outputs=raw_outputs)
    print("label predicted:" + str(post_outputs[0]['labels'][0]))
    return post_outputs[0]['labels'][0]

if __name__ == "__main__":
    print(classify("I like the", "food"))