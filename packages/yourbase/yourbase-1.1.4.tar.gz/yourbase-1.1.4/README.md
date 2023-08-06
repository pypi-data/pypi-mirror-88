# YourBase Python Skipper

## What is this?

This is a Python package you can use in conjunction with [YourBase](https://yourbase.io).

## What does it do?

YourBase has a unique test acceleration that records the execution of your
tests, builds a dependency graph, and uses it to bypass tests that do not
need to be run based on the changes in a commit. This Python package makes
those commands much finer-grained for Python projects, enabling more
acceleration.

To achieve this, when running in the YourBase CI, this package will load a
lighweight wrapper for Python that will determine if a test needs to run
based on the YourBase runtime dependency graph.

## How do I use this?

Simply run
```python
pip install yourbase
pip freeze > requirements.txt
```

YourBase supports [`pytest`][pytest] and [`unittest`][unittest].

If you are using `pytest`, you're done!

If you are using `unittest`, just import `yourbase` before your tests start:
```python
import yourbase
```
It's not important exactly where, as long as it's before your tests run.
Additionally, if your tests define `setUp` or `tearDown` methods on
`unittest.TestCase` or a child class, be sure they are calling
`super().setUp()` and `super().tearDown()` respectively.

If you are using another testing framework, please create an issue to let us
know! We'd love to support it 🎈

No matter your testing framework, after installation you will not be impacted
locally other than seeing a message during testing that your tests will not
be accelerated. When you run your tests in the YourBase CI, they will be
accelerated.

[pytest]: https://pytest.org
[unittest]: https://docs.python.org/3/library/unittest.html

## Contributing
This open source package is a lightweight wrapper for your code that plugs it
into the more complex proprietary systems powering YourBase CI servers. We
welcome contributions to this wrapper, but at this time we have not built
shims or mocks to allow it to be tested front to back outside our systems.

### Code style
We use [Black][black] for code formatting, which is similar in personality to
`gofmt` -- ruthless consistency, no configuration. Your build **will not pass
CI** if the Black run doesn't come back clean, so we recommend you have your
editor automatically run it on save. You can run it manually with

```sh
black .
```

[black]: https://pypi.org/project/black/
