# Basics

## Vocab
### LLM
Stands for Large Language Model. LLMs simply process text. They do not have memory, autonomy, or the ability to interact with anything. 

### Agent
A person who performs a specific task.

### AI Agent
An LLM that performs a specific task. To do this, LLMs gain memory, autonomy, and the ability to interact with things.

Simple agent pipeline:
1. Prompt the LLM with context which includes available tools and have it decide the next step
2. Have the LLM return a structured output where you can parse the tool usage
3. Call the tool in your actual code with the parameters the LLM provided (if provided) and include the response in the context
4. Repeat from step 1 until the desired task is completed

## LangChain
### `BaseChatModel`
The model to invoke or pass into the `create_agent` method.

#### Methods
##### `invoke(LanguageModelInput)`
Invokes an LLM.

---
### `LanguageModelInput`
```
LanguageModelInput = PromptValue | str | Sequence[MessageLikeRepresentation]
```
```
MessageLikeRepresentation = (
    BaseMessage | list[str] | tuple[str, str] | str | dict[str, Any]
)
```
Takes in a variety of inputs.

Essential in the `invoke` method which takes in a `LanguageModelInput`. 

---
### `BaseMessage`
This is the base abstract message class. It is the input for `ChatPromptTemplates` and the output of invoking a model.

Classes that parent this base include:
1. `SystemMessage`
2. `HumanMessage`
3. `AIMessage`

#### Attributes

##### `content: str | list[str | dict]`
Usually returns a `str` but with multimodal or tool calling models it can sometimes return a `list[dict]`. `list[str]` is not standard.

##### `response_motadata: dict`

Contains all metadata about the response including the token count, model name, etc.