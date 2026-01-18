import os
import cohere

co = cohere.ClientV2(os.environ["COHERE_API_KEY"])
if "COHERE_API_KEY" not in os.environ:
    raise RuntimeError("COHERE_API_KEY not set")


# List models available to your API key
resp = co.models.list()
for m in resp.models:
    print(m.name)
