# Path Parameters[¶](#path-parameters "Permanent link"){.headerlink preview=""}

You can declare path \"parameters\" or \"variables\" with the same
syntax used by Python format strings:

::::::: {.tabbed-set .tabbed-alternate tabs="1:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/items/{item_id}")
    async def read_item(item_id):
        return {"item_id": item_id}
:::
::::
:::::
:::::::

The value of the path parameter `item_id` will be passed to your
function as the argument `item_id`.

So, if you run this example and go to
[http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo){.external-link
target="_blank"}, you will see a response of:

::: highlight
    {"item_id":"foo"}
:::

## Path parameters with types[¶](#path-parameters-with-types "Permanent link"){.headerlink preview=""}

You can declare the type of a path parameter in the function, using
standard Python type annotations:

::::::: {.tabbed-set .tabbed-alternate tabs="2:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/items/{item_id}")
    async def read_item(item_id: int):
        return {"item_id": item_id}
:::
::::
:::::
:::::::

In this case, `item_id` is declared to be an `int`.

::: {.admonition .check}
Check

This will give you editor support inside of your function, with error
checks, completion, etc.
:::

## Data [conversion]{.abbr title="also known as: serialization, parsing, marshalling"}[¶](#data-conversion "Permanent link"){.headerlink preview=""}

If you run this example and open your browser at
[http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3){.external-link
target="_blank"}, you will see a response of:

::: highlight
    {"item_id":3}
:::

::: {.admonition .check}
Check

Notice that the value your function received (and returned) is `3`, as a
Python `int`, not a string `"3"`.

So, with that type declaration, **FastAPI** gives you automatic request
[\"parsing\"]{.abbr
title="converting the string that comes from an HTTP request into Python data"}.
:::

## Data validation[¶](#data-validation "Permanent link"){.headerlink preview=""}

But if you go to the browser at
[http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo){.external-link
target="_blank"}, you will see a nice HTTP error of:

::: highlight
    {
      "detail": [
        {
          "type": "int_parsing",
          "loc": [
            "path",
            "item_id"
          ],
          "msg": "Input should be a valid integer, unable to parse string as an integer",
          "input": "foo"
        }
      ]
    }
:::

because the path parameter `item_id` had a value of `"foo"`, which is
not an `int`.

The same error would appear if you provided a `float` instead of an
`int`, as in:
[http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2){.external-link
target="_blank"}

::: {.admonition .check}
Check

So, with the same Python type declaration, **FastAPI** gives you data
validation.

Notice that the error also clearly states exactly the point where the
validation didn\'t pass.

This is incredibly helpful while developing and debugging code that
interacts with your API.
:::

## Documentation[¶](#documentation "Permanent link"){.headerlink preview=""}

And when you open your browser at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs){.external-link
target="_blank"}, you will see an automatic, interactive, API
documentation like:

![](/img/tutorial/path-params/image01.png)

::: {.admonition .check}
Check

Again, just with that same Python type declaration, **FastAPI** gives
you automatic, interactive documentation (integrating Swagger UI).

Notice that the path parameter is declared to be an integer.
:::

## Standards-based benefits, alternative documentation[¶](#standards-based-benefits-alternative-documentation "Permanent link"){.headerlink preview=""}

And because the generated schema is from the
[OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md){.external-link
target="_blank"} standard, there are many compatible tools.

Because of this, **FastAPI** itself provides an alternative API
documentation (using ReDoc), which you can access at
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc){.external-link
target="_blank"}:

![](/img/tutorial/path-params/image02.png)

The same way, there are many compatible tools. Including code generation
tools for many languages.

## Pydantic[¶](#pydantic "Permanent link"){.headerlink preview=""}

All the data validation is performed under the hood by
[Pydantic](https://docs.pydantic.dev/){.external-link target="_blank"},
so you get all the benefits from it. And you know you are in good hands.

You can use the same type declarations with `str`, `float`, `bool` and
many other complex data types.

Several of these are explored in the next chapters of the tutorial.

## Order matters[¶](#order-matters "Permanent link"){.headerlink preview=""}

When creating *path operations*, you can find situations where you have
a fixed path.

Like `/users/me`, let\'s say that it\'s to get data about the current
user.

And then you can also have a path `/users/{user_id}` to get data about a
specific user by some user ID.

Because *path operations* are evaluated in order, you need to make sure
that the path for `/users/me` is declared before the one for
`/users/{user_id}`:

::::::: {.tabbed-set .tabbed-alternate tabs="3:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/users/me")
    async def read_user_me():
        return {"user_id": "the current user"}


    @app.get("/users/{user_id}")
    async def read_user(user_id: str):
        return {"user_id": user_id}
:::
::::
:::::
:::::::

Otherwise, the path for `/users/{user_id}` would match also for
`/users/me`, \"thinking\" that it\'s receiving a parameter `user_id`
with a value of `"me"`.

Similarly, you cannot redefine a path operation:

::::::: {.tabbed-set .tabbed-alternate tabs="4:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/users")
    async def read_users():
        return ["Rick", "Morty"]


    @app.get("/users")
    async def read_users2():
        return ["Bean", "Elfo"]
:::
::::
:::::
:::::::

The first one will always be used since the path matches first.

## Predefined values[¶](#predefined-values "Permanent link"){.headerlink preview=""}

If you have a *path operation* that receives a *path parameter*, but you
want the possible valid *path parameter* values to be predefined, you
can use a standard Python [`Enum`]{.abbr title="Enumeration"}.

### Create an `Enum` class[¶](#create-an-enum-class "Permanent link"){.headerlink preview=""}

Import `Enum` and create a sub-class that inherits from `str` and from
`Enum`.

By inheriting from `str` the API docs will be able to know that the
values must be of type `string` and will be able to render correctly.

Then create class attributes with fixed values, which will be the
available valid values:

::::::: {.tabbed-set .tabbed-alternate tabs="5:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from enum import Enum

    from fastapi import FastAPI


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"


    app = FastAPI()


    @app.get("/models/{model_name}")
    async def get_model(model_name: ModelName):
        if model_name is ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep Learning FTW!"}

        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}

        return {"model_name": model_name, "message": "Have some residuals"}
:::
::::
:::::
:::::::

::: {.admonition .info}
Info

[Enumerations (or enums) are available in
Python](https://docs.python.org/3/library/enum.html){.external-link
target="_blank"} since version 3.4.
:::

::: {.admonition .tip}
Tip

If you are wondering, \"AlexNet\", \"ResNet\", and \"LeNet\" are just
names of Machine Learning [models]{.abbr
title="Technically, Deep Learning model architectures"}.
:::

### Declare a *path parameter*[¶](#declare-a-path-parameter "Permanent link"){.headerlink preview=""}

Then create a *path parameter* with a type annotation using the enum
class you created (`ModelName`):

::::::: {.tabbed-set .tabbed-alternate tabs="6:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from enum import Enum

    from fastapi import FastAPI


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"


    app = FastAPI()


    @app.get("/models/{model_name}")
    async def get_model(model_name: ModelName):
        if model_name is ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep Learning FTW!"}

        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}

        return {"model_name": model_name, "message": "Have some residuals"}
:::
::::
:::::
:::::::

### Check the docs[¶](#check-the-docs "Permanent link"){.headerlink preview=""}

Because the available values for the *path parameter* are predefined,
the interactive docs can show them nicely:

![](/img/tutorial/path-params/image03.png)

### Working with Python *enumerations*[¶](#working-with-python-enumerations "Permanent link"){.headerlink preview=""}

The value of the *path parameter* will be an *enumeration member*.

#### Compare *enumeration members*[¶](#compare-enumeration-members "Permanent link"){.headerlink preview=""}

You can compare it with the *enumeration member* in your created enum
`ModelName`:

::::::: {.tabbed-set .tabbed-alternate tabs="7:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from enum import Enum

    from fastapi import FastAPI


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"


    app = FastAPI()


    @app.get("/models/{model_name}")
    async def get_model(model_name: ModelName):
        if model_name is ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep Learning FTW!"}

        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}

        return {"model_name": model_name, "message": "Have some residuals"}
:::
::::
:::::
:::::::

#### Get the *enumeration value*[¶](#get-the-enumeration-value "Permanent link"){.headerlink preview=""}

You can get the actual value (a `str` in this case) using
`model_name.value`, or in general, `your_enum_member.value`:

::::::: {.tabbed-set .tabbed-alternate tabs="8:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from enum import Enum

    from fastapi import FastAPI


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"


    app = FastAPI()


    @app.get("/models/{model_name}")
    async def get_model(model_name: ModelName):
        if model_name is ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep Learning FTW!"}

        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}

        return {"model_name": model_name, "message": "Have some residuals"}
:::
::::
:::::
:::::::

::: {.admonition .tip}
Tip

You could also access the value `"lenet"` with `ModelName.lenet.value`.
:::

#### Return *enumeration members*[¶](#return-enumeration-members "Permanent link"){.headerlink preview=""}

You can return *enum members* from your *path operation*, even nested in
a JSON body (e.g. a `dict`).

They will be converted to their corresponding values (strings in this
case) before returning them to the client:

::::::: {.tabbed-set .tabbed-alternate tabs="9:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from enum import Enum

    from fastapi import FastAPI


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"


    app = FastAPI()


    @app.get("/models/{model_name}")
    async def get_model(model_name: ModelName):
        if model_name is ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep Learning FTW!"}

        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}

        return {"model_name": model_name, "message": "Have some residuals"}
:::
::::
:::::
:::::::

In your client you will get a JSON response like:

::: highlight
    {
      "model_name": "alexnet",
      "message": "Deep Learning FTW!"
    }
:::

## Path parameters containing paths[¶](#path-parameters-containing-paths "Permanent link"){.headerlink preview=""}

Let\'s say you have a *path operation* with a path `/files/{file_path}`.

But you need `file_path` itself to contain a *path*, like
`home/johndoe/myfile.txt`.

So, the URL for that file would be something like:
`/files/home/johndoe/myfile.txt`.

### OpenAPI support[¶](#openapi-support "Permanent link"){.headerlink preview=""}

OpenAPI doesn\'t support a way to declare a *path parameter* to contain
a *path* inside, as that could lead to scenarios that are difficult to
test and define.

Nevertheless, you can still do it in **FastAPI**, using one of the
internal tools from Starlette.

And the docs would still work, although not adding any documentation
telling that the parameter should contain a path.

### Path convertor[¶](#path-convertor "Permanent link"){.headerlink preview=""}

Using an option directly from Starlette you can declare a *path
parameter* containing a *path* using a URL like:

::: highlight
    /files/{file_path:path}
:::

In this case, the name of the parameter is `file_path`, and the last
part, `:path`, tells it that the parameter should match any *path*.

So, you can use it with:

::::::: {.tabbed-set .tabbed-alternate tabs="10:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/files/{file_path:path}")
    async def read_file(file_path: str):
        return {"file_path": file_path}
:::
::::
:::::
:::::::

::: {.admonition .tip}
Tip

You might need the parameter to contain `/home/johndoe/myfile.txt`, with
a leading slash (`/`).

In that case, the URL would be: `/files//home/johndoe/myfile.txt`, with
a double slash (`//`) between `files` and `home`.
:::

## Recap[¶](#recap "Permanent link"){.headerlink preview=""}

With **FastAPI**, by using short, intuitive and standard Python type
declarations, you get:

- Editor support: error checks, autocompletion, etc.
- Data \"[parsing]{.abbr
  title="converting the string that comes from an HTTP request into Python data"}\"
- Data validation
- API annotation and automatic documentation

And you only have to declare them once.

That\'s probably the main visible advantage of **FastAPI** compared to
alternative frameworks (apart from the raw performance).
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEzIDIwaC0yVjhsLTUuNSA1LjUtMS40Mi0xLjQyTDEyIDQuMTZsNy45MiA3LjkyLTEuNDIgMS40MkwxMyA4eiIgLz48L3N2Zz4=)
Back to top
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
