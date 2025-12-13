# Custom Response - HTML, Stream, File, others[¶](#custom-response-html-stream-file-others "Permanent link"){.headerlink preview=""} {#custom-response-html-stream-file-others}

By default, **FastAPI** will return the responses using `JSONResponse`.

You can override it by returning a `Response` directly as seen in
[Return a Response directly](../response-directly/){.internal-link
preview="" target="_blank"}.

But if you return a `Response` directly (or any subclass, like
`JSONResponse`), the data won\'t be automatically converted (even if you
declare a `response_model`), and the documentation won\'t be
automatically generated (for example, including the specific \"media
type\", in the HTTP header `Content-Type` as part of the generated
OpenAPI).

But you can also declare the `Response` that you want to be used (e.g.
any `Response` subclass), in the *path operation decorator* using the
`response_class` parameter.

The contents that you return from your *path operation function* will be
put inside of that `Response`.

And if that `Response` has a JSON media type (`application/json`), like
is the case with the `JSONResponse` and `UJSONResponse`, the data you
return will be automatically converted (and filtered) with any Pydantic
`response_model` that you declared in the *path operation decorator*.

::: {.admonition .note}
Note

If you use a response class with no media type, FastAPI will expect your
response to have no content, so it will not document the response format
in its generated OpenAPI docs.
:::

## Use `ORJSONResponse`[¶](#use-orjsonresponse "Permanent link"){.headerlink preview=""}

For example, if you are squeezing performance, you can install and use
[`orjson`](https://github.com/ijl/orjson){.external-link
target="_blank"} and set the response to be `ORJSONResponse`.

Import the `Response` class (sub-class) you want to use and declare it
in the *path operation decorator*.

For large responses, returning a `Response` directly is much faster than
returning a dictionary.

This is because by default, FastAPI will inspect every item inside and
make sure it is serializable as JSON, using the same [JSON Compatible
Encoder](../../tutorial/encoder/){.internal-link preview=""
target="_blank"} explained in the tutorial. This is what allows you to
return **arbitrary objects**, for example database models.

But if you are certain that the content that you are returning is
**serializable with JSON**, you can pass it directly to the response
class and avoid the extra overhead that FastAPI would have by passing
your return content through the `jsonable_encoder` before passing it to
the response class.

::::::: {.tabbed-set .tabbed-alternate tabs="1:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import ORJSONResponse

    app = FastAPI()


    @app.get("/items/", response_class=ORJSONResponse)
    async def read_items():
        return ORJSONResponse([{"item_id": "Foo"}])
:::
::::
:::::
:::::::

::: {.admonition .info}
Info

The parameter `response_class` will also be used to define the \"media
type\" of the response.

In this case, the HTTP header `Content-Type` will be set to
`application/json`.

And it will be documented as such in OpenAPI.
:::

::: {.admonition .tip}
Tip

The `ORJSONResponse` is only available in FastAPI, not in Starlette.
:::

## HTML Response[¶](#html-response "Permanent link"){.headerlink preview=""}

To return a response with HTML directly from **FastAPI**, use
`HTMLResponse`.

- Import `HTMLResponse`.
- Pass `HTMLResponse` as the parameter `response_class` of your *path
  operation decorator*.

::::::: {.tabbed-set .tabbed-alternate tabs="2:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI()


    @app.get("/items/", response_class=HTMLResponse)
    async def read_items():
        return """
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
        """
:::
::::
:::::
:::::::

::: {.admonition .info}
Info

The parameter `response_class` will also be used to define the \"media
type\" of the response.

In this case, the HTTP header `Content-Type` will be set to `text/html`.

And it will be documented as such in OpenAPI.
:::

### Return a `Response`[¶](#return-a-response "Permanent link"){.headerlink preview=""}

As seen in [Return a Response
directly](../response-directly/){.internal-link preview=""
target="_blank"}, you can also override the response directly in your
*path operation*, by returning it.

The same example from above, returning an `HTMLResponse`, could look
like:

::::::: {.tabbed-set .tabbed-alternate tabs="3:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI()


    @app.get("/items/")
    async def read_items():
        html_content = """
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
:::
::::
:::::
:::::::

::: {.admonition .warning}
Warning

A `Response` returned directly by your *path operation function* won\'t
be documented in OpenAPI (for example, the `Content-Type` won\'t be
documented) and won\'t be visible in the automatic interactive docs.
:::

::: {.admonition .info}
Info

Of course, the actual `Content-Type` header, status code, etc, will come
from the `Response` object you returned.
:::

### Document in OpenAPI and override `Response`[¶](#document-in-openapi-and-override-response "Permanent link"){.headerlink preview=""}

If you want to override the response from inside of the function but at
the same time document the \"media type\" in OpenAPI, you can use the
`response_class` parameter AND return a `Response` object.

The `response_class` will then be used only to document the OpenAPI
*path operation*, but your `Response` will be used as is.

#### Return an `HTMLResponse` directly[¶](#return-an-htmlresponse-directly "Permanent link"){.headerlink preview=""}

For example, it could be something like:

::::::: {.tabbed-set .tabbed-alternate tabs="4:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI()


    def generate_html_response():
        html_content = """
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)


    @app.get("/items/", response_class=HTMLResponse)
    async def read_items():
        return generate_html_response()
:::
::::
:::::
:::::::

In this example, the function `generate_html_response()` already
generates and returns a `Response` instead of returning the HTML in a
`str`.

By returning the result of calling `generate_html_response()`, you are
already returning a `Response` that will override the default
**FastAPI** behavior.

But as you passed the `HTMLResponse` in the `response_class` too,
**FastAPI** will know how to document it in OpenAPI and the interactive
docs as HTML with `text/html`:

![](/img/tutorial/custom-response/image01.png)

## Available responses[¶](#available-responses "Permanent link"){.headerlink preview=""}

Here are some of the available responses.

Keep in mind that you can use `Response` to return anything else, or
even create a custom sub-class.

::: {.admonition .note}
Technical Details

You could also use `from starlette.responses import HTMLResponse`.

**FastAPI** provides the same `starlette.responses` as
`fastapi.responses` just as a convenience for you, the developer. But
most of the available responses come directly from Starlette.
:::

### `Response`[¶](#response "Permanent link"){.headerlink preview=""}

The main `Response` class, all the other responses inherit from it.

You can return it directly.

It accepts the following parameters:

- `content` - A `str` or `bytes`.
- `status_code` - An `int` HTTP status code.
- `headers` - A `dict` of strings.
- `media_type` - A `str` giving the media type. E.g. `"text/html"`.

FastAPI (actually Starlette) will automatically include a Content-Length
header. It will also include a Content-Type header, based on the
`media_type` and appending a charset for text types.

::::::: {.tabbed-set .tabbed-alternate tabs="5:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI, Response

    app = FastAPI()


    @app.get("/legacy/")
    def get_legacy_data():
        data = """<?xml version="1.0"?>
        <shampoo>
        <Header>
            Apply shampoo here.
        </Header>
        <Body>
            You'll have to use soap here.
        </Body>
        </shampoo>
        """
        return Response(content=data, media_type="application/xml")
:::
::::
:::::
:::::::

### `HTMLResponse`[¶](#htmlresponse "Permanent link"){.headerlink preview=""}

Takes some text or bytes and returns an HTML response, as you read
above.

### `PlainTextResponse`[¶](#plaintextresponse "Permanent link"){.headerlink preview=""}

Takes some text or bytes and returns a plain text response.

::::::: {.tabbed-set .tabbed-alternate tabs="6:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    app = FastAPI()


    @app.get("/", response_class=PlainTextResponse)
    async def main():
        return "Hello World"
:::
::::
:::::
:::::::

### `JSONResponse`[¶](#jsonresponse "Permanent link"){.headerlink preview=""}

Takes some data and returns an `application/json` encoded response.

This is the default response used in **FastAPI**, as you read above.

### `ORJSONResponse`[¶](#orjsonresponse "Permanent link"){.headerlink preview=""}

A fast alternative JSON response using
[`orjson`](https://github.com/ijl/orjson){.external-link
target="_blank"}, as you read above.

::: {.admonition .info}
Info

This requires installing `orjson` for example with `pip install orjson`.
:::

### `UJSONResponse`[¶](#ujsonresponse "Permanent link"){.headerlink preview=""}

An alternative JSON response using
[`ujson`](https://github.com/ultrajson/ultrajson){.external-link
target="_blank"}.

::: {.admonition .info}
Info

This requires installing `ujson` for example with `pip install ujson`.
:::

::: {.admonition .warning}
Warning

`ujson` is less careful than Python\'s built-in implementation in how it
handles some edge-cases.
:::

::::::: {.tabbed-set .tabbed-alternate tabs="7:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import UJSONResponse

    app = FastAPI()


    @app.get("/items/", response_class=UJSONResponse)
    async def read_items():
        return [{"item_id": "Foo"}]
:::
::::
:::::
:::::::

::: {.admonition .tip}
Tip

It\'s possible that `ORJSONResponse` might be a faster alternative.
:::

### `RedirectResponse`[¶](#redirectresponse "Permanent link"){.headerlink preview=""}

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by
default.

You can return a `RedirectResponse` directly:

::::::: {.tabbed-set .tabbed-alternate tabs="8:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import RedirectResponse

    app = FastAPI()


    @app.get("/typer")
    async def redirect_typer():
        return RedirectResponse("https://typer.tiangolo.com")
:::
::::
:::::
:::::::

------------------------------------------------------------------------

Or you can use it in the `response_class` parameter:

::::::: {.tabbed-set .tabbed-alternate tabs="9:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import RedirectResponse

    app = FastAPI()


    @app.get("/fastapi", response_class=RedirectResponse)
    async def redirect_fastapi():
        return "https://fastapi.tiangolo.com"
:::
::::
:::::
:::::::

If you do that, then you can return the URL directly from your *path
operation* function.

In this case, the `status_code` used will be the default one for the
`RedirectResponse`, which is `307`.

------------------------------------------------------------------------

You can also use the `status_code` parameter combined with the
`response_class` parameter:

::::::: {.tabbed-set .tabbed-alternate tabs="10:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import RedirectResponse

    app = FastAPI()


    @app.get("/pydantic", response_class=RedirectResponse, status_code=302)
    async def redirect_pydantic():
        return "https://docs.pydantic.dev/"
:::
::::
:::::
:::::::

### `StreamingResponse`[¶](#streamingresponse "Permanent link"){.headerlink preview=""}

Takes an async generator or a normal generator/iterator and streams the
response body.

::::::: {.tabbed-set .tabbed-alternate tabs="11:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse

    app = FastAPI()


    async def fake_video_streamer():
        for i in range(10):
            yield b"some fake video bytes"


    @app.get("/")
    async def main():
        return StreamingResponse(fake_video_streamer())
:::
::::
:::::
:::::::

#### Using `StreamingResponse` with file-like objects[¶](#using-streamingresponse-with-file-like-objects "Permanent link"){.headerlink preview=""}

If you have a
[file-like](https://docs.python.org/3/glossary.html#term-file-like-object){.external-link
target="_blank"} object (e.g. the object returned by `open()`), you can
create a generator function to iterate over that file-like object.

That way, you don\'t have to read it all first in memory, and you can
pass that generator function to the `StreamingResponse`, and return it.

This includes many libraries to interact with cloud storage, video
processing, and others.

::::::: {.tabbed-set .tabbed-alternate tabs="12:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse

    some_file_path = "large-video-file.mp4"
    app = FastAPI()


    @app.get("/")
    def main():
        def iterfile():  # (1)
            with open(some_file_path, mode="rb") as file_like:  # (2)
                yield from file_like  # (3)

        return StreamingResponse(iterfile(), media_type="video/mp4")
:::
::::
:::::
:::::::

1.  This is the generator function. It\'s a \"generator function\"
    because it contains `yield` statements inside.

2.  By using a `with` block, we make sure that the file-like object is
    closed after the generator function is done. So, after it finishes
    sending the response.

3.  This `yield from` tells the function to iterate over that thing
    named `file_like`. And then, for each part iterated, yield that part
    as coming from this generator function (`iterfile`).

    So, it is a generator function that transfers the \"generating\"
    work to something else internally.

    By doing it this way, we can put it in a `with` block, and that way,
    ensure that the file-like object is closed after finishing.

::: {.admonition .tip}
Tip

Notice that here as we are using standard `open()` that doesn\'t support
`async` and `await`, we declare the path operation with normal `def`.
:::

### `FileResponse`[¶](#fileresponse "Permanent link"){.headerlink preview=""}

Asynchronously streams a file as the response.

Takes a different set of arguments to instantiate than the other
response types:

- `path` - The file path to the file to stream.
- `headers` - Any custom headers to include, as a dictionary.
- `media_type` - A string giving the media type. If unset, the filename
  or path will be used to infer a media type.
- `filename` - If set, this will be included in the response
  `Content-Disposition`.

File responses will include appropriate `Content-Length`,
`Last-Modified` and `ETag` headers.

::::::: {.tabbed-set .tabbed-alternate tabs="13:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import FileResponse

    some_file_path = "large-video-file.mp4"
    app = FastAPI()


    @app.get("/")
    async def main():
        return FileResponse(some_file_path)
:::
::::
:::::
:::::::

You can also use the `response_class` parameter:

::::::: {.tabbed-set .tabbed-alternate tabs="14:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import FileResponse

    some_file_path = "large-video-file.mp4"
    app = FastAPI()


    @app.get("/", response_class=FileResponse)
    async def main():
        return some_file_path
:::
::::
:::::
:::::::

In this case, you can return the file path directly from your *path
operation* function.

## Custom response class[¶](#custom-response-class "Permanent link"){.headerlink preview=""}

You can create your own custom response class, inheriting from
`Response` and using it.

For example, let\'s say that you want to use
[`orjson`](https://github.com/ijl/orjson){.external-link
target="_blank"}, but with some custom settings not used in the included
`ORJSONResponse` class.

Let\'s say you want it to return indented and formatted JSON, so you
want to use the orjson option `orjson.OPT_INDENT_2`.

You could create a `CustomORJSONResponse`. The main thing you have to do
is create a `Response.render(content)` method that returns the content
as `bytes`:

::::::: {.tabbed-set .tabbed-alternate tabs="15:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from typing import Any

    import orjson
    from fastapi import FastAPI, Response

    app = FastAPI()


    class CustomORJSONResponse(Response):
        media_type = "application/json"

        def render(self, content: Any) -> bytes:
            assert orjson is not None, "orjson must be installed"
            return orjson.dumps(content, option=orjson.OPT_INDENT_2)


    @app.get("/", response_class=CustomORJSONResponse)
    async def main():
        return {"message": "Hello World"}
:::
::::
:::::
:::::::

Now instead of returning:

::: highlight
    {"message": "Hello World"}
:::

\...this response will return:

::: highlight
    {
      "message": "Hello World"
    }
:::

Of course, you will probably find much better ways to take advantage of
this than formatting JSON. 😉

## Default response class[¶](#default-response-class "Permanent link"){.headerlink preview=""}

When creating a **FastAPI** class instance or an `APIRouter` you can
specify which response class to use by default.

The parameter that defines this is `default_response_class`.

In the example below, **FastAPI** will use `ORJSONResponse` by default,
in all *path operations*, instead of `JSONResponse`.

::::::: {.tabbed-set .tabbed-alternate tabs="16:1"}
::: tabbed-labels
Python 3.8+
:::

::::: tabbed-content
:::: tabbed-block
::: highlight
    from fastapi import FastAPI
    from fastapi.responses import ORJSONResponse

    app = FastAPI(default_response_class=ORJSONResponse)


    @app.get("/items/")
    async def read_items():
        return [{"item_id": "Foo"}]
:::
::::
:::::
:::::::

::: {.admonition .tip}
Tip

You can still override `response_class` in *path operations* as before.
:::

## Additional documentation[¶](#additional-documentation "Permanent link"){.headerlink preview=""}

You can also declare the media type and many other details in OpenAPI
using `responses`: [Additional Responses in
OpenAPI](../additional-responses/){.internal-link preview=""
target="_blank"}.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEzIDIwaC0yVjhsLTUuNSA1LjUtMS40Mi0xLjQyTDEyIDQuMTZsNy45MiA3LjkyLTEuNDIgMS40MkwxMyA4eiIgLz48L3N2Zz4=)
Back to top
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
