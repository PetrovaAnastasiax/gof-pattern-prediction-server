from fastapi import FastAPI

from code2vec.config import Config
from code2vec.embeding_extractor import EmbeddingExtractor
from code2vec.tensorflow_model import Code2VecModel
from models import JavaFile

app = FastAPI()

config = Config(set_defaults=True, verify=True)
model = Code2VecModel(config)
extractor = None

# Define startup event handler
@app.on_event("startup")
async def startup_event():
    global extractor
    extractor = EmbeddingExtractor(config, model)

# Define shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    model.close_session()


@app.post("/predict")
async def predict(request: JavaFile):
    prediction = extractor.extract_embeddings_from_request(request)
    return prediction





















# form/data
# file: binary
# path: org/example/inner
# className: User.java
# request
# Content-Type: application/json
# {
#     "packagePath": "org.example",
#     "className": "Main.java",
#     "classText": "import java.util.ArrayList;\npublic class Main {\n   public static void main(String[] args) { System.out.println(args[0]); }}"
# }

# resposne
# {
#     "packagePath": "org.example",
#     "className": "Main.java",
#     "predictedPattern": "ADAPTER"
# }
# predictedPatter: enum ADAPTER, BUILDER, PROTOTYPE, SINGLETON, NONE