import os
import cohere

# Read API key from environment variable
api_key = os.getenv("COHERE_API_KEY")

if not api_key:
    raise RuntimeError("COHERE_API_KEY environment variable is not set")

# Create Cohere client
co = cohere.ClientV2(api_key=api_key)

# Simple text generation request
response = co.chat(
    model="command-a-03-2025",
    messages=[
#       {"role":"user","content":"Explain what an API is in simple terms?"} 
       {"role":"user","content":"List all years between 2000 and 2026, inclusive"} 
    ],
    max_tokens=600,
)


# learning

#print(type(response))
#print(type(response.generations))
#print(type(response.generations[0]))


# Print the generated text
#out = []
#for block in response.message.content:
#    if hasattr(block,"text") and block.text:
#        out.append(block.text)
#print("".join(out).strip())
#print(len(response.message.content))

#print(response.message.content)

#print("".join(block.text for block in response.message.content if hasattr(block,"text")))
block = response.message.content[0]

print(type(block))
print(block.__class__)
print(block.__class__.__name__)
print(dir(block))
print(block.dict())