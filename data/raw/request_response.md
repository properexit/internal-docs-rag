# Request Body[¶](#request-body "Permanent link"){.headerlink preview=""}

When you need to send data from a client (let\'s say, a browser) to your
API, you send it as a **request body**.

A **request** body is data sent by the client to your API. A
**response** body is the data your API sends to the client.

Your API almost always has to send a **response** body. But clients
don\'t necessarily need to send **request bodies** all the time,
sometimes they only request a path, maybe with some query parameters,
but don\'t send a body.

To declare a **request** body, you use
[Pydantic](https://docs.pydantic.dev/){.external-link target="_blank"}
models with all their power and benefits.

::: {.admonition .info}
Info

To send data, you should use one of: `POST` (the more common), `PUT`,
`DELETE` or `PATCH`.

Sending a body with a `GET` request has an undefined behavior in the
specifications, nevertheless, it is supported by FastAPI, only for very
complex/extreme use cases.

As it is discouraged, the interactive docs with Swagger UI won\'t show
the documentation for the body when using `GET`, and proxies in the
middle might not support it.
:::

## Import Pydantic\'s `BaseModel`[¶](#import-pydantics-basemodel "Permanent link"){.headerlink preview=""}

First, you need to import `BaseModel` from `pydantic`:

::::::: {.tabbed-set .tabbed-alternate tabs="1:1"}
::: tabbed-labels
Python 3.10+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        return item
:::
::::
:::::
:::::::

🤓 Other versions and variants

::::::: {.tabbed-set .tabbed-alternate tabs="2:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from typing import Union

    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: Union[str, None] = None
        price: float
        tax: Union[float, None] = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        return item
:::
::::
:::::
:::::::

## Create your data model[¶](#create-your-data-model "Permanent link"){.headerlink preview=""}

Then you declare your data model as a class that inherits from
`BaseModel`.

Use standard Python types for all the attributes:

::::::: {.tabbed-set .tabbed-alternate tabs="3:1"}
::: tabbed-labels
Python 3.10+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        return item
:::
::::
:::::
:::::::

🤓 Other versions and variants

::::::: {.tabbed-set .tabbed-alternate tabs="4:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from typing import Union

    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: Union[str, None] = None
        price: float
        tax: Union[float, None] = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        return item
:::
::::
:::::
:::::::

The same as when declaring query parameters, when a model attribute has
a default value, it is not required. Otherwise, it is required. Use
`None` to make it just optional.

For example, this model above declares a JSON \"`object`\" (or Python
`dict`) like:

::: highlight
    {
        "name": "Foo",
        "description": "An optional description",
        "price": 45.2,
        "tax": 3.5
    }
:::

\...as `description` and `tax` are optional (with a default value of
`None`), this JSON \"`object`\" would also be valid:

::: highlight
    {
        "name": "Foo",
        "price": 45.2
    }
:::

## Declare it as a parameter[¶](#declare-it-as-a-parameter "Permanent link"){.headerlink preview=""}

To add it to your *path operation*, declare it the same way you declared
path and query parameters:

::::::: {.tabbed-set .tabbed-alternate tabs="5:1"}
::: tabbed-labels
Python 3.10+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        return item
:::
::::
:::::
:::::::

🤓 Other versions and variants

::::::: {.tabbed-set .tabbed-alternate tabs="6:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from typing import Union

    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: Union[str, None] = None
        price: float
        tax: Union[float, None] = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        return item
:::
::::
:::::
:::::::

\...and declare its type as the model you created, `Item`.

## Results[¶](#results "Permanent link"){.headerlink preview=""}

With just that Python type declaration, **FastAPI** will:

- Read the body of the request as JSON.
- Convert the corresponding types (if needed).
- Validate the data.
  - If the data is invalid, it will return a nice and clear error,
    indicating exactly where and what was the incorrect data.
- Give you the received data in the parameter `item`.
  - As you declared it in the function to be of type `Item`, you will
    also have all the editor support (completion, etc) for all of the
    attributes and their types.
- Generate [JSON Schema](https://json-schema.org){.external-link
  target="_blank"} definitions for your model, you can also use them
  anywhere else you like if it makes sense for your project.
- Those schemas will be part of the generated OpenAPI schema, and used
  by the automatic documentation [UIs]{.abbr title="User Interfaces"}.

## Automatic docs[¶](#automatic-docs "Permanent link"){.headerlink preview=""}

The JSON Schemas of your models will be part of your OpenAPI generated
schema, and will be shown in the interactive API docs:

![](/img/tutorial/body/image01.png)

And will also be used in the API docs inside each *path operation* that
needs them:

![](/img/tutorial/body/image02.png)

## Editor support[¶](#editor-support "Permanent link"){.headerlink preview=""}

In your editor, inside your function you will get type hints and
completion everywhere (this wouldn\'t happen if you received a `dict`
instead of a Pydantic model):

![](/img/tutorial/body/image03.png)

You also get error checks for incorrect type operations:

![](/img/tutorial/body/image04.png)

This is not by chance, the whole framework was built around that design.

And it was thoroughly tested at the design phase, before any
implementation, to ensure it would work with all the editors.

There were even some changes to Pydantic itself to support this.

The previous screenshots were taken with [Visual Studio
Code](https://code.visualstudio.com){.external-link target="_blank"}.

But you would get the same editor support with
[PyCharm](https://www.jetbrains.com/pycharm/){.external-link
target="_blank"} and most of the other Python editors:

![](/img/tutorial/body/image05.png)

::: {.admonition .tip}
Tip

If you use [PyCharm](https://www.jetbrains.com/pycharm/){.external-link
target="_blank"} as your editor, you can use the [Pydantic PyCharm
Plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin/){.external-link
target="_blank"}.

It improves editor support for Pydantic models, with:

- auto-completion
- type checks
- refactoring
- searching
- inspections
:::

## Use the model[¶](#use-the-model "Permanent link"){.headerlink preview=""}

Inside of the function, you can access all the attributes of the model
object directly:

::::::: {.tabbed-set .tabbed-alternate tabs="7:1"}
::: tabbed-labels
Python 3.10+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        item_dict = item.dict()
        if item.tax is not None:
            price_with_tax = item.price + item.tax
            item_dict.update({"price_with_tax": price_with_tax})
        return item_dict
:::
::::
:::::
:::::::

🤓 Other versions and variants

::::::: {.tabbed-set .tabbed-alternate tabs="8:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from typing import Union

    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: Union[str, None] = None
        price: float
        tax: Union[float, None] = None


    app = FastAPI()


    @app.post("/items/")
    async def create_item(item: Item):
        item_dict = item.dict()
        if item.tax is not None:
            price_with_tax = item.price + item.tax
            item_dict.update({"price_with_tax": price_with_tax})
        return item_dict
:::
::::
:::::
:::::::

::: {.admonition .info}
Info

In Pydantic v1 the method was called `.dict()`, it was deprecated (but
still supported) in Pydantic v2, and renamed to `.model_dump()`.

The examples here use `.dict()` for compatibility with Pydantic v1, but
you should use `.model_dump()` instead if you can use Pydantic v2.
:::

## Request body + path parameters[¶](#request-body-path-parameters "Permanent link"){.headerlink preview=""}

You can declare path parameters and request body at the same time.

**FastAPI** will recognize that the function parameters that match path
parameters should be **taken from the path**, and that function
parameters that are declared to be Pydantic models should be **taken
from the request body**.

::::::: {.tabbed-set .tabbed-alternate tabs="9:1"}
::: tabbed-labels
Python 3.10+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None


    app = FastAPI()


    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: Item):
        return {"item_id": item_id, **item.dict()}
:::
::::
:::::
:::::::

🤓 Other versions and variants

::::::: {.tabbed-set .tabbed-alternate tabs="10:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from typing import Union

    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: Union[str, None] = None
        price: float
        tax: Union[float, None] = None


    app = FastAPI()


    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: Item):
        return {"item_id": item_id, **item.dict()}
:::
::::
:::::
:::::::

## Request body + path + query parameters[¶](#request-body-path-query-parameters "Permanent link"){.headerlink preview=""}

You can also declare **body**, **path** and **query** parameters, all at
the same time.

**FastAPI** will recognize each of them and take the data from the
correct place.

::::::: {.tabbed-set .tabbed-alternate tabs="11:1"}
::: tabbed-labels
Python 3.10+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None


    app = FastAPI()


    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: Item, q: str | None = None):
        result = {"item_id": item_id, **item.dict()}
        if q:
            result.update({"q": q})
        return result
:::
::::
:::::
:::::::

🤓 Other versions and variants

::::::: {.tabbed-set .tabbed-alternate tabs="12:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from typing import Union

    from fastapi import FastAPI
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        description: Union[str, None] = None
        price: float
        tax: Union[float, None] = None


    app = FastAPI()


    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
        result = {"item_id": item_id, **item.dict()}
        if q:
            result.update({"q": q})
        return result
:::
::::
:::::
:::::::

The function parameters will be recognized as follows:

- If the parameter is also declared in the **path**, it will be used as
  a path parameter.
- If the parameter is of a **singular type** (like `int`, `float`,
  `str`, `bool`, etc) it will be interpreted as a **query** parameter.
- If the parameter is declared to be of the type of a **Pydantic
  model**, it will be interpreted as a request **body**.

::: {.admonition .note}
Note

FastAPI will know that the value of `q` is not required because of the
default value `= None`.

The `str | None` (Python 3.10+) or `Union` in `Union[str, None]` (Python
3.8+) is not used by FastAPI to determine that the value is not
required, it will know it\'s not required because it has a default value
of `= None`.

But adding the type annotations will allow your editor to give you
better support and detect errors.
:::

## Without Pydantic[¶](#without-pydantic "Permanent link"){.headerlink preview=""}

If you don\'t want to use Pydantic models, you can also use **Body**
parameters. See the docs for [Body - Multiple Parameters: Singular
values in
body](../body-multiple-params/#singular-values-in-body){.internal-link
preview="" target="_blank"}.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEzIDIwaC0yVjhsLTUuNSA1LjUtMS40Mi0xLjQyTDEyIDQuMTZsNy45MiA3LjkyLTEuNDIgMS40MkwxMyA4eiIgLz48L3N2Zz4=)
Back to top
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
