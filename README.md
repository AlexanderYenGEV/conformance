# TROLIE 1.0 Conformance Suite

This repo provides testing tools to assess how well implementations conform to
the [TROLIE API specification](https://trolie.energy/spec-1.0).

### Who is this for?

Vendors and their customers should use these tests to verify which TROLIE
operations are correctly supported by their implementations.

Additionally, there are limits to the expressivity of OpenAPI; these tests will
clarify the intended behavior where the spec is ambiguous.

Finally, we anticipate this test suite will be used in CI pipelines as fast functional tests.

### What is it?

The Conformance Suite is implemented as a set of BDD-style tests, using pytest-bdd. These tests are organized into "conformance profiles":

* Forecasting (in progress)
* Real-Time (not started)
* Seasonal (not started)
* RC Peering (not started)

#### Test Data

The majority of conformance tests will need to be able to make assumptions about
the model that is loaded into the TROLIE server implementation. This includes
Ratings Obligations, Monitoring Sets, and power system resources that will be
used in the tests. To organize those conceptually, we intend to map onto the
[WSCC 9-Bus System](https://icseg.iti.illinois.edu/wscc-9-bus-system/). Included will be a standalone JSON model that closely follows the
`application/vnd.trolie.monitoring-set.v1+json` media type, enriched with the other information needed to represent the test data.

### How do I get started?

Checkout this repo, and open it with VS Code. It is configured with a devcontainer, so you will be prompted to build it and reopen a session with the devcontainer. After the devcontainer is started, there will be a Jupyter server running at `localhost:8888`; instructions for running the various Conformance Profiles will be found there.

### Running Locally

#### Step 1:
In [`pytest.ini`](./pytest.ini), update the `TROLIE_BASE_URL` variable.

#### Step 2:
Currently the `TrolieClient` implementation in
[`test/helpers.py`](test/helpers.py) assumes the use of a bearer token in the
authorization header. We have provided a hook (see the `AuthTokenProvider`
protocol in `helpers.py`) for your implementation to return that token.

The simplest way to use that hook is to copy
[`auth_token_provider_outline.py`](./auth_token_provider_outline.py) to
`test/auth_token_provider.py` then update all of the `<<change me>>` strings in
your environment.

In the future we may switch to defining a protocol for `TrolieClient` instead,
so that users of this conformance suite can control the entire HTTP stack.

#### Step 3:
Build the LEP cluster and update host files.

#### Step 3.1: 
Generate admin-api-client.yaml for [`auth_token_provider_outline.py`](./auth_token_provider_outline.py)

#### Step 4.1:
Run ```$ pytest -v --capture=tee-sys -q -rA --tb=auto --alluredir=allure-results --clean-alluredir``` in the terminal.

#### Step 4.2:
Run ```allure serve allure-results``` to generate the report

#### Step 5 (Optional):
In [`Local Conformance_Profile.ipynb`](./Forecasting_Conformance_Profile.ipynb) change `TROLIE_BASE_URL` and `TZ` variables to run the test suite through the jupyter notebook.

### Running in CI Pipeline (For LEP)

#### Step 1: 
Build the LEP cluster 

#### Step 2: 
Run TROLIE conformance tests by unchecking every parameter except `deployTrolieConformance` and switching testRunProfile to `manual`

#### Step 3:
A downloadable .zip file should be created and the Allure plugin to should appear, click the Allure plugin button to view the report
